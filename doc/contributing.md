# Contributing to SHUHelper

## What should I know before I get started?

### 技术栈

#### 语言

#### 前端

前端使用 [Nuxt 框架](https://nuxtjs.org)来进行SSR。

使用 Nuxt 自带的 [Vuex](https://vuex.vuejs.org/zh/) 和 [Axios](https://axios.nuxtjs.org)。

UI框架使用 [Vuetify](https://vuetifyjs.com) 。

除配置文件等完全不包含业务逻辑的代码文件外，应尽可能使用typescript代替javascript。

### 后端

后端使用 [Koa](https://koa.bootcss.com) 框架。

语言全部使用typescript。

服务器使用 [MongoDB](https://www.mongodb.com) 。

使用 [Redis](https://redis.io) 来进行缓存。

## 如何启动开发服务器

### 安装依赖

首先需要安装 [node.js](https://nodejs.org/en/)、[yarn](https://yarnpkg.com)、[MongoDB](https://www.mongodb.com) 和 [Redis](https://redis.io)。

上述依赖的安装请参考互联网上资料和官方文档。

### 启动后端

进入backend文件夹后:

首先用yarn或npm安装所有npm包:
```shell
yarn
```
或
```bash
npm install
```

接着就可以启动了，我们提供了开发服务器启动脚本。

执行

```bash
./script/dev-server.sh
```

即可启动后端开发服务器。

### 启动前端

进入frontend文件夹后:

首先用yarn或npm安装所有npm包:
```shell
yarn
```
或
```bash
npm install
```

接着：

```bash
npm run dev
```

或

```bash
yarn dev
```
即可启动前端。

⚠️：如果安装包时yarn报了有关 upath 和 node 版本的错误，可以先：
```bash
yarn config set ignore-engines true
```
再
```bash
yarn
```
试试。

## Styleguides

### Git使用

#### Git Commit Messages

Commit message的第一行长度不超过30个字

Commit message要表达出这次commit做了什么

Commit message写法参考 [AngularJS Git Commit Message Conventions](https://gist.github.com/stephenparish/9941e89d80e2bc58a153)。


#### Git commit 和 push的时机

如果你能做到这些，那你可以commit and push一次：

- 确保你的代码在你能想到的范围内能够工作
- 确保你能为本次commit写一个有意义的Commit Message
- 在commit前请删去所有注释掉的代码，如果某天你真的需要这些注释掉的代码，你可以用版本控制工具找回。
 
  同理，请不要在commit的代码中包含用于调试的输入输出语句。

#### 当你的代码和线上代码冲突时

使用变基（Rebase）而非合并（Merge）来处理冲突。

## 代码Styleguide

⚠️：你可以拒绝遵守这些规定，但请你在commit了这么做的代码之后，开一个issue来找一个愿意这么做的人来帮你修改你的代码。

如果你发现代码中有不符合这些规定的内容，而不愿意自行修复它，请开一个issue来让我们知道。

### 变量、函数和自定义类型的命名

- 使用小驼峰（eg. camelCase）来为局部变量、类型和函数命名。

- 使用大驼峰（eg. CamelCase）来为导出的自定义类型和函数命名。

- 命名时的自然语言使用英文，**绝对禁止**混用英文和中文拼音。

- 变量名要反应变量代表什么，类似的，类型名要反应类型是什么，函数名要反应函数做了什么。

- 变量、函数和类型的名称尽量保持在9~16个字符之间

  - 除非在“变量是循环索引”或“变量代表数学上的变量”的情况下，否则**绝对禁止**使用单个字符的变量名。
  - 除非是数学上约定好的变量名，否则**绝对禁止**使用仅由数字区别的几个变量名（eg. x1,x2）。

- 为相同的东西取相同的名字，为不同的东西取不同的名字，为相反的东西取相反的名字

  - 一些标准反义词

    | 原义   | 反义     |
    | ------ | -------- |
    | add    | remove   |
    | begin  | end      |
    | create | destory  |
    | first  | last     |
    | insert | delete   |
    | get    | set      |
    | lock   | unlock   |
    | min    | max      |
    | next   | previous |
    | open   | close    |
    | show   | hide     |
    | start  | stop     |
    | up     | down     |

- **如果变量名太长**，请按顺序考虑以下这些方法

  1. 去掉虚词（and、or、the）

  2. 使用标准缩写，一些缩写如下：

       | 全称        | 缩写 |
       | ----------- | ---- |
       | index       | idx  |
       | object      | obj  |
       | document    | doc  |
       | text        | txt  |
       | position    | pos  |
       | information | info |

  3. 去掉所有非前置元音（但保证单词仍然能被拼读出来）（eg. computer -> cmptr，screen -> scrn）

       如果你使用了这一条，请将你使用的缩写添加到上面的标准缩写表中