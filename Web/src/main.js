/* eslint-disable */
// === DEFAULT / CUSTOM STYLE ===
// WARNING! always comment out ONE of the two require() calls below.
// 1. use next line to activate CUSTOM STYLE (./src/themes)
require(`./themes/app.${__THEME}.styl`)
// 2. or, use next line to activate DEFAULT QUASAR STYLE
// require(`quasar/dist/quasar.${__THEME}.css`)
// ==============================

// Uncomment the following lines if you need IE11/Edge support
// require(`quasar/dist/quasar.ie`)
// require(`quasar/dist/quasar.ie.${__THEME}.css`)

import Vue from 'vue'
// import Quasar from 'quasar'
import router from './router'
import Vuex from 'vuex'
import axios from 'axios'
import state from './states'
import Vuelidate from 'vuelidate'
import Navigation from 'libs/Nav'
import VueAMap from 'vue-amap'
import ga from 'libs/analytics.js'
import FastClick from 'fastclick'
// import PullTo from 'vue-pull-to'
import Quasar, {
  Toast,
  QBtn,
  QIcon,
  QList,
  QItem,
  QItemSide,
  QLayout,
  QToolbar,
  QToolbarTitle,
  QCard,
  QCardMain,
  QCardActions,
  QCardTitle,
  QCardSeparator,
  QItemMain,
  QSideLink,
  QTransition,
  QCollapsible,
  QItemTile,
  QSelect,
  QModal,
  QModalLayout,
  QPullToRefresh,
  QInfiniteScroll,
  QSpinnerDots,
  QFixedPosition,
  QField,
  BackToTop,
  QListHeader,
  GoBack,
  QItemSeparator
} from 'quasar'
if (__THEME === 'mat') {
  require('quasar-extras/roboto-font')
}
import 'quasar-extras/material-icons'
// import 'quasar-extras/ionicons'
// import 'quasar-extras/fontawesome'
import 'quasar-extras/animate'
import {
  Field
} from 'mint-ui'

Vue.component(Field.name, Field)
// Vue.use(PullTo)
Vue.use(Vuelidate)

Vue.use(VueAMap)
VueAMap.initAMapApiLoader({
  key: 'ad8f18c4339cb057e3290e15c0bf3ce7',
  plugin: ['AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.Geolocation', 'AMap.ControlBar'],
  uiVersion: '1.0'
})
Vue.prototype.$map = VueAMap

FastClick.attach(document.body)

Vue.use(Quasar, {
  components: {
    QBtn,
    QModal,
    QModalLayout,
    QTransition,
    QCardSeparator,
    QIcon,
    QList,
    QItemSide,
    QItemTile,
    QItem,
    QToolbar,
    QLayout,
    QSelect,
    QCollapsible,
    QCard,
    QCardTitle,
    QToolbarTitle,
    QCardMain,
    QCardActions,
    QItemMain,
    QSideLink,
    QPullToRefresh,
    QInfiniteScroll,
    QSpinnerDots,
    QFixedPosition,
    QField,
    QListHeader,
    QItemSeparator
  },
  directives: {
    BackToTop,
    GoBack
  }
})

router.beforeEach((to, from, next) => {
  // console.log(to, from)
  next()
  // console.log(history)
})

router.afterEach((to, from) => {
  ga.logPage(to.path, to.name, 'UA-111372547-1')
  // console.log(history)
})


Vue.use(Vuex)
const store = new Vuex.Store(state)
Vue.config.productionTip = false
// Vue.use(Quasar) // Install Quasar Framework
Vue.prototype.$UHE = {
  version: 0.1,
  appName: 'SHUhelper',
  schoolName: '上海大学'
}

Vue.use(Navigation, { router, store })

const moment = require('moment')
require('moment/locale/zh-cn')
Vue.use(require('vue-moment'), {
  moment
})


var instance = axios
if (PROD) {
  instance = axios.create({
    baseURL: 'https://www.shuhelper.cn/',
    timeout: 30000
    // headers: { 'X-Custom-Header': 'foobar' }
  })
}
Vue.directive('back', {
  bind: function (el, binding, vnode) {
    el.onclick = function () {
      if (history.length > 1) {
        router.go(-1)
      } else {
        router.push('/index')
      }
    }
  }
})
instance.interceptors.response.use(
  function (response) {
    return response
  },
  function (error) {
    if (error.response.status === 401) {
      Toast.create(`需要先登录`)
      if (router.history.current.fullPath !== '/login') {
        router.push('/login?redirect=' + router.history.current.fullPath)
      }
    }
    return Promise.reject(error)
  }
)
Vue.prototype.$http = instance

Vue.filter('two_digits', value => {
  if (value < 0) {
    return '00'
  }
  if (value.toString().length <= 1) {
    return `0${value}`
  }
  return value
})


Vue.filter('cnNum', function (value) {
  value = value.toString()
  let map = {
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
    '7': '七',
    '8': '八',
    '9': '九'
  }
  return map[value]
})
Vue.filter('term', function (value) {
  let map = {
    '1': '秋',
    '2': '冬',
    '3': '春',
    '4': '夏'
  }
  value = value.toString()
  // console.log(value)
  let year = parseInt(value.slice(2, 4))
  // console.log(year)
  // console.log(map[value[5]])
  return `${year}-${year + 1}${map[value[5]]}`
})

Quasar.start(() => {
  /* eslint-disable no-new */
  new Vue({
    el: '#q-app',
    router,
    store,
    render: h => h(require('./App').default)
  })
})
