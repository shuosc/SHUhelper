<template>
  <div style="height:100%;">
  <view-box ref="viewBox" body-padding-top="46px" body-padding-bottom="50px">
  <x-header slot="header" style="width:100%;position:absolute;left:0;top:0;z-index:100;">SHUhelper 2.0 preview
  <div slot="right" @click="$store.state.account.token != ''?logout():showLoginForm = true">{{$store.state.account.token != ''?'注销':'登录'}}</div>
  </x-header>
    <scroller lock-x scrollbar-y height="-100" ref="foodscroller">
        <div>
        <marquee style="margin-top:10px;">
          <marquee-item v-for="i in 5" :key="i" @click.native="onClick(i)"  style="text-align:center;">现在是预览版，功能还不全哦❤</marquee-item>
        </marquee>
        <div v-for="group in functions_groups">
          <group-title>{{group.group_tittle}}</group-title>
          <grid>
            <grid-item style="text-align:center;":link="item.url" :label="item.tittle" v-for="item in group.functions">
              <i slot="icon" style="color:#009ACD;font-size:1.5rem;" :class="'iconfont ' + item.icon"></i>
            </grid-item>
          </grid>
        </div>
        <divider>Powered by SHUhelper</divider>
        </div>
    </scroller>
    <div slot="bottom">
     <tabbar>
        <tabbar-item selected :link="'/'">
            <i class="iconfont icon-dashboard" slot="icon"></i>
            <span slot="label">功能</span>
        </tabbar-item>
        <tabbar-item :link="'/my'">
            <i class="iconfont icon-heart" slot="icon"></i>
            <span slot="label">我的</span>
        </tabbar-item>  
    </tabbar>
    </div>
    </view-box>
    <popup v-model="showLoginForm">
      <div class="popup1">
        <group label-width="4em" label-margin-right="2em" label-align="right">
          <x-input title="学号" v-model="cardID"></x-input>
          <x-input title="密码" type="password" v-model="password"></x-input>
        </group>
        <group label-width="4em" label-margin-right="2em" label-align="right">
          <x-button type="primary" @click.native="login()">登录</x-button>
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
  data () {
    return {
      value: 1,
      show: false,
      showLoginForm: false,
      is_login: false,
      cart: {
        'isempty': true
      },
      cardID: '',
      password: '',
      orderTime: '0',
      now: 0,
      currentFood: {},
      selectSpecificationShow: false,
      functions_groups: [{
        'group_tittle': '特色功能',
        'functions': [{
          'tittle': '旧版helper',
          'icon': 'icon-heart-o',
          'url': 'https://www.shuhelper.cn/'
        }, {
          'tittle': '空教室查询',
          'icon': 'icon-xiangtongfangjianrenwu',
          'url': '/service-frame/findemptyroom'
        }, {
          'tittle': '都有空吗',
          'icon': 'icon-group'
        }, {
          'tittle': '一键退学',
          'icon': 'icon-drivers-license-o'
        }, {
          'tittle': '尔美西餐厅预定',
          'icon': 'icon-dppj',
          'url': 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf6081fd49106fe2b&redirect_uri=https%3a%2f%2fermei.shuhelper.cn%2f%23%2fhome&response_type=code&scope=snsapi_base&state=123#wechat_redirect'
        }, {
          'tittle': '陆续上线中...',
          'icon': 'icon-certificate'
        }]}, {
          'group_tittle': '常用查询',
          'functions': [{
            'tittle': '晨跑课外活动',
            'icon': 'icon-tiyu2',
            'url': '/query/tiyu'
          }, {
            'tittle': '课外活动时间表',
            'icon': 'icon-tiyu1',
            'url': '/frame/activities'
          }, {
            'tittle': '校历',
            'icon': 'icon-rili',
            'url': '/frame/cal'
          }, {
            'tittle': '课表',
            'icon': 'icon-course-table'
          }, {
            'tittle': '校园地图',
            'icon': 'icon-map-o',
            'url': '/frame/map'
          }, {
            'tittle': '就医指导',
            'icon': 'icon-yiyuan',
            'url': '/frame/med'
          }, {
            'tittle': '校车运行',
            'icon': 'icon-bus',
            'url': '/frame/bus'
          }, {
            'tittle': '场馆开放',
            'icon': 'icon-icon'
          }, {
            'tittle': '一卡通余额流水',
            'icon': 'icon-icon1'
          }, {
            'tittle': '陆续上线中...',
            'icon': 'icon-certificate'
          }]
        }]
    }
  },
  created: function () {
    if (localStorage.getItem('loginstate') !== null && this.$store.state.account.token === '') {
      console.log('read from local storage')
      this.verifyToken()
    }
  },
  computed: {
  },
  methods: {
    logout () {
      localStorage.clear()
      this.$http.get('/api/accounts/logout')
      this.$vux.toast.show({
        position: 'bottom',
        type: 'text',
        text: '已注销'
      })
      this.$store.commit('clearAccount')
      console.log('logout')
    },
    verifyToken () {
      var _this = this
      var token = JSON.parse(localStorage.getItem('loginstate')).token
      this.$http.get('/api/accounts/login-with-token?token=' + token)
      .then((response) => {
        if (response.data.success) {
          var payload = JSON.parse(localStorage.getItem('loginstate'))
          _this.$store.commit('updateAccount', payload)
          this.$vux.toast.show({
            position: 'bottom',
            type: 'text',
            text: '已使用缓存登录'
          })
        } else {
          _this.logout()
        }
      })
    },
    login () {
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
          localStorage.setItem('loginstate', JSON.stringify(payload))
          _this.$store.commit('updateAccount', payload)
          this.$vux.alert.show({
            title: '成功',
            content: '验证通过',
            onShow () {
            },
            onHide () {
              console.log(response)
              _this.showLoginForm = false
            }
          })
        } else {
          this.$vux.alert.show({
            title: '提示',
            content: '一卡通绑定失败 请重新尝试',
            onShow () {
            },
            onHide () {
              console.log(response)
            }
          })
        }
      })
    },
    resetScroller () {
      this.$nextTick(() => {
        this.$refs.cartscroller.reset({
        })
      })
    }
  }
}
</script>

<style>
.popup {
  width: 95%;
  background-color:#fff;
  height:300px;
  margin:0 auto;
  border-radius:5px;
  padding-top:10px;
}
.title {
    text-align:left;
}
.desc {
    text-align:left;
    font-size:10px;
    color: grey;
}
.logo {
  width: 100px;
  height: 100px
}
.trolley {
    position:absolute;
    display:block;
    width:100%;
    height:40px;
    bottom:50px;
}
.popup1 {
  padding-bottom:15px;
  height:200px;
}
.item {
  border: 1px solid #ececec;
  margin:0 5px;
  padding: 5px;
  font-size: 0.8em;
  width:25%;
}
.box {
  width:100%;
  padding-bottom:10px;
}
.item-selected {
  border: 1px solid green;
}
</style>
