<template>
  <div style="height:100%;">
  <view-box ref="viewBox" body-padding-top="46px" body-padding-bottom="0px">
    <x-header slot="header" title="SHUhelper 2.0 preview" style="width:100%;position:absolute;left:0;top:0;z-index:100;">
    </x-header>
    <iframe style="height:100%;width:100%" :src="'https://old.shuhelper.cn/' + $route.params.name"></iframe>
    </view-box>
  </div>
</template>

<script>
import { XHeader, ViewBox } from 'vux'

export default {
  components: {
    XHeader,
    ViewBox
  },
  data () {
    return {
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
