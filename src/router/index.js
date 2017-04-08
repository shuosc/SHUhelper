import Vue from 'vue'
import Router from 'vue-router'
// import Hello from '@/components/Hello'
import Functions from '@/views/functions'
import My from '@/views/My'
import Map from '@/views/Map'
import Frame from '@/views/Frame'
import ServiceFrame from '@/views/ServiceFrame'
Vue.use(Router)

const routes = [{
  path: '/',
  name: 'Hello',
  component: Functions
}, {
  path: '/my',
  name: 'Hello',
  component: My
}, {
  path: '/map',
  name: 'Hello',
  component: Map
}, {
  path: '/frame/:name',
  name: 'Hello',
  component: Frame
}, {
  path: '/service-frame/:name',
  name: 'Hello',
  component: ServiceFrame
}]

export default routes
