<template>
  <!-- Don't drop "q-app" class -->
  <div id="q-app">
    <q-scroll-area style="width: 100vw; height: 100vh;">
    <router-view />
    </q-scroll-area>
  </div>
</template>

<script>
/*
 * Root component
 */
import { Toast } from 'quasar'
export default {
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
          this.$http.get('/api/users/logout')
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
</style>
