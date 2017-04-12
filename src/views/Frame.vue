<template>
  <div style="height:100%;">
    <iframe style="height:100%;width:100%" :src="'https://static.shuhelper.cn/' + $route.params.name + '.html'"></iframe>
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
