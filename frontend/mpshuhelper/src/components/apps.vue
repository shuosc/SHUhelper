<template lang="pug">
  div.page__bd
    div.weui-grids.grid
      block(v-for="(item,index) in grids" :key="index")
        navigator(:url='item.url' class="weui-grid" hover-class="weui-grid_active")
          image.weui-grid__icon(:src="item.src")
          div.weui-grid__label {{item.name}}
</template>
<style scoped>

</style>

<script>
export default {
  data() {
    return {
      grids: [
        {
          src: '/static/calendar.png',
          name: '课程表',
          url: '/pages/myCourse/main'
        },
        {
          src: '/static/lostnfound.png',
          name: '失物招领',
          url: '/pages/lost-n-found/main'
        },
        {
          src: '/static/developing.png',
          name: '敬请期待'
          // url: '/pages/room-booking/main'
        },
        {
          src: '/static/developing.png',
          name: '敬请期待'
          // url: '/pages/room-booking/main'
        }
      ]
    }
  }
}
</script>
