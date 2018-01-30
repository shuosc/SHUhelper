<template lang="pug">
  div
    blockquote(style="margin:1rem;")
      small
        | 这里是一些常用的功能，网站的集合。
    //- <q-search v-model="search" />
    q-card.no-margin(dense v-for="group in appsGroup" :key="group.name")
      q-card-title {{group.name}}
      q-card-separator
      q-card-main
        blockquote(v-if="group.detail")
          small
            | {{group.detail}}
        .row.flex
          q-item.col-3.text-center(dense multiline v-for="app in group.apps" @click="onAppClick(app)" :key="app.name")
            q-item-main
              q-item-tile(label)
                q-icon(:name="app.icon" style="font-size: 1.6rem" color="primary")
              q-item-tile(style="font-size:0.7rem;" sublabel)
                | {{app.name}}
    q-modal(minimized v-model="modal")
      q-card.no-margin
        q-card-title 提示
        q-card-main 
          | 您正在前往
          span.token
            | {{app.name}}
          br
          | {{app.detail}}
          br
          | 网址是
          span.token
            | {{app.url}}
          br
          | 点击确认继续
          br
          | 提示：android app中暂时无法打开网页，请手动复制网址到浏览器
        q-card-actions.no-padding.no-margin.row.flex.text-center.justify-center
          q-btn.col-6.no-margin(flat @click="modal=false") 取消
          q-btn.col-6.no-margin(flat) 确定

</template>

<script>
import { Dialog, openURL } from 'quasar'
export default {
  data() {
    return {
      modal: false,
      app: {
        name: '',
        detail: '',
        url: ''
      },
      appsGroup: [
        {
          name: 'helper提供的服务',
          detail: '',
          apps: [
            // { name: '我的宿舍', icon: 'bubble_chart', url: '/info' },
            // { name: '一卡通余额', icon: 'bubble_chart', url: '/info' },
            // {
            //   name: '空教室',
            //   icon: 'fa-xiangtongfangjianrenwu',
            //   url: '/empty-room'
            // },
            // { name: '体育活动', icon: 'bubble_chart', url: '/info' },
            { name: '校园地图', icon: 'fa-map-o', url: '/map' },
            // { name: '快速链接', icon: 'bubble_chart', url: '/info' },
            { name: '课程搜索', icon: 'fa-book', url: '/course-query' },
            { name: '评课社区', icon: 'fa-book', url: '/course-evaluations' },
            { name: '选课管理（测试）', icon: 'fa-book', url: '/course-manage' },
            // { name: '学生财务', icon: 'fa-money', url: '/fin' },
            // { name: '校车运行', icon: 'fa-bus', url: '/bus' },
            // { name: '晨跑课外', icon: 'fa-tiyujiankang', url: '/sports' },
            // { name: '物理实验', icon: 'fa-07', url: '/phylab' },
            // { name: '校历', icon: 'fa-rili', url: '/school-cal' },
            // { name: '就医指导', icon: 'fa-yiyuan', url: '/med' },
            // { name: '人生解答书', icon: 'fa-key', url: '/the-answer' },
            {
              name: '尔美订餐',
              icon: 'fa-dppj',
              detail: '在这里你可以预定尔美二楼西餐厅的中饭和晚饭',
              external: true,
              url: 'http://ermei.shuhelper.cn/'
            },
            {
              name: '排课助手',
              icon: 'fa-paw',
              detail:
                '在这里你可以给自己排出一份合理的课表，该服务由SHUhelper提供',
              external: true,
              url: 'http://xk.shuhelper.cn/'
            }
          ]
        },
        {
          name: '校内服务',
          detail: '有些服务需要校园网方可访问',
          apps: [
            {
              name: 'PIM系统',
              icon: 'PIM',
              detail: '一些常用事务的流程需要在这里进行',
              external: true,
              url: 'http://pim.shu.edu.cn/'
            },
            {
              name: '研习空间',
              icon: 'fa-fangjian',
              detail: '图书馆的研习空间预约系统，由图书馆提供',
              external: true,
              url:
                'http://room-booking.lib.shu.edu.cn/ClientWeb/xcus/ic2/Default.aspx'
            },
            {
              name: '孰知网',
              detail: '新版成就系统，在这里你可以参加课外活动，以及更多',
              icon: 'SZ',
              external: true,
              url: 'http://www.sz.shu.edu.cn'
            },
            {
              name: '选课系统(冬)',
              icon: 'XK',
              external: true,
              detail: '冬季学期选课系统',
              url: 'http://xk.shu.edu.cn'
            },
            {
              name: '选课系统(春)',
              detail: '春季学期选课系统',
              icon: 'XK',
              external: true,
              url: 'http://xk.shu.edu.cn:8080'
            },
            {
              name: '教务系统',
              icon: 'CJ',
              detail: '教务管理系统，查成绩什么的',
              external: true,
              url: 'http://cj.shu.edu.cn'
            },
            {
              name: '微软软件',
              icon: 'MS',
              detail: '校园正版系统，office下载',
              external: true,
              url: 'ftp://msftp.shu.edu.cn'
            },
            {
              name: '校园邮箱',
              icon: 'MAIL',
              detail: '校园邮箱',
              external: true,
              url: 'http://mail.shu.edu.cn/'
            }
          ]
        },
        {
          name: '开源社区',
          detail: '',
          apps: [
            {
              name: 'SHUer.link',
              external: true,
              detail: '面对上大师生的导航网站',
              icon: 'fa-iosnavigate',
              url: 'https://shuer.link/'
            },
            {
              name: '开源镜像',
              external: true,
              detail: '开源社区维护的上海大学开源镜像站',
              icon: 'M',
              url: 'https://mirrors.shuosc.org/'
            }
          ]
        },
        {
          name: '校外网站',
          detail: '',
          apps: [
            {
              name: '中国知网',
              icon: 'CNKI',
              external: true,
              detail: '查阅，下载论文',
              url: 'http://cnki.net'
            }
          ]
        }
      ]
    }
  },
  methods: {
    onAppClick(app) {
      if (app.external) {
        this.app = app
        // this.modal = true
        Dialog.create({
          title: '提示',
          message: `你正在前往${app.name}<br/><br/>${app.url}<br/><br/>${
            app.detail
          }<br/><br/>点击确认将在新网页中打开${app.name}<br/><br/>提示：android app中暂时无法打开网页，请手动复制网址到浏览器`,
          buttons: [
            '取消',
            {
              label: '确定',
              handler() {
                openURL(app.url)
              }
            }
          ]
        })
      } else {
        this.$router.push(app.url)
      }
    }
  }
}
</script>

<style>

</style>
