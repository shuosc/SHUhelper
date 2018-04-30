<template lang="pug">
  div(class="container" @click="clickHandle('test click', $event)")
    div.row.header-box
    div.row.user-info
      .col-2
      .col-8(style="color:white;text-align:center;font-weight:bold;")
        | Hi, {{userInfo.nickName}}
      .col-2
        img(@click="onAvatarClick",style="height:1.5rem;width:1.5rem;margin:auto;display:block;" class="userinfo-avatar" v-if="userInfo.avatarUrl" :src="userInfo.avatarUrl" background-size="cover")
    //- div
    time-table(:courses="courses" @showDetail="showDetail")
    //- <div class="userinfo" @click="bindViewTap">
    //-   <img class="userinfo-avatar" v-if="userInfo.avatarUrl" :src="userInfo.avatarUrl" background-size="cover" />
    //-   <div class="userinfo-nickname">
    //-     <card :text="userInfo.nickName"></card>
    //-   </div>
    //- </div>

    //- <div class="usermotto">
    //-   <div class="user-motto">
    //-     <card :text="motto"></card>
    //-   </div>
    //- </div>

    //- <form class="form-container">
    //-   <input type="text" class="form-control" v-model="motto" placeholder="v-model" />
    //-   <input type="text" class="form-control" v-model.lazy="motto" placeholder="v-model.lazy" />
    //- </form>
    //- <a href="/pages/counter/main" class="counter">去往Vuex例页面</a>
    //- <a href="/pages/login/main" class="counter">去往登陆页面</a>
</template>

<script>
import card from '@/components/card'
import TimeTable from '@/components/TimeTable'
import { decrypt } from '@/utils/index.js'

export default {
  data() {
    return {
      motto: 'Hello World',
      userInfo: {},
      courses: [],
      isLogin: false
    }
  },

  components: {
    card,
    TimeTable
  },
  methods: {
    reAuth() {
      wx.login({
        success: res => {
          this.$http
            .get(`/auth/mp/app?code=${res.code}&source=shuhelper_mp_app`)
            .then(response => {
              this.redirectToLogin(response.data.authID)
            })
            .catch(err => {
              this.redirectToLogin(err.response.data.authID)
            })
        }
      })
    },
    updateCourseState(data) {
      let user = wx.getStorageSync('user')
      if (!user) {
        this.reAuth()
      }
      this.courses = decrypt(data.data, user.password)
    },
    bindViewTap() {
      const url = '../logs/main'
      wx.navigateTo({ url })
    },
    clickHandle(msg, ev) {
      console.log('clickHandle:', msg, ev)
    },
    refreshCourse() {
      wx.showNavigationBarLoading()
      let user = wx.getStorageSync('user')
      if (!user.id) {
        this.reAuth()
      }
      this.$http
        .post('/users/data/my-course', {
          id: user.id,
          pw: user.password
        })
        .then(res => {
          wx.hideNavigationBarLoading()
          console.log(res)
          this.getCourses()
          wx.stopPullDownRefresh()
          wx.showToast({
            title: '刷新课表成功'
          })
        })
        .catch(err => {
          wx.hideNavigationBarLoading()
          if (err.status.code === 401) {
            wx.redirectTo({
              url: '/pages/login/main'
            })
          }
          console.log(err)
        })
    },
    getCourses() {
      this.$http
        .get('/users/data/my-course')
        .then(response => {
          // let time = this.$store.state.time
          wx.setStorageSync(`myCourses:2018_3`, response.data)
          this.updateCourseState(response.data)
        })
        .catch(err => {
          if (err.response.status === 404) {
            // wx.showToast(`更新课表中`)
            this.refreshCourse()
          } else {
            // wx.showToast(`更新失败${err.response.status}`)
          }
        })
    },
    onAvatarClick() {
      wx.showActionSheet({
        itemList: ['重新登录', '关于'],
        success: res => {
          console.log(res.tapIndex)
          if (res.tapIndex === 0) {
            this.reAuth()
            // wx.redirectTo({
            //   url: '/pages/login/main'
            // })
          } else {
            wx.showModal({
              title: 'SHUhelper 小程序版本 v0.1.5',
              content:
                `现在您也可以在微信小程序里查看课表啦。使用过程中出现问题请直接向微信公众号 shuhelper 后台反馈。`,
              showCancel: false
            })
          }
        }
      })
    }
  },
  onPullDownRefresh() {
    console.log('pull down')
    wx.showModal({
      title: '提示',
      content: '刷新当前课表吗，这可能需要一点时间',
      success: res => {
        wx.stopPullDownRefresh()
        if (res.confirm) {
          this.refreshCourse()
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },
  created() {
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
  background-color: #85b7d8;
}
.user-info {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  height: 2rem;
  margin-left: 0.5rem;
  margin-right: 0.5rem;
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
  background-color: #85b7d8;
  position: relative;
  top: -2rem;
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
