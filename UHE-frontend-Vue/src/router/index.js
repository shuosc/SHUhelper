import Vue from 'vue'
import Router from 'vue-router'
import Home from '../views/Home'
// import Square from '../views/Square'
const Calendar = () => import('../views/Calendar')
const Messages = () => import('../views/Messages')
const Conversation = () => import('../views/Conversation')
const Apps = () => import('../views/Apps')
const My = () => import('../views/My')
const profile = () => import('../views/profile')
const map = () => import('../views/map')
const coursesQuery = () => import('@/views/coursesQuery')
const course = () => import('@/views/course')
const fin = () => import('@/views/fin')
const TimeLine = () => import('@/views/feed/TimeLine')
const replaceAvatar = () => import('@/views/replaceAvatar')
const emptyRoom = () => import('@/views/emptyRoom')
import bus from '@/views/bus'
import schoolCal from '@/views/schoolCal'
import med from '@/views/med'
// import map from '../views/map'
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/empty-room',
      name: 'emptyRoom',
      component: emptyRoom,
      meta: {
        title: '空教室',
        unableBottomNavgation: true
      }
    },
    {
      path: '/replace-avatar',
      name: 'replaceAvatar',
      component: replaceAvatar,
      meta: {
        title: '更改头像',
        unableBottomNavgation: true
      }
    },
    {
      path: '/med',
      name: 'med',
      component: med,
      meta: {
        title: '就医指导',
        unableBottomNavgation: true
      }
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: profile,
      meta: {
        title: '个人资料'
      }
    },
    {
      path: '/school-cal',
      name: 'schoolCal',
      component: schoolCal,
      meta: {
        title: '17-18校历',
        unableBottomNavgation: true
      }
    },
    {
      path: '/bus',
      name: 'bus',
      component: bus,
      meta: {
        title: '校车运行',
        unableBottomNavgation: true
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
      path: '/feed-add-link',
      component: function (resolve) {
        require(['@/components/dialog/AddFeedLink.vue'], resolve)
      },
      meta: {
        dialog: true,
        unableBottomNavgation: true
      }
    },
    {
      path: '/feed-add-text',
      component: function (resolve) {
        require(['@/components/dialog/AddFeedText.vue'], resolve)
      },
      meta: {
        dialog: true,
        unableBottomNavgation: true
      }
    },
    {
      path: '/feed-detail/:id',
      component: function (resolve) {
        require(['@/components/dialog/FeedDetail.vue'], resolve)
      },
      name: 'feedDetail',
      meta: {
        dialog: true,
        unableBottomNavgation: true
      }
    },
    {
      path: '/square',
      name: 'Square',
      component: TimeLine,
      meta: {
        disableBack: true,
        title: '广场',
        keepAlive: true
      },
      children: [
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
  ],
  scrollBehavior (to, from, savedPosition) {
    console.log(savedPosition)
    if (savedPosition) {
      return savedPosition
    } else {
      return { x: 0, y: 0 }
    }
  }
})
