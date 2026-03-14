---
title: C-CPPLearning
date: 2023-01-03 11:55:54
tags:
    - C/CPP
    - Note
cover: C-CPPLearning.png
description: C/C++ note && data structure, algorithm
---

## Data Type

### Convert

- string to int
  bacause `atoi()` is C base function, and the parameter is char array  
  so firt step is convert `string` to `char[]`, and then..
  - `int num = atoi(str.c_str());`
