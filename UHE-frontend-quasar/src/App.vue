<template>
  <!-- Don't drop "q-app" class -->
  <div id="q-app">
    <q-layout ref="layout" view="hHh Lpr fff" :left-class="{'bg-grey-2': true}">
      <q-toolbar slot="header">
        <q-btn flat @click="$refs.layout.toggleLeft()">
          <q-icon name="menu" />
        </q-btn>
        <q-toolbar-title>
          首页
          <!-- <div slot="subtitle">Running on University Helper Engine v{{$UHE.version}}</div> -->
        </q-toolbar-title>
        <router-view name="toolbar"/>
      </q-toolbar>

      <div slot="left">
        <!--
        Use <q-side-link> component
        instead of <q-item> for
        internal vue-router navigation
      -->
        <left-panel/>
        <!-- <router-view  name="left"/> -->
      </div>
      <router-view />
    </q-layout>
    <!-- </q-scroll-area> -->
  </div>
</template>

<script>
/*
 * Root component
 */
import LeftPanel from '@/LayoutLeftPanel'
import { Toast } from 'quasar'
export default {
  components: {
    LeftPanel
  },
  created() {
    this.verifyToken()
  },
  methods: {
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
        this.$router.push('/login')
        return
      }
      this.$http
        .get(`/api/users/login-with-token/?token=${token}`)
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
/* body {
  overflow-y: hidden;
} */
</style>
