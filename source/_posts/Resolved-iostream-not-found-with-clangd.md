---
title: Resolved iostream not found with clangd
date: 2026-03-15 18:41:32
cover: clangd.svg
tags: C++, Envirenment
category: Issues Solved
---

## Think about it

Couldn't found means, the c++ lib didn't in user path or in clangd reachable path.

### Try 1 add c++ path to system

`export CPLUS_INCLUDE_PATH="/usr/include/x86_64-linux-gnu/c++/11"`, if didn't have that library, then use these command below

```bash
sudo apt update
sudo apt install libstdc++-<specific version you want>-dev
```

Obviously, it didn't work

### Try 2 add clang configuration

Create a `.clangd` file in project directory, and then add

```.clangd
CompileFlags:
# -isystem: Used to point to system headers (like iostream issue). Using -isystem tells the compiler to treat the directory as a system include, which often suppresses unnecessary warnings from those files.
  Add: [
    "-isystem/usr/include/x86_64-linux-gnu/c++/11"
  ]
```

Enjoy c++ coding~
