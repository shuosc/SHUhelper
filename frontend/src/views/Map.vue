<template>
  <div style="height:100%;">
    <iframe style="height:100%;width:100%"
            src="http://static.shuhelper.cn/map.html"></iframe>
  </div>
</template>

<script>

export default {
  components: {},
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
