<template>
  <v-app toolbar style="height:100%;" :class="$store.state.user.custom.theme">
    <v-toolbar fixed dense class="primary">
      <v-btn icon @click.prevent="back" v-if="!$route.meta.disableBack">
        <v-icon>iconfont-back</v-icon>
      </v-btn>
      <v-toolbar-title v-text="$route.meta.title"></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu bottom class="ma-0">
        <v-btn icon slot="activator">
          <v-icon>iconfont-morevert</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-if="$store.state.user.cardID!==''" @click.native="onProfileClick">
            <v-list-tile-title>个人资料</v-list-tile-title>
          </v-list-tile>
          <v-list-tile v-if="$store.state.user.cardID===''" @click.native="login()">
            <v-list-tile-title>登陆</v-list-tile-title>
          </v-list-tile>
          <v-list-tile v-else @click.native="logout()">
            <v-list-tile-title>注销</v-list-tile-title>
          </v-list-tile>
          <v-list-tile @click.native="aboutDialog=true">
            <v-list-tile-title>关于</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>
    <!-- overflowY:'scroll' -->
    <main :style="{paddingBottom:ui.bottomNavigationVisible?'56px':'0',height:'100%'}" class="wrapper" id="main" ref="container" @scroll="handleScroll">
      <v-slide-y-transition mode="out-in">
        <!-- <keep-alive> -->
       <router-view v-if="!$route.meta.keepAlive"></router-view>
        <keep-alive>
          <router-view v-if="$route.meta.keepAlive"></router-view>
        </keep-alive>
        
        <!-- </keep-alive> -->
      </v-slide-y-transition>
    </main>
    <v-bottom-nav class="primary ma-0 pa-0" dark v-model="ui.bottomNavigationVisible" :active.sync="bottomNavgationIndex">
      <v-btn flat v-for="(nav,index) in bottomNavs" :key="index" @click.native="onBottomNavgationClick(index)">
        <span>{{nav.name}}</span>
        <v-icon>{{nav.icon}}</v-icon>
      </v-btn>
    </v-bottom-nav>
    <login> </login>
    <v-snackbar :timeout="snackbar.timeout" :top="snackbar.y === 'top'" :bottom="snackbar.y === 'bottom'" :right="snackbar.x === 'right'" :left="snackbar.x === 'left'" :multi-line="snackbar.mode === 'multi-line'" :vertical="snackbar.mode === 'vertical'" v-model="snackbar.visible" style="bottom:100px;">
      {{ snackbar.text }}
      <v-btn flat class="pink--text" @click.native="snackbar.visible = false">Close</v-btn>
    </v-snackbar>
    <v-layout row justify-center style="position: relative;">
      <v-dialog v-model="aboutDialog" lazy absolute>
        <v-card>
          <v-card-title>
            <div class="headline">SHUhelper3</div>
          </v-card-title>
          <v-card-text>
            <p>SHUhelper是一个开源的校园门户系统 旨在为所有人的生活带来便利</p>
            <p>目前由上海大学开源社区负责维护</p>
            <p>
              <a href="https://www.pgyer.com/SHUhelper">Android</a>|
              <a href="http://shuhelper.shuosc.org">项目主页</a>|
              <a href="https://github.com/shuopensourcecommunity/SHUhelper">GitHub</a>|
              <a href="https://osc.shu.edu.cn/">开源社区</a>
            </p>
            <p>
              联系我们:
              <a href="mailto:contact@shuosc.org">contact@shuosc.org</a>
            </p>
            <p>
              加入开源社区QQ群：146685225
            </p>
            <p>
              开源社区公众号：shuosc
            </p>
            <p>
              SHUhelper公众号：shuhelper
            </p>
            <p style="text-align:center;">
              <img src="/static/built-with-love.svg"><br/><img src="/static/for-you.svg"></p>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-layout>
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
      aboutDialog: false,
      scrolled: false,
      scrollY: 0,
      bottomNavgationIndex: 0,
      loginLoading: false,
      bottomNavs: [{ name: '首页', icon: 'iconfont-xuexiao', url: '/' },
      { name: '广场', icon: 'iconfont-filtervintage', url: '/square' },
      { name: '课表', icon: 'iconfont-calendar1', url: '/calendar' },
      { name: '消息', icon: 'iconfont-message', url: '/messages' }
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
      sessionStorage.clear()
      let token = this.$store.state.user.token
      this.$store.commit('clearAccount')
      this.$router.push('/')
      this.$store.commit('showSnackbar', { text: '已注销' })
      this.$http.get('/api/v1/users/logout?token=' + token)
    },
    login () {
      this.$store.commit('showLoginDialog')
    },
    verifyToken () {
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
          this.$http.get('/api/v1/users/logout')
        }
      }
      if (token === '') {
        this.login()
        return
      }
      this.$http.get(`/api/v1/users/login-with-token/?token=${token}`)
        .then((response) => {
          // var payload = JSON.parse(localStorage.getItem('loginstate'))
          var custom = {}
          try {
            custom = JSON.parse(response.data.custom)
          } catch (e) {
            e
            custom = {}
          }
          payload.custom = custom
          _this.$store.commit('updateAccount', payload)
          if (custom.loginText === undefined) {
            _this.$store.commit('showSnackbar', { text: `${response.data.name}，欢迎登陆` })
          } else {
            _this.$store.commit('showSnackbar', { text: `${custom.loginText}` })
          }
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style lang="stylus">
// $color-pack = false
@import './stylus/main'
$unset secondary
$unset primary
.fullscreen-v-img
  z-index:10
.wrapper 
  overflow: auto
  -webkit-overflow-scrolling: touch
</style>
