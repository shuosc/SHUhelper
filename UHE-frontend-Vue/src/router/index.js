import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home'
import Square from '../views/Square'
import Calendar from '../views/Calendar'
import Messages from '../views/Messages'
import Conversation from '../views/Conversation'
import Apps from '../views/Apps'
import My from '../views/My'
import profile from '../views/profile'
import map from '../views/map'
// import map from '../views/map'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/profile/:id',
      name: 'profile',
      component: profile
    },
    {
      path: '/map',
      name: 'map',
      component: map,
      meta: {
        unableBottomNavgation: true
      }
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/square',
      name: 'Square',
      component: Square
    }, {
      path: '/security-map',
      name: 'security-map',
      component: function (resolve) {
        require(['@/views/AMap.vue'], resolve)
      },
      meta: {
        keepAlive: false,
        unableBottomNavgation: true
      }
    },
    {
      path: '/Calendar',
      name: 'Calendar',
      component: Calendar
    },
    {
      path: '/messages',
      name: 'Messages',
      component: Messages
    },
    {
      path: '/conversation/:id',
      name: 'Conversation',
      component: Conversation,
      meta: {
        unableBottomNavgation: true
      }
    },
    {
      path: '/apps',
      name: 'Apps',
      component: Apps
    },
    {
      path: '/my',
      name: 'My',
      component: My
    }
  ]
})
