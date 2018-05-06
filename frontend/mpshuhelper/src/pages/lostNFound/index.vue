<template lang="pug">
  div(class="container" @click="clickHandle('test click', $event)")
    div.row.header-box.justify-between
      div(style="display:flex;padding-left:1rem;")
        div(style="flex:1;display:flex;")
          img.avatar(:src="user.avatarURL",background-size="cover")
        div(style="color:white;flex:4;padding-left:1rem;font-size:1rem;")
          | {{user.username?user.username:'游客'}}
      .col-1(style="text-align:center;font-weight:bold;")
        //- | Hi, {{user.username}}
      div(style="color:white;display:flex;align-items:center;font-size:1rem;")
        div.iconfont.icon-more(style="padding-right:1rem;padding-left:0.5rem;" @click="onMoreClick")
    div.fab(@click="onAddClick")
      div.iconfont.icon-add
    //- div.row.user-info(@click="onAvatarClick")
      .col-2
      .col-8(style="text-align:center;font-weight:bold;")
        | Hi, {{user.username}}
      .col-2
        img(@click="onAvatarClick",style="height:1.5rem;width:1.5rem;margin:auto;display:block;" class="userinfo-avatar" v-if="user.avatarURL" :src="user.avatarURL" background-size="cover")
    //- div.nav-box
      div(:style="{flex:4}" :class="{'nav-tab-selected':tabIndex === 0}" @click="tabIndex=0")
        | 寻找失物
      div
        | |
      div(:style="{flex:4}" :class="{'nav-tab-selected':tabIndex === 1}" @click="tabIndex=1")
        | 寻找失主
    div.search-bar
      input()
    div()
      div.lost-card(v-for="i in 10" @click="onPostClick")
        div(style="flex:1;display:flex;")
          div(style="background-color:#ccc;height:90%;width:90%;margin:auto;")
        div(style="flex:2;display:flex;flex-direction:column;justify-content:space-between;")
          div(style="flex:1;")
            | title
          div(style="flex:1;")
            | location
          div(style="flex:1;display:flex;")
            div(style="flex:1;display:flex;align-items:center;justify-contet:space-between;")
              //- div(style="flex:1;display:flex;")
                img.avatar(:src="user.avatarURL",background-size="cover")
              div(style="flex:1;color:black;flex:4;font-size:1rem;")
                | {{user.username?user.username:'游客'}}
            div(style="flex:1;")
            div(style="flex:1;text-align:right;padding-right:1rem;")
              span(style="color:grey;font-size:0.5rem;") 2018/07/23
        div(style="display:flex;position:absolute;bottom:5px;right:5px;width:70px;height:70px;border:1px solid red;border-radius:35px;")
          div(style="display:flex;margin:auto;transform:rotate(-30deg);color:grey;") 已找到
</template>

<script>
import card from '@/components/card'
import TimeTable from '@/components/TimeTable'
// import { decrypt } from '@/utils/index.js'
import { mapState } from 'vuex'
export default {
  data() {
    return {
      motto: 'Hello World',
      userInfo: {},
      courses: [],
      isLogin: false,
      tabIndex: 0
    }
  },
  computed: mapState(['user']),
  components: {
    card,
    TimeTable
  },
  methods: {
    bindViewTap() {
      const url = '../logs/main'
      wx.navigateTo({ url })
    },
    clickHandle(msg, ev) {
      console.log('clickHandle:', msg, ev)
    },
    onAddClick() {
      wx.navigateTo({
        url: 'new'
      })
    },
    onMoreClick() {
      wx.showActionSheet({
        itemList: ['重新登录', '返回首页'],
        success: res => {
          console.log(res.tapIndex)
          if (res.tapIndex === 0) {
            wx.redirectTo({
              url: '/pages/login/main'
            })
          } else {
            wx.redirectTo({
              url: '/pages/login/main'
            })
          }
        }
      })
    },
    onPostClick() {
      wx.redirectTo({
        url: 'post'
      })
    },
    onAvatarClick() {
      wx.showActionSheet({
        itemList: ['重新登录', '返回首页'],
        success: res => {
          console.log(res.tapIndex)
          if (res.tapIndex === 0) {
            // this.reAuth()
            wx.redirectTo({
              url: '/pages/login/main'
            })
          } else {
            wx.redirectTo({
              url: '/pages/login/main'
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
  created() {}
}
</script>

<style scoped>
.fab {
  border-radius: 50%;
  height: 5rem;
  width: 5rem;
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background-color: #7eb3ec;
  color: white;
  z-index: 1000;
  box-shadow: 0 5px 5px #ccd8e2;
  display: flex;
  justify-content: center;
  align-items: center;
} 
.avatar {
  border-radius: 50%;
  height: 2rem;
  width: 2rem;
  margin: auto;
  display: block;
}
.search-bar {
  height: 3rem;
  /* margin-top: 10px; */
  margin: 10px 10px 10px 10px;
  /* border: 1px solid #aaa; */
  font-size: 1.3rem;
  padding-left: 10px;
  background-color: #fff;
  box-shadow: 0 15px 20px #ccd8e2;
  border-radius: 10px;
}
.lost-card {
  height: 100px;
  display: flex;
  box-sizing: border-box;
  border-radius: 10px;
  background-color: #fff;
  margin: 10px;
  box-shadow: 0 5px 5px #ccd8e2;
  align-items: stretch;
  position: relative;
}
.header-box {
  height: 3rem;
  padding-top: 1rem;
  padding-bottom: 1rem;
  background-color: #7eb3ec;
  border-radius: 0px 0px 10px 10px;
  box-shadow: 0px 4px 4px -2px rgba(0, 0, 0, 0.2);
  z-index: 2;
}
.nav-box {
  box-shadow: 0px 4px 4px -2px rgba(0, 0, 0, 0.2);
  border-radius: 0px 0px 10px 10px;
  display: flex;
  width: 100vw;
  justify-content: space-between;
  vertical-align: text-bottom;
  align-self: center;
  height: 4rem;
  font-size: 1.5rem;
  color: white;
  text-align: center;
  z-index: 1;
  background-color: #7eb3ec;
  position: relative;
  top: -8px;
  box-sizing: content-box;
}
.nav-tab-selected {
  /* box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.2) inset; */
  border-bottom: 2px solid #fff !important;
  /* border-bottom-left-radius: 10px; */
  /* border-bottom-right-radius: 10px; */
}
.nav-box > div {
  display: flex;
  justify-content: center;
  align-content: center;
  flex-direction: column;
  box-sizing: border-box;
}
.nav-box :first-child {
  margin-left: 10px;
}
.nav-box :last-child {
  margin-right: 10px;
}
.container {
  /* padding: 10px; */
  /* padding-right: 10px; */
  padding-bottom: 10px;
  /* padding-top: 10px; */
  box-sizing: border-box;
  background: #eee;
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
