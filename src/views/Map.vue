<template>
  <div style="height:100%;">
  <view-box ref="viewBox" body-padding-top="46px" body-padding-bottom="0px">
    <x-header slot="header" title="SHUhelper 2.0 preview" style="width:100%;position:absolute;left:0;top:0;z-index:100;">
    <div slot="right">登录</div>
    </x-header>
    <iframe style="height:100%;width:100%" src="http://static.shuhelper.cn/map.html"></iframe>
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
    }
  },
  computed: {
  },
  methods: {
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

</style>
