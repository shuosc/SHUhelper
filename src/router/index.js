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
import FindFreeTime from '@/views/FindFreeTime'
import SUIndex from '@/views/SUIndex'

Vue.use(Router)

const routes = [{
  path: '/',
  component: Functions
}, {
  path: '/my',
  component: My
}, {
  path: '/map',
  component: Map
}, {
  path: '/frame/:name',
  component: Frame
}, {
  path: '/service-frame/:name',
  component: ServiceFrame
}, {
  path: '/query/:name',
  component: QueryTemplate
}, {
  path: '/messageboard',
  component: Messageboard
}, {
  path: '/classrooms',
  component: Classrooms
}, {
  path: '/courses',
  component: Courses
}, {
  path: '/findfreetime',
  component: FindFreeTime
}, {
  path: '/index-su',
  component: SUIndex
}]
export default routes
