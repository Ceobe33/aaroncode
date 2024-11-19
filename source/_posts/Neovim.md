---
title: Neovim note
date: "2023-05-02 14:00"
cover: Vim-m.png
tags: [Note, Neovim, Tutorial]
description: vim/neovim note
---

## Tutorials

- [蓝桥实验楼](https://www.lanqiao.cn/courses/2840)
  - [github](https://github.com/overmind1980/oeasyvim), [gitee](https://gitee.com/overmind1980/oeasyvim)

## knowledge

everything be required which inside `lua/` directory

## Install Vim on Ubuntu

1. [install windows virtual Linux](https://learn.microsoft.com/en-us/windows/wsl/install) then
2. install nvim on Ubuntu [3 Ways to install NeoVim on Ubuntu 22.04 or 20.04](https://linux.how2shout.com/3-ways-to-install-neovim-on-ubuntu-22-04-or-20-04)
  - official[link](https://github.com/neovim/neovim/wiki/Building-Neovim)
    1. install requirements
      `sudo apt-get install ninja-build gettext cmake unzip curl`
  - maybe have some issue about Hyper-V
    1. [win10](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/about/)&#x20;
    2. [win11](https://techcommunity.microsoft.com/t5/educator-developer-blog/step-by-step-enabling-hyper-v-for-use-on-windows-11/ba-p/3745905)
        1. you may need to learn [配置和管理 Hyper-V](https://learn.microsoft.com/zh-cn/training/modules/configure-manage-hyper-v/?WT.mc_id=academic-89565-abartolo)
    maybe have issue about `sudo dpkg -i nvim-linux64.deb` ==though it is not same step(it's another way to install Neovim)==
        1.  \[Try] [How to Install Python Pip on Ubuntu 20.04](https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/#:\~:text=To%20install%20pip%20for%20Python%203%20on%20%3Cu%3EUbuntu%3C%2Fu%3E,verify%20the%20installation%20by%20checking%20the%20pip%20version%3A)
  - install latest nvim
    1. download appimage [nvim devolopment](https://github.com/neovim/neovim/releases/nightly)
    2. first of all, try to run this file
        1. install requirement(on Ubuntu >= 22.04)  \
            `sudo add-apt-repository universe`  \
            `sudo apt install libfuse2`
        2. `sudo chmod u+x nvim.appimage`
        3. `./nvim.appimage`
    3. move `nvim.appimage` to `nvim/`
        - `mv nvim.appimage ./nvim`
    4. change nvim directory to execute mode
        - `sudo chmod +x nvim`
    5. i don't know what's meaning of this step
        - `sudo chown root:root nvim`
    6. idk 2
        - `sudo mv nvim /usr/bin`
  - install from source [toturial](https://github.com/neovim/neovim/wiki/Building-Neovim#build-prerequisites)
    1. clone repo `git clone https://github.com/neovim/neovim`
    - ==Issues==  
      1. `OpenSSL: error:0A00010B:SSL routines::wrong version number` <br>`Unable to establish SSL connection.`

3. configuration step
  1. install packer

- Ubuntu command

  1. `mv <file name> <new name>`   modified file name&#x20;

- [download files on linux](https://linux.cn/article-12752-1.html)
  - use appimage file [youtube link](https://youtu.be/rHxgQ8c6H7k)

### about windows

- install wget: [download Url](https://eternallybored.org/misc/wget/)
  > article： [download-your-website-with-wget](https://builtvisible.com/download-your-website-with-wget/)
-

### about ubuntu

- wsl install

  1. [如何在 Windows 上用 WSL 2 快速体验丝般顺滑的 Linux](https://www.51cto.com/article/720323.html)

  - error:
    1. couldn't install ubuntu subsystem on window
        1. fix: 控制面板-卸载程序-启用或关闭Windows功能， 两个功能~~开关~~重启一下
           - [ ] 适用于Linux的Windows子系统
           - [ ] 虚拟机平台
- input command didn't display 终端命令不显示
  - 关闭输入回显 `stty -echo`
  - 打开输入回显 `stty echo`

### about node, npm

- knowledge
  1. [如何将 Node 和 NPM 更新到最新版本](https://www.freecodecamp.org/chinese/news/how-to-update-node-and-npm-to-the-latest-version/)
- issue: `permmision denied npm`
  - fix:
    1. `sudo npm install -g appium --allow-root`
    2. `sudo npm install -g appium --unsafe-perm=true --allow-root`

### terminal emulator

- kitty
  - error

    ```bash
    aaron@Aaron:~$ kitty
    [079 22:57:35.657859] [glfw error 65542]: EGL: Library not found
    [079 22:57:35.659454] Traceback (most recent call last):
    File "/usr/bin/../lib/kitty/kitty/main.py", line 344, in main
      _main()
    File "/usr/bin/../lib/kitty/kitty/main.py", line 337, in _main
      run_app(opts, cli_opts, bad_lines)
    File "/usr/bin/../lib/kitty/kitty/main.py", line 183, in __call__
      _run_app(opts, args, bad_lines)
    File "/usr/bin/../lib/kitty/kitty/main.py", line 156, in _run_app
      window_id = create_os_window(
    ValueError: Failed to create GLFWwindow
    ```

  - fix: `sudo apt-get install libglfw3-dev libgles2-mesa-dev`

### install plugin

[0 to LSP : Neovim RC From Scratch](https://youtu.be/w7i4amO_zaE)

- maybe have some problem over `$keymap$` setting, fix trying:
  - upgrade nvim version
- error: `[mason-lspconfig.nvim] Server "sumneko_lua" is not a valid entry in ensure_installed. Make sure to only provide lspconfig server names.`
  - fix:

配置加速下载

1. [neovim 插件管理器packer配置加速下载](https://www.bilibili.com/read/cv16639595)

#### packer/Plugins

- **Error**
  1. `job.lua:94: Killing git due to timeout!`
    1. fix: `sudo apt update`
  2. `couldn't find 'packer' identifier`
    1. fix: exit nvim, re-enter
- **Install**
  1. -treesitter playground* install **failed**
  2. -telescope* installed
    - [ ] how to set exploring range
  3.

### nvim issue

- [x] DONE: need to **source** all of files over every jump nvim in time
  - just follow [official tutorial](https://neovim.io/doc/user/starting.html#initialization:~:text=7.%20Load%20user%20config%20(execute%20Ex%20commands%20from%20files%2C%20environment%2C%20%E2%80%A6).)
    >   Unix			    ~/.config/nvim/init.vim		    (or init.lua)
	    Windows			    ~/AppData/Local/nvim/init.vim	(or init.lua)
	    $XDG_CONFIG_HOME  	$XDG_CONFIG_HOME/nvim/init.vim	(or init.lua)

### git

- error
  - `fatal: unable to access '`[`https://github.com/neovim/neovim/`](https://github.com/neovim/neovim/)`': GnuTLS recv error (-110): The TLS connection was non-properly terminated`
  - fix:
    1. \[option] `git config --global http.proxy http://proxy.server.com:8080`, `git config --global https.proxy https://proxy.server.com:8080`
    2. `git config --global --unset http.proxy`, `git config --global --unset https.proxy`
    3. then try to clone again
  - if speed too slow try to use this:

  - [git clone SPEEDUP 网达极客社区](https://gitclone.com/)

## nvim operate

- **copy paste**
- inside vim
  - copy: `y`, paste: `p`
- from outside to inside
  - copy(win): `Ctrl c`, paste: `"+p`
- from inside to outside
  - copy: `"+y`, paste(win): `Ctrl v`
- **replace**
  1. slect statement
  2. type command `s/src/des/g`  /g means global(over select)

### with files

- open linux grep result files as nvim args
  `grep -rf "<grep-str>" . | xargs vim`
  > value `f` is don't display grep content

### have unnormal symbol

- `^M`
  - regular expression(didn't work)
  - `%s/^M//g`
  - change file encode type
    1. `e ++ff=dos`
    2. `set ff=unix`
    3. `wq`
- **comment** code block quickly
  1. $visual line mode$
     1. select the lines what you want to comment
     2. `Shift-I` to insert comment symbol('--, //, $, #')
     3. complete then press `Esc` twice to confirm
  2. command $normal mode$
     1. `:[start_line],[end_line]s/^/--`  eg:`:10,15/^/--`~(.lua)~
  3. regular expresion
     1. `:g/\while/s/^/#`~(.py)~
- **uncomment**
  1. $visual mode$
     1. `Ctrl-v` select the comment symbol
     2. press `x` to remove that

## cursor

| command/ hot keys                   | function                                                         |
| ----------------------------------- | ---------------------------------------------------------------- |
| `vim .`                             | open directory tree                                              |
| **Move Cursor**                     | **====================**                                         |
| `f`                                 | search -*f**orward                                               |
| `;`                                 | repeat forward last search                                       |
| `,`                                 | repeat back last search                                          |
| `_`, `$$`, `0`                      | move cursor to `line first character`, `line tail`, `line begin` |
| `\$` (under normal mode, no'\\')    | create new file                                                  |
| `ci<symbol pair>`                   | eg:`ci(`will clear inside '()' content and the cursor jump into  |
| `V%`                                | jump to another pair(from open to close bracket etc...)          |
| `q:`                                | open cmd history                                                 |
| `%`, `d`                            | create file, create directory                                    |
| **Telescope view** `Alt h/j/k/l, i` | jump to `$Results$` window, jump back input label                |
| **File telescope**                  |                                                                  |
| `<C-o>`                             | jump back last cursor position                                   |
| `gx`                                | open/direct url link to your default browser                     |
| `args`                              | list the open files(buffers?)                                    |

## vim config file

```
" edit setting
set tabstop=4  " tab key contain space num

" showing setting
set laststatus=2 " always showing status bar
set number   " show line index

set relativenumber " show the relative line number

" ---------------------------------------------------------

" Use a line cursor within insert mode and a block cursor everywhere else.
"
" Reference chart of values:
"  Ps = 0 -> blinking block.
"  Ps = 1 -> blinking block (default).
"  Ps = 2 -> steady block.
"  Ps = 3 -> blinking underline.
"  Ps = 4 -> steady underline.
"  Ps = 5 -> blinking bar (xterm).
"  Ps = 6 -> steady bar (xterm).
let &t_SI = "\e[5 q"
let &t_EI = "\e[1 q"



```

