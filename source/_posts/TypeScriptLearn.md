---
title: TypeScriptLearn
date: 2022-12-29 08:01:58
cover: TypeScriptLearn.png
tags:
    - TypeScript
    - Note
description: TypeScript learning note
---

## Describe

[TypeScript 简介](https://cloud.tencent.com/developer/article/1188631)  

## Independency

- run TS file in vs-code
  1. set-up packages
     `npm install -g typescript`
     `npm install -g ts-node`
  2. set-up code runner plug-in
  3. press play and enjoy it

## Grammer

- **关键字** 下面语句会被赋值为什么类型？
  `const fullName: string = 'Dylan Israel';`
  1. Implicit ×
  2. Explicit √
  > 参考：[typescript-type-inference](https://www.schibsted.pl/blog/typescript-type-inference/)
- **配置** `noImplicitAny` 可以通过启用编译器选项来禁用隐式变量类型赋值
  TODO figure out:
  autoTypeAssignment = FALSE
  noAutoType
  Implicit = FALSE
- **类型**
  [继承和原型：Inheritance & prototype](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)  
  - `unknown` 类似于 ‘any’，但在不确定类型时更安全。
    TODO figure out:
    similar
    never
    unknown
  - keyof 关键字可以与索引名一起使用来提取索引类型
  - ~~不能~~可以为泛型分配默认值
  - 以下代码参数的类型是什么？
    `function ex(param1?: string){}`
    -`unknown`
    -`string | null` ~理解：null不是类型，是一个变量的状态~
    -`string`
    -`string | undefined` √
- **类型别名**通常与 `Strings` 类型一起使用
- **接口**类似于类型别名，但仅适用于对象类型
- **枚举**的两种类型是 `String` 与 `Number`
- Definitely Typed 是最受欢迎的声明文件存储库
  TypeScript 的正式名称
  是使类型动态化的项目~(感觉这描述有问题)~
  - JavaScript 是*类型动态化*的语言：类型动态化指的是只有在~~运行~~编译时才可以确定变量的数据类型
  TypeScript 的超集 ×?
  - TypeScript 是 JavaScript 的超集
- **面向对象特性**
  - 设置 protected 修饰符的属性和方法只允许在继承的类中使用？ ×
    还可以在当前类使用
  - `override` 指内容重写，外壳相同，
    `overload` 指参数列表(参数类型、个数、返回类型)不同
    > 参考： [override & overload](https://www.runoob.com/java/java-override-overload.html)

## Test

- TODO:
  - vs code for ts check is too strict: how to modified to `use strict` mode?
  - 隐式转换除了 `==`、`!!`也会出现在使用索引取数组元素嘛？
    `arr[10] = 0`
    `arr['1'] = 2` <--here
    `alert(arr[1])` // equal 2

## Issue

['this' implicitly has type 'any' error in TypeScript #](https://bobbyhadz.com/blog/typescript-this-implicitly-has-type-any)

## Code Formatting

[编写高质量可维护的代码：Awesome TypeScript](https://mp.weixin.qq.com/s?__biz=Mzg3NTcwMTUzNA==&mid=2247486311&idx=1&sn=e673c558cde252bcd3357074fbf0a365&source=41)
