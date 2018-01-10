<template lang="pug">
  div
    q-card
      q-card-title.text-center
        | SHUhelper V4
      q-card-main
        p.light-paragraph
          | SHUhelper 是设立于15年9月1日的网站，旨在让所有人的生活更加便利。
        //- p
          | 目前，您可以通过有效的校园一卡通和一卡通密码使用本应用的服务，您的数据都经过您的密码加密，您的数据没有泄漏的风险。
        p
          | 目前，有以下几种方法可以使用本网站的服务：
          ul
            li
              | 直接在浏览器中访问 
              span.token
                | shuhelper.cn
            li
              a(href= "https://www.pgyer.com/apiv1/app/install?aId=e7c4929b91486d9f76a6b6790df36f76&_api_key=a6a7ba51429b6968af23b13eec01d815")
                | 安装Android App
            li 
              | iOS 将网站添加到桌面
        p
          | 遇到问题，建议欢迎在广场里发表。
        p
          | 本项目在GPLV3的协议下开放源代码，代码托管在
          a(href="https://github.com/shuopensourcecommunity/SHUhelper")
            | GitHub
        p
          | 欢迎关注我们的微信公众号，微信搜索 
          span.token
            | shuhelper
        p
          small
            | 联系我们: admin@shuhelper.cn
        p.text-center
          img(src="https://forthebadge.com/images/badges/built-with-love.svg")
          br
          small(style='color:grey;')
            | 上海大学开源社区 
            br
            | 2017 SHU OpenSourceCommnuity
            
</template>
<script>
export default {
}
</script>
<style>

</style>
