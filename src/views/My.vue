<template>
  <div style="height:100%;">
    <scroller lock-x
              scrollbar-y
              height="-100"
              ref="scroller">
      <div>
        <group title="账号">
          <cell title="姓名"
                :value="$store.state.account.name"></cell>
          <cell title="用户名"
                :value="$store.state.account.nickname"></cell>
          <cell title="学号"
                :value="$store.state.account.card_id"></cell>
        </group>
        <group title="设置">
          <cell title="帮助"
                value="还没写"></cell>
          <cell title="关于"
                value="版本 v2.0.0 Preview"></cell>
          <cell title="微信公众号"
                value="搜索添加:shuhelper"></cell>
        </group>
        <divider>BUILT WITH ❤</divider>
      </div>
    </scroller>
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
  data() {
    return {
      value: 1,
      show: false,
      activateShow: false,
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
        'group_tittle': '常用功能',
        'functions': [{
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }, {
          'tittle': '体育',
          'icon': 'ico'
        }]
      }]
    }
  },
  computed: {
  },
  methods: {
  }
}
</script>

<style>

</style>
