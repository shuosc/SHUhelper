<template>
  <v-app light toolbar style="height:100%;">
    <v-toolbar fixed dense>
      <v-btn icon @click.prevent="back" v-if="!$route.meta.disableBack">
        <v-icon>arrow_back</v-icon>
      </v-btn>
      <v-toolbar-title v-text="$route.meta.title"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon v-if="$store.state.user.cardID===''" @click.native="login()">
        登陆
      </v-btn>
      <v-btn icon v-else @click.native="logout()">
        注销
      </v-btn>
      <!-- <v-btn icon @click.native="onProfileClick">
                  <v-icon>help</v-icon>
                </v-btn> -->
      <!-- <v-btn icon @click.native="onProfileClick">
                  <v-icon>perm_identity</v-icon>
                </v-btn> -->
      <!-- <v-btn icon>
                <v-icon>search</v-icon>
              </v-btn> -->
    </v-toolbar>
    <main :style="{paddingBottom:ui.bottomNavigationVisible?'56px':'0',height:'100%',overflowY:'scroll'}" id="main" ref="container" @scroll="handleScroll">
      <v-slide-y-transition mode="out-in">
        <!-- <keep-alive> -->
        <router-view></router-view>
        <!-- </keep-alive> -->
      </v-slide-y-transition>
    </main>
    <v-bottom-nav class="white ma-0 pa-0" v-model="ui.bottomNavigationVisible" :active.sync="bottomNavgationIndex">
      <v-btn flat light v-for="(nav,index) in bottomNavs" :key="index" class="teal--text" @click.native="onBottomNavgationClick(index)">
        <span>{{nav.name}}</span>
        <v-icon>{{nav.icon}}</v-icon>
      </v-btn>
    </v-bottom-nav>
    <login> </login>
    <v-snackbar :timeout="snackbar.timeout" :top="snackbar.y === 'top'" :bottom="snackbar.y === 'bottom'" :right="snackbar.x === 'right'" :left="snackbar.x === 'left'" :multi-line="snackbar.mode === 'multi-line'" :vertical="snackbar.mode === 'vertical'" v-model="snackbar.visible" style="bottom:100px;">
      {{ snackbar.text }}
      <v-btn flat class="pink--text" @click.native="snackbar.visible = false">Close</v-btn>
    </v-snackbar>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
import _ from 'lodash'
import Login from './components/dialog/Login'
export default {
  components: {
    Login
  },
  data () {
    return {
      items: [
        'All', 'Family', 'Friends', 'Coworkers'
      ],
      scrolled: false,
      scrollY: 0,
      bottomNavgationIndex: 0,
      loginLoading: false,
      bottomNavs: [{ name: '首页', icon: 'school', url: '/' },
      { name: '广场', icon: 'filter_vintage', url: '/square' },
      { name: '课表', icon: 'event', url: '/calendar' },
      { name: '消息', icon: 'chat', url: '/messages' }
        // { name: '更多', icon: 'more', url: '/messages' }
      ],
      clipped: false,
      drawer: false,
      fixed: false,
      dialog: false,
      remeberMe: false,
      passwordVisiable: false,
      miniVariant: false,
      title: '首页'
    }
  },
  computed: mapState([
    'snackbar', 'ui'
  ]),
  created () {
    this.$router.push('/')
    // this.bottomNavgationIndex = 0
    // for (let index in this.bottomNavs) {
    //   console.log(this.$route.path, this.bottomNavs[index].url)
    //   if (this.bottomNavs[index].url === this.$route.path) {
    //     this.bottomNavgationIndex = index
    //     console.log(index)
    //   }
    // }
    // console.log(this.bottomNavgationIndex)
    // console.log(this.$refs.container, 'ref')
    // this.$refs.container.addEventListener('scroll', this.handleScroll)
    // window.addEventListener('scroll', this.handleScroll)
    this.verifyToken()
  },
  mounted () {
    // this.$refs.container.addEventListener('scroll', this.handleScroll)
    // console.log('mounted', this.$refs)
  },
  destroyed () {
    // this.$refs.container.removeEventListener('scroll', this.handleScroll)
  },
  watch: {
    '$route' (to, from) {
      // this.$refs.container.scrollTop = 0
      this.scrollY = this.$refs.container.scrollTop
    }
  },
  methods: {
    onProfileClick () {
      // console.log(this.$store.state.user.cardID)
      if (this.$store.state.user.cardID !== '') {
        this.$router.push(`/profile/${this.$store.state.user.cardID}`)
      } else {
        this.$store.commit('showLoginDialog')
      }
    },
    handleScroll: _.throttle(function () {
      let container = this.$refs.container
      let scrollHeight = container.scrollHeight
      let clientHeight = container.clientHeight
      let scrollTop = container.scrollTop
      if (this.$route.meta.unableBottomNavgation) {
        this.$store.commit('hideBottomNavgation')
        return
      }
      if (scrollTop <= 20) {
        this.$store.commit('showBottomNavgation')
        return
      }
      if (scrollHeight - clientHeight - scrollTop <= 60) {
        this.$store.commit('hideBottomNavgation')
        return
      }
      if (this.scrollY < scrollTop) {
        if (this.$store.state.ui.bottomNavigationVisible) {
          this.$store.commit('hideBottomNavgation')
        }
      } else {
        this.$store.commit('showBottomNavgation')
      }
      this.scrollY = scrollTop
    }, 50),
    back () {
      this.$router.go(-1)
    },
    onBottomNavgationClick (index) {
      this.$router.replace(this.bottomNavs[index].url)
      this.bottomNavgationIndex = index
      console.log(this.bottomNavgationIndex)
    },
    logout () {
      localStorage.clear()
      let token = this.$store.state.user.token
      this.$store.commit('clearAccount')
      this.$router.push('/')
      this.$store.commit('showSnackbar', { text: '已注销' })
      this.$http.get('/api/users/logout?token=' + token)
    },
    login () {
      this.$store.commit('showLoginDialog')
    },
    verifyToken () {
      var _this = this
      try {
        var token = JSON.parse(localStorage.getItem('loginstate')).token
      } catch (err) {
        console.log(err)
      }
      this.$http.get(`/api/users/login-with-token/?token=${token}`)
        .then((response) => {
          var payload = JSON.parse(localStorage.getItem('loginstate'))
          _this.$store.commit('updateAccount', payload)
          _this.$store.commit('showSnackbar', { text: `${response.data.name}，欢迎登陆` })
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style lang="stylus">
  @import './stylus/main'
.fullscreen-v-img
  z-index:10
.body
  -webkit-overflow-scrolling:touch
</style>
