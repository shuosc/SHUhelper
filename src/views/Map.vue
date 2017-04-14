<template>
  <div style="height:100%;">
    <iframe style="height:100%;width:100%"
            src="http://static.shuhelper.cn/map.html"></iframe>
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
    }
  },
  computed: {
  },
  methods: {
    resetScroller() {
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
