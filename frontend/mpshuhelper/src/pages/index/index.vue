<template lang="pug">
  div(class="container" @click="clickHandle('test click', $event)")
    div.row.header-box
    div.row.user-info(@click="onAvatarClick")
      .col-2
      .col-8(style="text-align:center;font-weight:bold;")
        | Hi, {{user.username}}
      .col-2
        img(@click="onAvatarClick",style="height:1.5rem;width:1.5rem;margin:auto;display:block;" class="userinfo-avatar" v-if="user.avatarURL" :src="user.avatarURL" background-size="cover")
    apps
    //- div.calendar
      | 今天是{{time.year}}{{time.term}}{{time.week}}
    
</template>

<script>
import card from '@/components/card'
import apps from '@/pages/apps/index'
// import { decrypt } from '@/utils/index.js'
import { mapState } from 'vuex'
export default {
  data() {
    return {
      motto: 'Hello World',
      userInfo: {},
      courses: [],
      isLogin: false
    }
  },
  computed: mapState(['user', 'time']),
  components: {
    card,
    apps
  },
  onShow() {
    this.$store.dispatch('syncTime')
  },
  methods: {
    reAuth() {
      wx.login({
        success: res => {
          this.$http
            .get(`/auth/mp/app?code=${res.code}&source=shuhelper_mp_app`)
            .then(response => {
              console.log(response)
              wx.redirectTo({
                url: '/pages/login/main'
              })
              // this.redirectToLogin(response.authID)
            })
            .catch(err => {
              console.log(err)
              this.redirectToLogin(err.response.authID)
            })
        }
      })
    },
    bindViewTap() {
      const url = '../logs/main'
      wx.navigateTo({ url })
    },
    clickHandle(msg, ev) {
      console.log('clickHandle:', msg, ev)
    },
    onAvatarClick() {
      wx.showActionSheet({
        itemList: ['重新登录', '关于'],
        success: res => {
          console.log(res.tapIndex)
          if (res.tapIndex === 0) {
            // this.reAuth()
            wx.redirectTo({
              url: '/pages/login/main'
            })
          } else {
            wx.showModal({
              title: 'SHUhelper 小程序版本 v0.1.5',
              content: `现在您也可以在微信小程序里查看课表啦。使用过程中出现问题请直接向微信公众号 shuhelper 后台反馈。`,
              showCancel: false
            })
          }
        }
      })
    }
  },
  onPullDownRefresh() {
    console.log('pull down')
  },
  created() {
    console.log(this.user)
  }
  // onLoad: function() {
  //   console.log('onload')
  //   if (this.$root.$mp.query.refresh) {
  //     this.getUserInfo()
  //   }
  // }
}
</script>

<style scoped>
.header-box {
  height: 1rem;
  padding-top: 1rem;
  padding-bottom: 1rem;
  background-color: #7eb3ec;
}
/* 85b7d8 */
.user-info {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  height: 2rem;
  margin-left: 0.5rem;
  margin-right: 0.5rem;
  padding-top: 1.5rem;
  color: white;
  padding-bottom: 1.5rem;
  background-color: #7eb3ec;
  position: relative;
  top: -2rem;
  border-bottom: 2px solid #6b93ad;
  /* background-image: linear-gradient(180deg, #85b7d8 0%, #c2e9fb 90%); */
}
.container {
  /* padding: 10px; */
  /* padding-right: 10px; */
  padding-bottom: 10px;
  /* padding-top: 10px; */
  box-sizing: border-box;
}
.page {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: #50a3a2;
  background: -webkit-linear-gradient(top left, #03a9f4 0%, #53e3a6 100%);
  background: linear-gradient(to bottom, #03a9f4 0%, #fff 100%);
  height: 100vh; /* Allow spacing based on window height */
  margin: 0;
  min-height: 240px;
  z-index: 6000;
}
.userinfo {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.userinfo-avatar {
  border-radius: 50%;
}

.userinfo-nickname {
  color: #aaa;
}

.usermotto {
  margin-top: 150px;
}

.form-control {
  display: block;
  padding: 0 12px;
  margin-bottom: 5px;
  border: 1px solid #ccc;
}

.counter {
  display: inline-block;
  margin: 10px auto;
  padding: 5px 10px;
  color: blue;
  border: 1px solid blue;
}
</style>
