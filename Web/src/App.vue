<template lang="pug">
  div#q-app
    q-layout(ref="layout" view="lHh Lpr lFf" :left-class="{'bg-grey-2': true}" reveal)
      q-toolbar(slot="header" v-show="!$route.meta.disableToolbar")
        <q-btn v-show="$route.meta.back" slot="left" flat round small class="primary" v-back>
          <q-icon name="keyboard_backspace" />
        </q-btn>
        q-btn(flat v-show="!$route.meta.back" @click="$refs.layout.toggleLeft()")
          q-icon(name="menu")
        q-toolbar-title {{$route.meta.title}}
        router-view(name="toolbar")
      left-panel( slot="left")
      //- transition(:name="'router-' + stack.direction")      
        //- q-transition(enter="fadeIn" leave="fadeOut" mode="out-in" :duration="300" @leave="resetScroll")
      navigation
        router-view
      q-modal.flex(ref="imgModal" minimized @click.native="$refs.imgModal.close()")
        q-card.no-margin(flat v-if="imgLoading" style="min-height:100px;min-width:100px;")
          q-inner-loading(:visible="imgLoading")
            q-spinner-gears(size="50px" color="primary")
        img.responsive(:src="img" v-show="!imgLoading" @load="imgLoad")
      div(slot="footer" v-show="!$route.meta.disableBottom && $q.platform.is.mobile")
        bottom-navigation
</template>

<script>
/*
 * Root component
 */
import LeftPanel from '@/LayoutLeftPanel'
import { mapState } from 'vuex'
import BottomNavigation from '@/BottomNavigation'
import { Toast, QInnerLoading, QSpinnerGears } from 'quasar'
import ga from 'libs/analytics.js'
export default {
  components: {
    LeftPanel,
    BottomNavigation,
    QInnerLoading,
    QSpinnerGears
  },
  data() {
    return {
      title: '首页',
      imgLoading: false,
      img: ''
    }
  },
  computed: {
    ...mapState(['stack'])
  },
  created() {
    this.$q.events.$on('app:showImg', this.showImg)
    ga.loginUser('00000001')
    this.verifyToken()
    this.getTime()
  },
  methods: {
    imgLoad() {
      this.imgLoading = false
    },
    showImg(img) {
      if (this.img !== img) {
        this.imgLoading = true
      }
      this.img = img
      this.$refs.imgModal.open()
    },
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
html,
body {
  /* height: 100%; */
  /* width: 100%; */
  /* overflow: auto; */
  -webkit-overflow-scrolling: touch;
}
/* #q-app {
  height: 100%;
} */
.router-backward-enter-active,
.router-forward-enter-active,
.router-backward-leave-active,
.router-forward-leave-active {
  will-change: transform;
  transition: all 500ms ease-out;
  height: 100%;
  width: 100%;
  position: absolute;
  backface-visibility: hidden;
}

.router-backward-enter {
  opacity: 1;
  transform: translate3d(-50%, 0, 0);
}

.router-backward-leave-active {
  opacity: 0.5;
  z-index: 100;
  transform: translate3d(100%, 0, 0);
}

.router-forward-enter {
  opacity: 1;
  transform: translate3d(100%, 0, 0);
}

.router-forward-leave-active {
  opacity: 0.5;
  transform: translate3d(-50%, 0, 0);
}
</style>
