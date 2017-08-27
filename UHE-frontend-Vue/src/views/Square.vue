<template>
  <div>
    <v-tabs light centered grow v-model="e1" style="height:100%;">
      <v-tabs-bar slot="activators" class="grey lighten-3">
        <v-tabs-slider class="primary"></v-tabs-slider>
        <v-tabs-item v-for="(item, index) in items" :key="index" :href="'#tab-' + index" class="primary--text">
          {{ item }}
        </v-tabs-item>
      </v-tabs-bar>
      <!-- v-infinite-scroll="getContent" infinite-scroll-disabled="loading" infinite-scroll-distance="10" -->
      <v-tabs-content :id="'tab-0'">
        <time-line ref="timeLine" @loaded="loaded" @loadingComplete="loadingComplete" @loadingReset="loadingReset"></time-line>
      </v-tabs-content>
      <v-tabs-content :id="'tab-1'">
        <activities></activities>
      </v-tabs-content>
      <v-tabs-content :id="'tab-2'">
        <others></others>
      </v-tabs-content>

    </v-tabs>
    
  </div>
</template>
<script>
import TimeLine from './feed/TimeLine'
import others from '@/views/others'
import activities from '@/views/activities'
// import InfiniteLoading from '@/vue-infinite-loading/src'
export default {
  components: {
    TimeLine,
    others,
    activities
    // InfiniteLoading
  },
  data () {
    return {
      items: ['动态', '活动', '其他'],
      e1: 'tab-0',
      fab: false
    }
  },
  watch: {
    e1: function (val) {
      console.log(val)
      this.loadingReset()
    }
  },
  // beforeRouteLeave (to, from, next) {
  //   console.log(to)
  //   // 导航离开该组件的对应路由时调用
  //   // 可以访问组件实例 `this`
  // },
  methods: {
    getContent () {
      if (this.e1 === 'tab-0') {
        this.$refs.timeLine.getFeeds()
      } else {
        // this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
      }
    },
    loaded () {
      console.log('loaded')
      // this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
    },
    loadingComplete () {
      // this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
    },
    loadingReset () {
      // this.$refs.infiniteLoading.$emit('$InfiniteLoading:reset')
    }
  }
}
</script>
<style>
.tabs__items {
  height: 100% !important;
  /* position: static; */
  /* padding-top:40px; */
  /* clear: both; */
}
</style>
