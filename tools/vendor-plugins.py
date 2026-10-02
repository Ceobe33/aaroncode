#!/usr/bin/env python3
"""
把主题用到的第三方 JS/CSS 下载到站点自己的 source/pluginsSrc/ 下，
配合 _config.butterfly.yml 里的 CDN.third_party_provider: local，
让访客不再去 cdn.jsdelivr.net 拉任何东西。

放在站点 source/ 而不是主题里，是因为 Hexo 中「主题的同名资源会覆盖站点资源」，
而反过来站点资源不受主题影响 —— 这样 ChinaCareer 等其它站点继续各用各的。

版本从 themes/butterfly/plugins.yml 读取（即主题实测过的版本），避免 jsdelivr
上 "latest" 漂移。katex / hexo-math 直接从 node_modules 取，保证 CSS 与
服务端渲染用的 JS 版本一致。

用法：
    python3 tools/vendor-plugins.py
"""

import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent
THEME_DIR = SITE_DIR / "themes" / "butterfly"
PLUGINS_YML = THEME_DIR / "plugins.yml"
VENDOR_DIR = SITE_DIR / "source" / "pluginsSrc"
CACHE_DIR = Path.home() / ".cache" / "hexo-plugins"

# 需要本地的 plugins.yml 条目 -> 额外要一起带上的目录（相对包根）
NEEDED = {
    "fancybox_css_v4": [],
    "fancybox_v4": [],
    "fontawesomeV6": ["webfonts"],
    "algolia_search_v4": [],
    "instantsearch_v4": [],
    "aplayer_css": [],
    "aplayer_js": [],
    "meting_js": [],
    "blueimp_md5": [],
    "instantpage": [],
    "snackbar_css": [],
    "snackbar": [],
    "pjax": [],
    "lazyload": [],
}

# katex 相关的 CSS/JS 从 node_modules 直接拷，版本跟随服务端渲染用的 katex
FROM_NODE_MODULES = {
    "katex": ("katex", "dist/katex.min.css"),
    "katex_copytex": ("katex", "dist/contrib/copy-tex.min.js"),
}


def parse_plugins_yml(path: Path) -> dict:
    """够用的极简解析：顶层 `key:` 起一条，缩进的 `k: v` 作为属性。"""
    entries, current = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\S[^:]*):\s*(.*)$", raw)
        if m and not raw.startswith(" "):
            current = m.group(1)
            entries[current] = {}
        elif current and ":" in raw:
            k, v = raw.strip().split(":", 1)
            entries[current][k] = v.strip().strip("'\"")
    return entries


def fetch_tarball(name: str, version: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe = name.replace("/", "_").replace("@", "")
    tarball = CACHE_DIR / f"{safe}-{version}.tgz"
    if tarball.exists():
        return tarball
    print(f"  下载 {name}@{version}")
    subprocess.run(
        ["npm", "pack", f"{name}@{version}", "--silent", "--pack-destination", str(CACHE_DIR)],
        check=True, stdout=subprocess.DEVNULL,
    )
    produced = sorted(CACHE_DIR.glob(f"*{version}.tgz"), key=lambda p: p.stat().st_mtime)
    if not produced:
        sys.exit(f"npm pack 没有产出 {name}@{version} 的 tarball")
    if produced[-1] != tarball:
        shutil.move(str(produced[-1]), tarball)
    return tarball


def extract(tarball: Path, name: str, wanted: list, extra_dirs: list) -> None:
    dest_root = VENDOR_DIR / name
    with tarfile.open(tarball) as tf:
        members = tf.getnames()
        picked = []
        for rel in wanted:
            member = f"package/{rel}"
            if member not in members:
                sys.exit(f"{tarball.name} 里没有 {member}")
            picked.append(member)
        for d in extra_dirs:
            picked += [m for m in members if m.startswith(f"package/{d}/")]

        for member in picked:
            rel = member[len("package/"):]
            target = dest_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                continue
            target.write_bytes(src.read())
            print(f"  {target.relative_to(SITE_DIR)}  ({target.stat().st_size / 1024:.0f}KB)")


def copy_from_node_modules(pkg: str, rel: str, name: str) -> None:
    src = SITE_DIR / "node_modules" / pkg / rel
    if not src.exists():
        sys.exit(f"缺少 {src}，先 npm install")
    target = VENDOR_DIR / name / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)
    print(f"  {target.relative_to(SITE_DIR)}  ({target.stat().st_size / 1024:.0f}KB)")


def main() -> None:
    entries = parse_plugins_yml(PLUGINS_YML)
    print("从 plugins.yml vendor 第三方库 -> source/pluginsSrc/")
    done = set()
    for key in NEEDED:
        if key not in entries:
            sys.exit(f"plugins.yml 里没有 {key}")
        name = entries[key]["name"]
        version = entries[key]["version"]
        file = entries[key]["file"]
        if name in done:
            continue
        # 同一个 npm 包可能被多个条目引用（如 @fancyapps/ui 的 css 和 js）
        siblings = [k for k in NEEDED if entries[k]["name"] == name]
        wanted = [entries[k]["file"] for k in siblings]
        extras = [d for k in siblings for d in NEEDED[k]]
        extract(fetch_tarball(name, version), name, wanted, extras)
        done.add(name)

    print("katex / hexo-math 从 node_modules 取")
    for _key, (pkg, rel) in FROM_NODE_MODULES.items():
        copy_from_node_modules(pkg, rel, "katex")
    copy_from_node_modules("hexo-math", "dist/style.css", "hexo-math")

    total = sum(f.stat().st_size for f in VENDOR_DIR.rglob("*") if f.is_file())
    print(f"\n完成，source/pluginsSrc 共 {total / 1048576:.1f}MB")
    print("记得把 _config.butterfly.yml 的 CDN.third_party_provider 设为 local")


if __name__ == "__main__":
    main()
