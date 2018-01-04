<template lang="pug">
  // Don't drop "q-app" class
  div#q-app
    q-layout(ref="layout" view="hHh Lpr fFf" :left-class="{'bg-grey-2': true}")
      q-toolbar(slot="header" v-if="!$route.meta.disableLayout")
        q-btn(flat @click="$refs.layout.toggleLeft()")
          q-icon(name="menu")
        q-toolbar-title {{title}}
          // <div slot="subtitle">Running on University Helper Engine v{{$UHE.version}}</div>
        router-view(name="toolbar")
      div(slot="left")
        // Use <q-side-link> component instead of <q-item> for internal vue-router navigation
        left-panel
        // <router-view  name="left"/>
      // <q-scroll-area style="width: 100%; height: 100%;">
      q-transition(enter="fadeIn" leave="fadeOut" mode="out-in" :duration="300" @leave="resetScroll")
        router-view
      //</q-scroll-area>
      div(slot="footer" v-if="$q.platform.is.ios && !$route.meta.disableLayout")
        q-tabs
          q-route-tab(icon="fa-xuexiao" to="/" exact slot="title" @click="changeTitle('首页')")
          // <q-route-tab icon="fa-filtervintage" to="/square" exact slot="title" /> 
          q-route-tab(icon="fa-calendar1" to="/schedule" exact slot="title" @click="changeTitle('日程')")
          // <q-route-tab icon="fa-message" to="/message" exact slot="title" /> 
          //</q-scroll-area>
</template>

<script>
/*
 * Root component
 */
import LeftPanel from '@/LayoutLeftPanel'
import { Toast } from 'quasar'
import ga from 'libs/analytics.js'
export default {
  components: {
    LeftPanel
  },
  data() {
    return {
      title: '首页'
    }
  },
  created() {
    this.verifyToken()
    this.getTime()
  },
  methods: {
    resetScroll(el, done) {
      document.documentElement.scrollTop = 0
      document.body.scrollTop = 0
      done()
    },
    changeTitle(newTitle) {
      this.title = newTitle
    },
    getTime() {
      this.$http.get('/api/time/').then(response => {
        this.$store.commit('updateTime', response.data)
      })
    },
    verifyToken() {
      var _this = this
      var token = ''
      var payload = {}
      // if (window.sessionStorage) {
      //   alert('浏览支持sessionStorage')
      // } else {
      //   alert('浏览暂不支持sessionStorage')
      // }
      try {
        token = JSON.parse(sessionStorage.getItem('loginstate')).token
        payload = JSON.parse(sessionStorage.getItem('loginstate'))
      } catch (err) {
        console.log(err)
        try {
          token = JSON.parse(localStorage.getItem('loginstate')).token
          payload = JSON.parse(localStorage.getItem('loginstate'))
        } catch (err) {
          console.log(err)
          // this.$http.get('/api/users/logout')
        }
      }
      if (token === '') {
        // this.$router.push('/login')
        return
      }
      this.$http
        .get(`/api/users/login/?token=${token}`)
        .then(response => {
          // var payload = JSON.parse(localStorage.getItem('loginstate'))
          var custom = {}
          try {
            custom = JSON.parse(response.data.custom)
          } catch (e) {
            console.log(e)
            custom = {}
          }
          payload.custom = custom
          payload.avatar = response.data.avatar
          _this.$store.commit('updateAccount', payload)
          ga.loginUser(payload.cardID)
          if (custom.loginText === undefined) {
            Toast.create(`${response.data.name}，欢迎登陆`)
          } else {
            Toast.create(`${custom.loginText}`)
          }
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style>

</style>
