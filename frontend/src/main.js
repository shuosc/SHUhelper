// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import FastClick from 'fastclick'
import VueRouter from 'vue-router'
import App from './App'
import Vuex from 'vuex'
import { WechatPlugin, AlertPlugin, LoadingPlugin, ConfirmPlugin, ToastPlugin } from 'vux'
import axios from 'axios'
import state from './state.js'
import AMap from 'vue-amap'
// import Home from './components/HelloFromVux'
// import routes from './router/index.js'

Vue.use(WechatPlugin)
Vue.use(ToastPlugin)
// Vue.use(AjaxPlugin)
Vue.use(AlertPlugin)
Vue.use(LoadingPlugin)
Vue.use(ConfirmPlugin)
Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(AMap)

import routes from './router/index.js'

const router = new VueRouter({
  mode: 'history',
  routes
  // scrollBehavior (to, from, savedPosition) {
  //   console.log(to.path)
  //   if (to.path === '/') {
  //     document.getElementById('vux_view_box_body').scrollTop = 0
  //     return { x: 0, y: 0 }
  //   } else {
  //     console.log(savedPosition)
  //     return savedPosition
  //   }
  // }
})

AMap.initAMapApiLoader({
  key: 'ba598ea13544001f281ce6891dbd259a',
  plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor']
})

FastClick.attach(document.body)

/* eslint-disable no-undef */
router.beforeEach((to, from, next) => {
  _hmt.push(['_trackPageview', to.path])
  if (document.getElementById('vux_view_box_body') != null) {
    // if (from.path === '/') {
    //   console.log(from, to)
    //   if (to.path === '/woods-hole') {
    //     // document.getElementById('xs-container').style.Transform = 'translateY(0px)'
    //   }
    // }
    if (to.path === '/' || to.name === 'query') {
      document.getElementById('vux_view_box_body').scrollTop = 0
    }
  }
  next()
})

Vue.config.productionTip = false
const store = new Vuex.Store(state)
/* eslint-disable no-new */
Vue.prototype.$http = axios
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app-box')
