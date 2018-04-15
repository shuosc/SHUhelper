<template lang="pug">
  div(class="container" @click="clickHandle('test click', $event)")
    div.row(style="height:1.5rem;padding-top:1rem;padding-bottom:1rem;background-color:#03A9F4;")
    div.row(style="box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);border-radius:10px;height:1.5rem;margin-left:0.5rem;margin-right:0.5rem;padding-top:1rem;padding-bottom:1rem;background-color:#03A8F4;position:relative;top:-2rem;")
      .col-2
      .col-8(style="text-align:center;font-weight:bold;")
        | Hi, {{userInfo.nickName}}
      .col-2
        img(style="height:1.5rem;width:1.5rem;margin:auto;display:block;" class="userinfo-avatar" v-if="userInfo.avatarUrl" :src="userInfo.avatarUrl" background-size="cover")
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

export default {
  data() {
    return {
      motto: 'Hello World',
      userInfo: {}
    }
  },

  components: {
    card
  },

  methods: {
    bindViewTap() {
      const url = '../logs/main'
      wx.navigateTo({ url })
    },
    getUserInfo() {
      // 调用登录接口
      wx.login({
        success: () => {
          wx.getUserInfo({
            success: res => {
              this.userInfo = res.userInfo
            }
          })
        }
      })
    },
    clickHandle(msg, ev) {
      console.log('clickHandle:', msg, ev)
    }
  },

  created() {
    // 调用应用实例的方法获取全局数据
    this.getUserInfo()
  }
}
</script>

<style scoped>
.page {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: #50a3a2;
  background: -webkit-linear-gradient(top left, #03A9F4 0%, #53e3a6 100%);
  background: linear-gradient(to bottom, #03A9F4 0%, #fff 100%);
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
