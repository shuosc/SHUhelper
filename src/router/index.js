import Vue from 'vue'
import Router from 'vue-router'
// import Hello from '@/components/Hello'
import Functions from '@/views/functions'
import My from '@/views/My'
import Map from '@/views/Map'
import Frame from '@/views/Frame'
import QueryTemplate from '@/views/QueryTemplate'
import ServiceFrame from '@/views/ServiceFrame'
import Messageboard from '@/views/Messageboard'
import Classrooms from '@/views/Classrooms'
import Courses from '@/views/Courses'
import WoodsHole from '@/views/WoodsHole'
import WoodsHoleSingle from '@/views/WoodsHoleSingle'
// import AMap from '@/views/AMap'
Vue.use(Router)

const routes = [{
  path: '/',
  component: Functions,
  meta: {
    keepAlive: false
  }
}, {
  path: '/my',
  component: My,
  meta: {
    keepAlive: false
  }
}, {
  path: '/map',
  component: Map,
  meta: {
    keepAlive: false
  }
}, {
  path: '/frame/:name',
  component: Frame,
  meta: {
    keepAlive: false
  }
}, {
  path: '/service-frame/:name',
  component: ServiceFrame,
  meta: {
    keepAlive: false
  }
}, {
  path: '/query/:name',
  name: 'query',
  component: QueryTemplate,
  meta: {
    keepAlive: false
  }
}, {
  path: '/messageboard',
  component: Messageboard,
  meta: {
    keepAlive: false
  }
}, {
  path: '/classrooms',
  component: Classrooms,
  meta: {
    keepAlive: false
  }
}, {
  path: '/courses',
  component: Courses,
  meta: {
    keepAlive: false
  }
}, {
  path: '/findfreetime',
  component: function (resolve) {
    require(['@/views/FindFreeTime.vue'], resolve)
  },
  meta: {
    keepAlive: false
  }
}, {
  path: '/index-su',
  component: function (resolve) {
    require(['@/views/SUIndex.vue'], resolve)
  },
  meta: {
    keepAlive: false
  }
}, {
  path: '/woods-hole',
  name: 'woodshole',
  component: WoodsHole,
  meta: {
    keepAlive: true
  }
}, {
  path: '/woods-hole/:id',
  name: 'woodsholesingle',
  component: WoodsHoleSingle,
  meta: {
    keepAlive: false
  }
}, {
  path: '/security-map',
  name: 'security-map',
  component: function (resolve) {
    require(['@/views/AMap.vue'], resolve)
  },
  meta: {
    keepAlive: false
  }
}, {
  path: '/mmap',
  name: 'mmap',
  component: function (resolve) {
    require(['@/views/MetaMap.vue'], resolve)
  },
  meta: {
    keepAlive: false
  }
}]
export default routes
