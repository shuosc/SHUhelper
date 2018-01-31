
<div  align="center">    
<img src="logo.png" width = "200" height = "200" alt="SHUhelper" align=center />
<h3>SHUhelper</h3>
</div>
<div  align="center">    
<img src="usage.gif" align=center />
</div>

[![flask](http://flask.pocoo.org/static/badges/made-with-flask-s.png)](http://flask.pocoo.org/)
[![codebeat badge](https://codebeat.co/badges/97b9864b-ffc5-497a-a4bd-27d73cc95e46)](https://codebeat.co/projects/github-com-shuopensourcecommunity-shuhelper-master)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![travis ci](https://api.travis-ci.org/shuopensourcecommunity/SHUhelper.svg?branch=master)](https://travis-ci.org/shuopensourcecommunity/SHUhelper)
[![Code Health](https://landscape.io/github/shuopensourcecommunity/SHUhelper/master/landscape.svg?style=flat)](https://landscape.io/github/shuopensourcecommunity/SHUhelper/master)

> 还在开发中呢，写文档是不可能的，这辈子都写不了文档，只能在commit里卖卖萌这样，勉强过过日子

## 简介
    SHUhelper是一个校园服务平台，集成了整合了已有的校园服务和信息，并在此之上提供更多。


## 特色

* 基于web技术，全平台适应
* 下一次push再编好不好

## How to contribute

### 如何拉起前端

首先你需要 yarn，请参照[官方网站](https://yarnpkg.com/zh-Hans/docs/install)安装yarn

然后只需
```shell
make buildweb
make runweb
```
前端就成功拉起了，应该会自动打开浏览器，并启用 auto reload。

### 如何拉起后端

首先你需要在 instance下放置正确的config.py文件。

可以向开发者索要这个文件。

然后：

```shell
make install
# 部分系统需要手动安装flask，如Ubuntu
# 需要 sudo apt install python3-flask
make run
```
后端就拉起了。

## Powered by

* [上海大学验证码识别服务](https://github.com/shuopensourcecommunity/anti-captcha.shuosc.org) by @EnJiang
