
<div  align="center">    
<img src="logo.png" width = "200" height = "200" alt="SHUhelper" align=center />
<h3>SHUhelper[WIP]</h3>
</div>
<div  align="center">    
<img src="usage.gif" align=center />
</div>

[![flask](http://flask.pocoo.org/static/badges/made-with-flask-s.png)](http://flask.pocoo.org/)
[![codebeat badge](https://codebeat.co/badges/97b9864b-ffc5-497a-a4bd-27d73cc95e46)](https://codebeat.co/projects/github-com-shuopensourcecommunity-shuhelper-master)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![travis ci](https://api.travis-ci.org/shuopensourcecommunity/SHUhelper.svg?branch=master)](https://travis-ci.org/shuopensourcecommunity/SHUhelper)
[![Code Health](https://landscape.io/github/shuopensourcecommunity/SHUhelper/master/landscape.svg?style=flat)](https://landscape.io/github/shuopensourcecommunity/SHUhelper/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/a73c427338c8d7add064/maintainability)](https://codeclimate.com/github/shuopensourcecommunity/SHUhelper/maintainability)

> 还在开发中呢，写文档是不可能的，这辈子都写不了文档，只能在commit里卖卖萌这样，勉强过过日子

## 简介
    SHUhelper是一个校园服务平台，集成了整合了已有的校园服务和信息，并在此之上提供更多。

## 目标

* 收集并整合常用校园公共信息，并且使其易于搜索和使用
* 提供校园内的公共社区平台，一定程度上解决信息交流，发布，查询，公告的问题
* 通过各种方式整合校园API，在师生个人层面上实现一站式的校园服务。如：课程表，成绩管理，财务查询，社区管理等
* 努力实现通用化，在实现SHUhelper的同时抽取高层逻辑以方便其他高校移植，参考或复用

## 目前实现的功能

* 校车时刻表（带计时，搜索）
* 评课社区及课程搜索
* 选课管理（查看选课排名，选课，退课）
* 校园广场（动态信息发布，评论，树洞，表白墙）
* 课程表（抓取教务信息实现）
* 物理实验选课查询
* 学费缴费查询
* 校历查看
* 校园地图
* 空教室查询
* 晨跑课外活动查询
* 课外活动表
* 校园导航
* 校园新闻

## 工作中的功能

* 校园二手
* 校园失物招领
* 全功能校园日历
* 校园日历在线ical
* 全站消息推送
* 微信后台管理

## 发展规划

我们希望未来能够通过SHUhelper打造一套成熟的校园应用框架，但是现在离这个目标还相去甚远，在这个过程中也许需要您的帮助。

如果您也在开发类似的应用，也希望SHUhelper的经验能给您带来一定的帮助。

同时，如果您有任何期望，建议，或者需要同开发者交流，欢迎在issues中提出，或者直接联系[上海大学开源社区](https://osc.shu.edu.cn)。

## How to contribute

### 如何拉起前端

首先你需要 yarn，请参照[官方网站](https://yarnpkg.com/zh-Hans/docs/install)安装yarn

然后只需
```shell
make runweb
```
前端就成功拉起了，应该会自动打开浏览器，并启用 auto reload。

### 如何拉起后端

首先，需要安装并且启动 mongodb 和 redis。你可以在他们的官方网站找到更多信息。

然后需要在 instance 下创建一个 config.py 文件，将 sample_config.py 里的内容粘贴到 config.py，并且按照你自己的服务器配置填写好内容。

然后：

```shell
make install
# 部分系统需要手动安装flask，如Ubuntu
# 需要 sudo apt install python3-flask
make dev
```
后端就拉起了。

## Powered by

* [上海大学验证码识别服务](https://github.com/shuopensourcecommunity/anti-captcha.shuosc.org) by @EnJiang
