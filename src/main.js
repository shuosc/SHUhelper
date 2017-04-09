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
import routes from './router/index.js'

const router = new VueRouter({
  routes
})

FastClick.attach(document.body)

Vue.config.productionTip = false
const store = new Vuex.Store(state)
/* eslint-disable no-new */
Vue.prototype.$http = axios
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app-box')
