<template>
  <div id="app"
       style="height:100%;">
    <view-box ref="viewBox"
              body-padding-top="46px"
              body-padding-bottom="50px">
      <x-header slot="header"
                :left-options="{showBack:$route.path!='/' && $route.path!='/my' }"
                style="width:100%;position:absolute;left:0;top:0;z-index:100;">SHUhelper 2.2
        <div slot="right"
             @click="$store.state.account.token != ''?logout():$store.commit('changeLoginFormShow')">{{$store.state.account.token != ''?'注销':'登录'}}</div>
      </x-header>
      <transition name="fade">
        <keep-alive>
          <router-view v-if="$route.meta.keepAlive"></router-view>
        </keep-alive>
      </transition>
      <transition name="fade">
        <router-view v-if="!$route.meta.keepAlive"></router-view>
      </transition>
      <div slot="bottom">
        <tabbar>
          <tabbar-item selected
                       :link="'/'">
            <i class="iconfont icon-dashboard"
               slot="icon"></i>
            <span slot="label">功能</span>
          </tabbar-item>
          <tabbar-item :link="'/my'">
            <i class="iconfont icon-heart"
               slot="icon"></i>
            <span slot="label">我的</span>
          </tabbar-item>
        </tabbar>
      </div>
    </view-box>
    <popup v-model="$store.state.showLoginForm"
           is-transparent
           height="270px"
           @on-hide="$store.state.showLoginForm?$store.commit('changeLoginFormShow'):1">
      <div class="popup">
        <group label-width="4em"
               label-margin-right="2em"
               label-align="right">
          <x-input title="学号"
                   v-model="cardID"></x-input>
          <x-input title="密码"
                   type="password"
                   v-model="password"></x-input>
        </group>
        <group label-width="4em"
               label-margin-right="2em"
               label-align="right">
          <x-button type="primary"
                    @click.native="login()">登录</x-button>
        </group>
      </div>
    </popup>
  </div>
</template>

<script>
import { Group, Cell, Tabbar, TabbarItem, XHeader, Divider, Card, XNumber, Flexbox, FlexboxItem, XImg, Scroller, ViewBox, XButton, Popup, Radio, XInput, Checker, CheckerItem, Grid, GridItem, GroupTitle, Marquee, MarqueeItem } from 'vux'

export default {
  components: {
    Grid,
    Marquee,
    MarqueeItem,
    GroupTitle,
    GridItem,
    Group,
    Cell,
    Tabbar,
    TabbarItem,
    XHeader,
    Divider,
    Card,
    XNumber,
    FlexboxItem,
    Flexbox,
    XImg,
    Scroller,
    ViewBox,
    XButton,
    Popup,
    Radio,
    XInput,
    Checker,
    CheckerItem
  },
  name: 'app',
  data() {
    return {
      cardID: '',
      password: ''
    }
  },
  methods: {
    logout() {
      var token = this.$store.state.account.token
      localStorage.clear()
      this.$http.get('/api/accounts/logout?token=' + token)
      this.$vux.toast.show({
        position: 'bottom',
        type: 'text',
        text: '已注销'
      })
      this.$store.commit('clearAccount')
    },
    login() {
      var _this = this
      this.$vux.loading.show({
        text: '验证一卡通中...'
      })
      this.$http.post('/api/accounts/login', {
        card_id: this.cardID,
        password: this.password
      })
        .then((response) => {
          this.$vux.loading.hide()
          if (response.data.success) {
            var payload = {
              card_id: this.cardID,
              password: this.password,
              name: response.data.name,
              nickname: response.data.nickname,
              token: response.data.token
            }
            try {
              localStorage.setItem('loginstate', JSON.stringify(payload))
            } catch (err) {
              this.$vux.alert.show({
                title: '提示',
                content: '本地存储失败，如果您在使用APP，请升级到最新版本(http://static.shuhelper.cn/SHUhelper.apk)，如果在使用浏览器，请关闭无痕浏览模式'
              })
            }
            _this.$store.commit('updateAccount', payload)
            _this.$store.commit('changeLoginFormShow')
            this.$vux.alert.show({
              title: '成功',
              content: '验证通过',
              onShow() {
              },
              onHide() {
                // console.log(response)
              }
            })
          } else {
            this.$vux.alert.show({
              title: '提示',
              content: '一卡通绑定失败 请重新尝试',
              onShow() {
              },
              onHide() {
                console.log(response)
              }
            })
          }
        })
    }
  }
}
</script>

<style lang="less">
@import '~vux/src/styles/reset.less';
html,
body {
  height: 100%;
  width: 100%;
  overflow-x: hidden;
}

body {
  background-color: #fbf9fe;
}

.fade-enter-active,
.fade-leave-active {
  // transition: opacity .5s
  transition: all .4s ease;
}

.fade-enter
/* .fade-leave-active in <2.1.8 */

{
  transform: translateX(600px);
  opacity: 0
}

.fade-leave-to {
  transform: translateX(-600px);
  opacity: 0
}

.popup {
  width: 95%;
  background-color: #fff;
  height: 220px;
  margin: 0 auto;
  border-radius: 5px;
  padding-top: 10px;
}
</style>
