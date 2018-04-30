/* eslint-disable */
import Vue from 'vue'
import App from './App'
import store from './store'
// var Fly = require('flyio/dist/npm/wx')
import {
  http
} from './http'
Vue.prototype.$http = http
Vue.prototype.$store = store
Vue.prototype.$user = {
  name: '',
  ID: '',
  pw: '',
  authID: ''
}

Vue.config.productionTip = false
App.mpType = 'app'

const app = new Vue(App)
app.$mount()

export default {
  // 这个字段走 app.json
  config: {
    // 页面前带有 ^ 符号的，会被编译成首页，其他页面可以选填，我们会自动把 webpack entry 里面的入口页面加进去
    pages: ['pages/logs/main', '^pages/index/main', 'pages/login/main', 'pages/me/main'],
    window: {
      backgroundTextStyle: 'dark',
      // navigationBarBackgroundColor: '#03A9F4',
      // navigationBarBackgroundColor: '#33B5E5',
      navigationBarBackgroundColor: '#85B7D8',
      navigationBarTitleText: 'SHUhelper',
      navigationBarTextStyle: 'white'
    },
    // tabBar: {
    //   // position: "top",
    //   list: [{
    //     pagePath: "pages/index/main",
    //     iconPath: "static/calendar-normal.png",
    //     selectedIconPath: "static/calendar-selected.png",
    //     text: "课表"
    //   }, {
    //     pagePath: "pages/me/main",
    //     iconPath: "static/home-normal.png",
    //     selectedIconPath: "static/home-selected.png",
    //     text: "我的"
    //   }]
    // },
  }
}
