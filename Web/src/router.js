
/* eslint-disable */
import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

function load(component) {
  // '@' is aliased to src/components
  return () =>
    import (`@/${component}.vue`)
}
import Login from '@/Login'
import Error404 from '@/Error404'
import Profile from '@/Profile'
import Square from '@/Square'
import Apps from '@/Apps'
import Schedule from '@/Schedule'
import Index from '@/Index'
import FeedDetail from '@/FeedDetail'
import CoursesDetail from '@/CoursesDetail'
import Courses from '@/Courses'
import CourseEvaluations from '@/CourseEvaluations'
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
      return {
        x: 0,
        y: 0
      }
    }
  },

  routes: [{
      path: '/',
      redirect: '/index',
      alias: ['index-su', 'home']
    },
    {
      path: '/index',
      component: Index,
      name: 'index',
      meta: {
        title: '首页'
      }
    },
    {
      path: '/login',
      component: Login,
      name: 'login'
    },
    {
      path: '/course-evaluations',
      component: CourseEvaluations,
      name: 'course-evaluations',
      meta: {
        title: '课程评价',
        disableBottom: true,
        back: true
      }
    },
    {
      path: '/courses/:id',
      component: CoursesDetail,
      name: 'course-detail',
      meta: {
        title: '课程',
        disableBottom: true,
        back: true
      }
    },
    {
      path: '/course-query',
      component: Courses,
      name: 'course-query',
      meta: {
        title: '课程',
        disableBottom: true,
        back: true
      }
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
        title: '地图',
        disableBottom: true,
        disableToolbar: true
      } // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/tree-hole',
      name: 'tree-hole',
      component: () =>
        import (`@/TreeHole.vue`),
      meta: {
        title: '树洞',
        disableBottom: true,
        disableToolbar: true
      } // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/news',
      name: 'news',
      component: load('News'),
      meta: {
        title: '新闻',
        disableBottom: true,
        disableToolbar: true
      } // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/love-board',
      name: 'love-board',
      component: load('LoveBoard'),
      meta: {
        title: '表白墙',
        disableBottom: true,
        disableToolbar: true
      } // children: [{ path: '/', component: load('Schedule') }]
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: Profile,
      meta: {
        title: '个人资料',
        disableBottom: true,
        disableToolbar: true
      }
    },
    {
      path: '/feeds/:id',
      name: 'feed',
      component: FeedDetail,
      meta: {
        title: '查看详情',
        disableBottom: true,
        disableToolbar: true
      }
    },
    {
      path: '/apps',
      name: 'apps',
      component: Apps,
      meta: {
        title: '应用'
      }
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
