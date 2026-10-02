#!/usr/bin/env python3
"""
按站点实际用到的字符裁剪自托管字体。

背景：themes/butterfly/source 里放的是完整字体（Source Han Sans CN 每个字重
约 6MB，4 个字重共 24MB），首页光字体就要下 12MB 以上。本脚本从生成好的
public/**/*.html 里收集所有出现过的字符，为每个 CJK 字重产出一份子集，
放到站点自己的 source/cn/ 下覆盖主题里的完整字体。

注意：新增文章如果引入了新的汉字，需要重新跑一次本脚本，否则那些字会回退到
系统字体显示。

用法（在站点根目录）：
    npx hexo generate          # 先构建，让脚本能读到全部页面的文字
    python3 tools/subset-fonts.py

    # 只重做 CJK、跳过 JetBrains 转换
    python3 tools/subset-fonts.py --skip-mono
"""

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent
THEME_DIR = SITE_DIR / "themes" / "butterfly"

# 完整字体的母版放在主题的 fonts-src/ 下：它在 source/ 之外，不会被复制进
# public/，因此不会进部署产物，但重新子集化时仍然需要它。
CJK_MASTER_DIR = THEME_DIR / "fonts-src" / "cn"
MONO_MASTER_DIR = THEME_DIR / "fonts-src" / "mono"

# 4 个 CJK 字重：主题 function.styl 里声明的 font-weight
CJK_WEIGHTS = {
    "Light": 300,
    "Regular": 400,
    "Bold": 700,
    "Heavy": 900,
}

# JetBrains Mono 只保留这几个 face（主题 CSS 已同步删减到这几个）
MONO_FACES = {
    "Regular": "normal",
    "Bold": "normal",
    "Italic": "italic",
}

# 除页面文字外必须保留的字符：ASCII 可见字符 + 常见中英文标点/全角形式。
# 这些通常出现在代码块、搜索结果、复制粘贴内容里，未必出现在 HTML 文本节点中。
EXTRA_CHARS = (
    "".join(chr(c) for c in range(0x20, 0x7F))
    + "，。、；：？！“”‘’（）《》【】〈〉「」『』…—～·￥×÷±°§¶†‡"
    + "　、。〃々〆〇〈〉《》「」『』【】〒〓〔〕〖〗〘〙〚〛〜〝〞"
    + "！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠"
    + "［＼］＾＿｀｛｜｝～￥"
    + "→←↑↓⇒⇔✓✔✗✘★☆●○◆◇■□▲▼△▽※"
)


def collect_charset() -> set:
    html_files = sorted((SITE_DIR / "public").rglob("*.html"))
    if not html_files:
        sys.exit("public/ 下没有 HTML，先跑 npx hexo generate")

    chars = set(EXTRA_CHARS)
    for path in html_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        # 只取正文，避免把内联 JS/CSS 里的字符也算进来
        text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.S | re.I)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
        chars |= {c for c in text if not c.isspace()}

    print(f"扫描 {len(html_files)} 个页面，去重字符 {len(chars)} 个"
          f"（其中 CJK {sum(1 for c in chars if ord(c) > 0x2E80)} 个）")
    return chars


def run_subset(src: Path, dst: Path, charset_file: Path) -> None:
    if not src.exists():
        sys.exit(f"缺少源字体：{src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "pyftsubset", str(src),
        f"--text-file={charset_file}",
        "--flavor=woff2",
        "--layout-features=*",
        f"--output-file={dst}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    print(f"  {dst.relative_to(SITE_DIR)}  {src.stat().st_size / 1048576:.1f}MB"
          f" -> {dst.stat().st_size / 1024:.0f}KB")


def to_woff2(src: Path, dst: Path) -> None:
    """整字体转 woff2（不裁字符，保留 Nerd Font 图标字形）。"""
    if not src.exists():
        sys.exit(f"缺少源字体：{src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    from fontTools.ttLib import TTFont
    font = TTFont(str(src))
    font.flavor = "woff2"
    font.save(str(dst))
    font.close()
    print(f"  {dst.relative_to(SITE_DIR)}  {src.stat().st_size / 1048576:.1f}MB"
          f" -> {dst.stat().st_size / 1024:.0f}KB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-mono", action="store_true",
                        help="跳过 JetBrains Mono 的 woff2 转换")
    args = parser.parse_args()

    charset = collect_charset()
    charset_file = SITE_DIR / "tools" / "font-charset.txt"
    charset_file.write_text("".join(sorted(charset)), encoding="utf-8")
    print(f"字符集写入 {charset_file.relative_to(SITE_DIR)}")

    print("Source Han Sans CN 子集 -> source/cn/")
    for name in CJK_WEIGHTS:
        run_subset(
            CJK_MASTER_DIR / f"SourceHanSansCN-{name}.otf",
            SITE_DIR / "source" / "cn" / f"SourceHanSansCN-{name}.woff2",
            charset_file,
        )

    if not args.skip_mono:
        print("JetBrains Mono Nerd Font Mono -> themes/butterfly/source/fonts/")
        for name in MONO_FACES:
            to_woff2(
                MONO_MASTER_DIR / f"JetBrainsMonoNerdFontMono-{name}.ttf",
                THEME_DIR / "source" / "fonts" / f"JetBrainsMonoNerdFontMono-{name}.woff2",
            )

    print("完成，记得重新 npx hexo generate 验证。")


if __name__ == "__main__":
    main()
