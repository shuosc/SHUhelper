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
      path: '/login',
      name: 'login',
      component: function (resolve) {
        require(['@/views/Login.vue'], resolve)
      },
      meta: {
        title: '登陆',
        unableBottomNavgation: true
      }
    },
    {
      path: '/external-service/:id',
      name: 'externalService',
      component: function (resolve) {
        require(['@/views/externalService.vue'], resolve)
      },
      meta: {
        title: '外部链接',
        unableBottomNavgation: true
      }
    },
    {
      path: '/the-answer',
      name: 'theAnswer',
      component: function (resolve) {
        require(['@/views/theAnswer.vue'], resolve)
      },
      meta: {
        title: '人生解答书',
        unableBottomNavgation: true
      }
    },
    {
      path: '/sales',
      name: 'sales',
      component: function (resolve) {
        require(['@/views/sales.vue'], resolve)
      },
      meta: {
        title: '售卖记录',
        unableBottomNavgation: true
      }
    },
    {
      path: '/sports',
      name: 'sports',
      component: function (resolve) {
        require(['@/views/sports.vue'], resolve)
      },
      meta: {
        title: '晨跑课外',
        unableBottomNavgation: true
      }
    },
    {
      path: '/phylab',
      name: 'phylab',
      component: function (resolve) {
        require(['@/views/phylab.vue'], resolve)
      },
      meta: {
        title: '物理实验',
        unableBottomNavgation: true
      }
    },
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
        title: '缴费查询',
        unableBottomNavgation: true
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
        title: '日程',
        customToolbar: false
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
