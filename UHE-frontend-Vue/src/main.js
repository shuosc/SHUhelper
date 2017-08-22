// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import axios from 'axios'
import state from './state.js'
import moment from 'moment'
import VueMomentJS from 'vue-momentjs'
import AMap from 'vue-amap'
import VueScroller from 'vue-scroller'
import {
  parseURL
} from './utils.js'
import VueImg from 'v-img'
import Toasted from 'vue-toasted'

Vue.use(Toasted)
Vue.use(VueImg)
moment.locale('zh-cn')
Vue.use(AMap)
Vue.use(VueMomentJS, moment)
Vue.use(Vuetify)
Vue.use(Vuex)
Vue.use(VueScroller)
// Vue.use(VueRouter)
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
    store.commit('hideBottomNavgation')
    next()
  } else {
    next()
    store.commit('showBottomNavgation')
  }
})
AMap.initAMapApiLoader({
  key: 'ba598ea13544001f281ce6891dbd259a',
  plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor']
})
Vue.prototype.$http = axios
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: {
    App
  }
})
