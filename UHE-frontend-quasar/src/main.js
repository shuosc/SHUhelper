// === DEFAULT / CUSTOM STYLE ===
// WARNING! always comment out ONE of the two require() calls below.
// 1. use next line to activate CUSTOM STYLE (./src/themes)
// require(`./themes/app.${__THEME}.styl`)
// 2. or, use next line to activate DEFAULT QUASAR STYLE
require(`quasar/dist/quasar.${__THEME}.css`)
// ==============================

// Uncomment the following lines if you need IE11/Edge support
// require(`quasar/dist/quasar.ie`)
// require(`quasar/dist/quasar.ie.${__THEME}.css`)

import Vue from 'vue'
// import Quasar from 'quasar'
import router from './router'
import Quasar, * as All from 'quasar'
import Vuex from 'vuex'
import axios from 'axios'
import state from './states'
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)
axios.interceptors.response.use(
  function(response) {
    // Do something with response data
    // console.log(response)
    return response
  },
  function(error) {
    // console.log('err from interceptor', error)
    if (error.response.status === 401) {
      // console.log('401 err', store)
      // store.commit('showSnackbar', {
      //   text: `需要先登录`
      // })
      // console.log(router.history)
      if (router.history.current.fullPath !== '/login') {
        router.push('/login?redirect=' + router.history.current.fullPath)
      }
      // store.commit('showLoginDialog')
    }
    return Promise.reject(error)
  }
)
Vue.prototype.$http = axios
// ...
Vue.use(Quasar, {
  components: All,
  directives: All
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
if (__THEME === 'mat') {
  require('quasar-extras/roboto-font')
}
import 'quasar-extras/material-icons'
// import 'quasar-extras/ionicons'
// import 'quasar-extras/fontawesome'
// import 'quasar-extras/animate'

Quasar.start(() => {
  /* eslint-disable no-new */
  new Vue({
    el: '#q-app',
    router,
    store,
    render: h => h(require('./App').default)
  })
})
