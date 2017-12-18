import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// function load(component) {
//   // '@' is aliased to src/components
//   return () => import(`@/${component}.vue`)
// }
import Login from '@/Login'
import Error404 from '@/Error404'
import Profile from '@/Profile'
import Square from '@/Square'
import Apps from '@/Apps'
import Schedule from '@/Schedule'
import Index from '@/Index'
export default new VueRouter({
  /*
   * NOTE! VueRouter "history" mode DOESN'T works for Cordova builds,
   * it is only to be used only for websites.
   *
   * If you decide to go with "history" mode, please also open /config/index.js
   * and set "build.publicPath" to something other than an empty string.
   * Example: '/' instead of current ''
   *
   * If switching back to default "hash" mode, don't forget to set the
   * build publicPath back to '' so Cordova builds work again.
   */

  mode: 'history',
  scrollBehavior: () => ({ y: 0 }),

  routes: [
    {
      path: '/login',
      component: Login
      // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/square',
      component: Square // children: [{ path: '/', component: load('Schedule') }]
    },

    {
      path: '/profile/:id',
      name: 'profile',
      component: Profile,
      meta: {
        title: '个人资料'
      }
    },
    {
      path: '/apps',
      component: Apps
      // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/schedule',
      component: Schedule
      // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/',
      component: Index,
      alias: '/index'
    },
    // Always leave this last one
    { path: '*', component: Error404 } // Not found
  ]
})
