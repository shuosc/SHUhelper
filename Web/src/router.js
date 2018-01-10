import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

function load(component) {
  // '@' is aliased to src/components
  return () => import(`@/${component}.vue`)
}
import Login from '@/Login'
import Error404 from '@/Error404'
import Profile from '@/Profile'
import Square from '@/Square'
import Apps from '@/Apps'
import Schedule from '@/Schedule'
import Index from '@/Index'
// import Map from '@/Map'
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
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { x: 0, y: 0 }
    }
  },

  routes: [
    {
      path: '/login',
      component: Login,
      name: 'login'
    },
    {
      path: '/2018',
      component: load('NewYearWish'),
      name: 'NewYearWish',
      meta: {
        disableLayout: true
      }
    },
    {
      path: '/square',
      name: 'square',
      component: Square,
      meta: {
        title: '广场'
      }
    },
    {
      path: '/map',
      name: 'map',
      component: load('Map'),
      meta: {
        title: '地图'
      } // children: [{ path: '/', component: load('Schedule') }]
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
      name: 'apps',
      component: Apps
      // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/schedule',
      component: Schedule,
      name: 'schedule',
      meta: {
        title: '日程'
      }
      // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/about',
      component: load('About'),
      name: 'about',
      meta: {
        title: '关于'
      }
    },
    {
      path: '/',
      redirect: '/index'
    },
    {
      path: '/index',
      component: Index,
      alias: ['index-su', 'home'],
      name: 'index',
      meta: {
        title: '首页'
      }
    },
    // Always leave this last one
    {
      path: '*',
      component: Error404,
      name: '404',
      meta: {
        title: '404'
      }
    } // Not found
  ]
})
