// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import axios from 'axios'
import state from './state.js'
import AMap from 'vue-amap'
import VueScroller from 'vue-scroller'
import {
  parseURL
} from '@/libs/utils.js'
import VueImg from 'v-img'
import Toasted from 'vue-toasted'
import {
  InfiniteScroll
} from 'mint-ui'
import _ from 'lodash'
Vue.use(InfiniteScroll)
const moment = require('moment')
require('moment/locale/zh-cn')
Vue.use(require('vue-moment'), {
  moment
})
// Vue.use(lodash)
Vue.use(Toasted)
Vue.use(VueImg)
Vue.use(AMap)
Vue.use(Vuetify)
Vue.use(Vuex)
Vue.use(VueScroller)
Vue.config.productionTip = false
Vue.toasted.register('default', 'Oops.. Something Went Wrong..', {
  type: 'error',
  icon: 'error_outline'
})
const store = new Vuex.Store(state)
router.beforeEach((to, from, next) => {
  if (to.path.match(/http/) !== null) {
    let toURL = parseURL(to.path.substring(1))
    let thisURL = parseURL(document.URL)
    if (toURL.host !== thisURL.host) {
      next({
        path: '/'
      })
      window.open(to.fullPath.substring(1))
    } else {
      next({
        path: thisURL.path
      })
    }
  }
  if (to.matched.some(record => record.meta.unableBottomNavgation)) {
    next()
    store.commit('hideBottomNavgation')
  } else {
    next()
    store.commit('showBottomNavgation')
  }
})
AMap.initAMapApiLoader({
  key: 'ba598ea13544001f281ce6891dbd259a',
  plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor']
})
axios.interceptors.response.use(function (response) {
  // Do something with response data
  // console.log(response)
  return response
}, function (error) {
  // console.log('err from interceptor', error)
  if (error.response.status === 401) {
    // console.log('401 err', store)
    store.commit('showSnackbar', {
      text: `需要先登录`
    })
    store.commit('showLoginDialog')
  }
  return Promise.reject(error)
})
Vue.prototype.$http = axios
Vue.prototype.$_ = _
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: {
    App
  },
  filters: {
    capitalize: function (value) {
      if (!value) return ''
      value = value.toString()
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
    term: function (value) {
      let map = {
        '1': '秋',
        '2': '冬',
        '3': '春',
        '4': '夏'
      }
      return value.slice(2, 4) + map[value[5]]
    }
  }
})
