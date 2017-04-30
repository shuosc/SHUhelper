<template>
  <div>
    <div @click="getSweetie()"
         id="sweetie">{{sweetie}}</div>
    <div v-for="group in functions_groups"
         :key="group.title">
      <group-title>{{group.group_tittle}}</group-title>
      <grid>
        <grid-item style="text-align:center;"
                   :link="item.url"
                   :label="item.tittle"
                   v-for="item in group.functions" v-if="item.visiable"
                   :key="item.title">
          <i slot="icon"
             style="color:#009ACD;font-size:1.5rem;"
             :class="'iconfont ' + item.icon"></i>
        </grid-item>
      </grid>
      </marquee>
    </div>
    <divider>Powered by SHUhelper</divider>
  </div>
</template>

<script>
import { Group, Cell, Tabbar, TabbarItem, XHeader, Divider, Card, XNumber, Flexbox, FlexboxItem, XImg, Scroller, ViewBox, XButton, Popup, Radio, XInput, Checker, CheckerItem, Grid, GridItem, GroupTitle, Marquee, MarqueeItem } from 'vux'

//  {
//           'group_tittle': '分流专题',
//           'functions': [{
//             'tittle': '学院分流QQ群',
//             'icon': 'icon-graduation-cap',
//             'url': '/query/tiyu'
//           }, {
//             'tittle': '往年分流排名',
//             'icon': 'icon-kaoshi',
//             'url': '/query/tiyu'
//           }, {
//             'tittle': '分流信息网',
//             'icon': 'icon-dili',
//             'url': '/query/tiyu'
//           }, {
//             'tittle': '分流政策',
//             'icon': 'icon-book',
//             'url': '/query/tiyu'
//           }]
// //         },
//  {
//             'tittle': '物理实验',
//             'icon': 'icon-07',
//             'url': '/query/phylab'
//           },
//  {
//           'tittle': '表白墙',
//           'icon': 'icon-heart',
//           'url': 'http://mp.weixin.qq.com/s/nT92e0XVFZHJ8XSpV9qtuQ'
//         }, {
//           'tittle': '留言板',
//           'icon': 'icon-kaoshi',
//           'url': '/messageboard'
//         }, {
//           'tittle': '匿名讨论版',
//           'icon': 'icon-comment-o',
//           'url': 'http://mp.weixin.qq.com/s/nT92e0XVFZHJ8XSpV9qtuQ'
//         },

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
  data() {
    return {
      value: 1,
      sweetie: '“There are no happy endings. Endings are the saddest part, So just give me a happy middle....And a very happy start.”',
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
          'url': 'https://old.shuhelper.cn/',
          'visiable': false
        }, {
          'tittle': '空教室查询',
          'icon': 'icon-xiangtongfangjianrenwu',
          'url': '/classrooms',
          'visiable': true
        }, {
          'tittle': '都有空吗',
          'icon': 'icon-group',
          'url': '/findfreetime',
          'visiable': true
        }, {
          'tittle': '一键退学',
          'icon': 'icon-drivers-license-o',
          'url': 'https://old.shuhelper.cn/login/vali/quit',
          'visiable': false
        }, {
          'tittle': '尔美西餐厅预定',
          'icon': 'icon-dppj',
          'url': 'http://mp.weixin.qq.com/s/nT92e0XVFZHJ8XSpV9qtuQ',
          'visiable': true
        }, {
          'tittle': '留言板',
          'icon': 'icon-kaoshi',
          'url': '/messageboard',
          'visiable': true
        }, {
          'tittle': '排课助手(PC)',
          'icon': 'icon-paw',
          'url': 'http://xk.shuhelper.cn/',
          'visiable': true
        }, {
          'tittle': '本学期课程查询',
          'icon': 'icon-book',
          'url': '/courses',
          'visiable': true
        }, {
          'tittle': '树洞',
          'icon': 'icon-shu',
          'url': '/woods-hole',
          'visiable': true
        }, {
          'tittle': '校园安全地图',
          'icon': 'icon-baoan-copy',
          'url': '/security-map',
          'visiable': true
        }, {
          'tittle': '陆续上线中...',
          'icon': 'icon-certificate',
          'visiable': true
        }]
      }, {
        'group_tittle': '常用查询',
        'functions': [{
          'tittle': '晨跑课外活动',
          'icon': 'icon-tiyu2',
          'url': '/query/tiyu',
          'visiable': true
        }, {
          'tittle': '课外活动时间表',
          'icon': 'icon-tiyu1',
          'url': '/frame/activities',
          'visiable': true
        }, {
          'tittle': '校历',
          'icon': 'icon-rili',
          'url': '/frame/cal',
          'visiable': true
        }, {
          'tittle': '课表',
          'icon': 'icon-course-table',
          'url': '/query/xk',
          'visiable': true
        }, {
          'tittle': '成绩',
          'icon': 'icon-tubiaozhizuomoban',
          'url': '/query/cj',
          'visiable': true
        }, {
          'tittle': '校园地图',
          'icon': 'icon-map-o',
          'url': '/frame/map',
          'visiable': true
        }, {
          'tittle': '体育场馆地图',
          'icon': 'icon-map',
          'url': '/frame/pemap',
          'visiable': true
        }, {
          'tittle': '就医指导',
          'icon': 'icon-yiyuan',
          'url': '/frame/med',
          'visiable': true
        }, {
          'tittle': '电话黄页',
          'icon': 'icon-huangye',
          'url': '/frame/tel',
          'visiable': true
        }, {
          'tittle': '校车运行',
          'icon': 'icon-bus',
          'url': '/frame/bus',
          'visiable': true
        }, {
          'tittle': '场馆开放',
          'icon': 'icon-icon',
          'url': '/frame/serviceschedule',
          'visiable': true
        }, {
          'tittle': '机房开放',
          'icon': 'icon-desktop',
          'url': '/frame/freelab',
          'visiable': true
        }, {
          'tittle': '一卡通余额流水',
          'icon': 'icon-icon1',
          'url': '/query/lehu',
          'visiable': true
        }, {
          'tittle': '财务缴费',
          'icon': 'icon-money',
          'url': '/query/fin',
          'visiable': true
        }, {
          'tittle': '陆续上线中...',
          'icon': 'icon-certificate',
          'visiable': true
        }]
      }
      ]
    }
  },
  created: function () {
    if (localStorage.getItem('loginstate') !== null && this.$store.state.account.token === '') {
      this.verifyToken()
    }
    this.getSweetie()
  },
  computed: {
  },
  methods: {
    getSweetie() {
      this.$http.get('/api/sweetie')
        .then((response) => {
          this.sweetie = response.data
        })
    },
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
      console.log('logout')
    },
    verifyToken() {
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
    resetScroller() {
      this.$nextTick(() => {
        this.$refs.scroller.reset({
        })
      })
    }
  }
}
</script>

<style>
#sweetie {
  color: #fff;
  border-radius: 15px;
  margin: 10px;
  padding: 5px;
  font-size: 0.8rem;
  background-color: rgba(83, 134, 139, 0.70);
  text-shadow: 0px 0px 0px #000;
  text-align: center;
}
</style>
