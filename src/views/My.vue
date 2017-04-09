<template>
  <div style="height:100%;">
  <view-box ref="viewBox" body-padding-top="46px" body-padding-bottom="50px">
  <x-header slot="header" title="SHUhelper 2.0 preview" style="width:100%;position:absolute;left:0;top:0;z-index:100;">
  </x-header>
    <scroller lock-x scrollbar-y height="-100" ref="foodscroller">
        <div>
        <group title="账号">
          <cell title="姓名" :value="$store.state.account.name"></cell>
          <cell title="用户名" :value="$store.state.account.nickname"></cell>
          <cell title="学号" :value="$store.state.account.card_id"></cell>
        </group>
        <group title="设置">
          <cell title="帮助" value="还没写"></cell>
          <cell title="关于" value="版本 v2.0.0 Preview"></cell>
        </group>
        <divider>BUILT WITH ❤</divider>
        </div>
    </scroller>
    <div slot="bottom">
     <tabbar>
        <tabbar-item :link="'/'">
            <i class="iconfont icon-dashboard" slot="icon"></i>
            <span slot="label">功能</span>
        </tabbar-item>
        <tabbar-item selected :link="'/my'">
            <i class="iconfont icon-heart" slot="icon"></i>
            <span slot="label">我的</span>
        </tabbar-item>  
    </tabbar>
    </div>
    </view-box>
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
