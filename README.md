# 大学助手引擎 University Helper Engine(UHE)

## 简介

此项目致力于构建一套开源的校园门户系统，解决大多数校园都存在的信息接口碎片化问题，并通过丰富的插件系统提供多样化的订制功能。

## 功能
 
目前有如下功能

* 校园信息流

* 校历

* 课表

* 私信，通知

* 插件系统

* 动态信息

## 依赖

## 预览

![](/doc/screenshot1.jpg)
![](/doc/screenshot2.jpg)
![](/doc/screenshot3.jpg)
![](/doc/screenshot4.jpg)

## 技术架构

UHE采用前后端分离的思路开发。

后端使用主要使用flask框架开发，数据库采用了MongoDB，此外还需要用到Celery以及Redis。后端代码位于`/UHE`

前端分为Web（Vue.JS）端，Android端和iOS端。目前着重开发Web端，Android端简单地使用一个webview来实现，iOS端在计划中，将来可能考虑用weex或native重写。代码目录分别是`/UHE-frontend-Vue`,`/Android`

## 开发环境搭建

### 后端

请查看 `/UHE/README.md`

### 前端-Web

请查看 `/UHE-frontend-Vue/README.md`


## 部署

## 插件

## 贡献


## Powered by

* [上海大学验证码识别服务](https://github.com/shuopensourcecommunity/anti-captcha.shuosc.org) by @EnJiang
