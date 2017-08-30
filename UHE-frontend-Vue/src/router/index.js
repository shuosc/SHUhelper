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
import coursesQuery from '@/views/coursesQuery'
import course from '@/views/course'
import fin from '@/views/fin'
// import map from '../views/map'
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/profile/:id',
      name: 'profile',
      component: profile
    },
    {
      path: '/fin',
      name: 'fin',
      component: fin
    },
    {
      path: '/courses/:id',
      name: 'course',
      component: course,
      meta: {
        unableBottomNavgation: true
      }
    },
    {
      path: '/courses-query',
      name: 'courses',
      component: coursesQuery,
      meta: {
        unableBottomNavgation: true
      }
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
      component: Home,
      meta: {
        disableBack: true
      }
    },
    {
      path: '/square',
      name: 'Square',
      component: Square,
      meta: {
        disableBack: true
      },
      children: [
        {
          path: 'feed-detail/:id',
          component: function (resolve) {
            require(['@/components/dialog/FeedDetail.vue'], resolve)
          },
          meta: {
            dialog: true
          }
        },
        {
          path: 'feed-add-link',
          component: function (resolve) {
            require(['@/components/dialog/AddFeedLink.vue'], resolve)
          },
          meta: {
            dialog: true
          }
        },
        {
          path: 'feed-add-text',
          component: function (resolve) {
            require(['@/components/dialog/AddFeedText.vue'], resolve)
          },
          meta: {
            dialog: true
          }
        },
        {
          path: 'others',
          component: function (resolve) {
            require(['@/views/others.vue'], resolve)
          }
        }
      ]
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
      component: Calendar,
      meta: {
        disableBack: true
      }
    },
    {
      path: '/messages',
      name: 'Messages',
      component: Messages,
      meta: {
        disableBack: true
      }
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
