---
title: Conquer pyenv install issue _ssl lib missing
date: 2026-03-14 20:37:17
cover: pyenvicon.png
tags: WSL, Issue
---

## Issue occur

wsl
![error](error.png)

loop up pyenv wiki:[ERROR: The Python ssl extension was not compiled. Missing the OpenSSL lib?](https://github.com/pyenv/pyenv/wiki/Common-build-problems#error-the-python-ssl-extension-was-not-compiled-missing-the-openssl-lib)

## Installing OpenSSL

[Installing OpenSSL locally under your username](https://help.dreamhost.com/hc/en-us/articles/360001435926-Installing-OpenSSL-locally-under-your-username)
try `pyenv install 3.10` again

failure!

### Clear appended path from windows:maybe the path ambitious:

[How to remove the Win10's PATH from WSL](https://stackoverflow.com/questions/51336147/how-to-remove-the-win10s-path-from-wsl)

```bash
# add this two line below to /etc/wsl.conf
[interop]
appendWindowsPath = false

# in cmd, to restart wsl and apply that config
wsl.exe --shutdown
```

try `pyenv install 3.10`
![install succeed](fixed.png)
