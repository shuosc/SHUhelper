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
      component: profile,
      meta: {
        title: ''
      }
    },
    {
      path: '/fin',
      name: 'fin',
      component: fin,
      meta: {
        title: '缴费查询'
      }
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
        unableBottomNavgation: true,
        title: '课程查询'
      }
    },
    {
      path: '/map',
      name: 'map',
      component: map,
      meta: {
        unableBottomNavgation: true,
        title: '校园地图'
      }
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        disableBack: true,
        title: '首页'
      }
    },
    {
      path: '/square',
      name: 'Square',
      component: Square,
      meta: {
        disableBack: true,
        title: '广场'
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
        unableBottomNavgation: true,
        title: '安全地图'
      }
    },
    {
      path: '/Calendar',
      name: 'Calendar',
      component: Calendar,
      meta: {
        disableBack: true,
        title: '日程'
      }
    },
    {
      path: '/messages',
      name: 'Messages',
      component: Messages,
      meta: {
        disableBack: true,
        title: '消息'
      }
    },
    {
      path: '/conversation/:id',
      name: 'Conversation',
      component: Conversation,
      meta: {
        unableBottomNavgation: true,
        title: '对话'
      }
    },
    {
      path: '/apps',
      name: 'Apps',
      component: Apps,
      meta: {
        unableBottomNavgation: true,
        title: '全部功能'
      }
    },
    {
      path: '/my',
      name: 'My',
      component: My
    }
  ]
})
