<template>
  <div style="height:100%;">
  <view-box ref="viewBox" body-padding-top="46px" body-padding-bottom="50px">
  <x-header slot="header" style="width:100%;position:absolute;left:0;top:0;z-index:100;">SHUhelper 2.0 preview
  <div slot="right" @click="log_in_out()">{{is_login?'注销':'登录'}}</div>
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
    <popup v-model="activateShow" :hide-on-blur="false">
      <div class="popup1">
        <group label-width="4em" label-margin-right="2em" label-align="right">
          <x-input title="学号" v-model="cardID"></x-input>
          <x-input title="密码" type="password" v-model="password"></x-input>
        </group>
        <group label-width="4em" label-margin-right="2em" label-align="right">
          <x-button type="primary" @click.native="activate">激活</x-button>
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
      activateShow: false,
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
            'icon': 'icon-tiyu2'
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
  computed: {
  },
  methods: {
    log_in_out () {
      console.log('login')
    },
    orderTimeChange (val) {
      if (val < this.now) {
        this.$vux.alert.show({
          title: '提示',
          content: '中午的订单需要在十点之前预定，下午的订单需要在下午三点之前预定哦'
        })
        this.$nextTick(() => {
          this.orderTime = this.now.toString()
        })
      } else {
        this.$store.commit('changeOrderTime', val)
      }
    },
    activate () {
      var _this = this
      this.$vux.loading.show({
        text: '验证一卡通中...'
      })
      this.$http.post('/api/activate', {
        id: this.$store.state.account.id,
        cardID: this.cardID,
        password: this.password
      })
      .then((response) => {
        this.$vux.loading.hide()
        if (response.data.status !== 'failed') {
          _this.$store.commit('login', response.data)
          this.$vux.alert.show({
            title: _this.$store.state.account.studentName + '谢谢你',
            content: '已成功绑定一卡通 可以订餐了',
            onShow () {
            },
            onHide () {
              console.log(response)
              _this.activateShow = false
              _this.getFoods()
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
      .catch(function (response) {
        this.$vux.alert.show({
          title: '提示',
          content: '一卡通绑定失败 请重新尝试 失败原因' + response.data,
          onShow () {
          },
          onHide () {
            console.log(response)
          }
        })
      })
    },
    doLogin () {
      var _this = this
      console.log(this.$route.query.code)
      if (this.$route.query.code === undefined) {
        window.location.href = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf6081fd49106fe2b&redirect_uri=https%3a%2f%2fermei.shuhelper.cn%2f%23%2fhome&response_type=code&scope=snsapi_base&state=123#wechat_redirect'
        return
      }
      this.$http.get('/api/getid?code=' + this.$route.query.code)
      .then((response) => {
        _this.$store.commit('login', response.data)
        while (_this.$store.state.account.credit === 0) {
          this.$vux.alert.show({
            title: '提示',
            content: '您因多次未按时取订单而被封禁',
            onShow () {
            },
            onHide () {
            }
          })
        }
        _this.getFoods()
        if (!_this.$store.state.account.isRegistered) {
          this.$vux.alert.show({
            title: '提示',
            content: '使用前需要先绑定一卡通~',
            onShow () {
            },
            onHide () {
              _this.activateShow = true
            }
          })
        }
      })
      .catch(function (response) {
        console.log(response)
      })
    },
    resetScroller () {
      this.$nextTick(() => {
        this.$refs.cartscroller.reset({
        })
      })
    },
    total: function () {
      var total = 0
      var foods = this.$store.state.foods
      for (var id in foods) {
        if (foods[id].amount !== 0) {
          total += foods[id].amount * (foods[id].price - foods[id].discount)
        }
      }
      return total
    },
    selectSpecification (specification) {
      this.$store.commit('setSpecification', { id: this.currentFood.id, specification: specification })
      this.selectSpecificationShow = false
    },
    amountChange (id, amount) {
      if (this.$store.state.foods[id].specifications.length !== 0 && this.$store.state.foods[id].amount === 0 && amount === 1) {
        this.currentFood = this.$store.state.foods[id]
        this.selectSpecificationShow = true
      }
      if (amount === 0) {
        this.$store.commit('clearSpecification', id)
      }
      this.$store.commit('updateFoodsVal', {id: id, amount: amount})
      var cart = {
        isempty: true,
        foods: {}
      }
      for (var i in this.$store.state.foods) {
        if (this.$store.state.foods[i].amount !== 0) {
          cart.isempty = false
          cart.foods[i] = this.$store.state.foods[i]
        }
      }
      this.cart = cart
      this.resetScroller()
    },
    getFoods () {
      this.$http.get('/api/foods')
                .then((response) => {
                  this.$store.commit('updateFoods', response.data)
                  this.$nextTick(() => {
                    this.$refs.foodscroller.reset({
                      top: 0
                    })
                  })
                })
                .catch(function (response) {
                  console.log(response)
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
