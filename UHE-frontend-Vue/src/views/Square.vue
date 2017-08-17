<template>
  <div>
    <v-tabs light fixed centered>
      <v-tabs-bar slot="activators" class="grey lighten-3">
        <v-tabs-slider class="primary"></v-tabs-slider>
        <v-tabs-item v-for="(item, index) in items" :key="index" :href="'#tab-' + index" class="primary--text">
          {{ item }}
        </v-tabs-item>
      </v-tabs-bar>
      <v-tabs-content :id="'tab-0'">
        <time-line></time-line>
      </v-tabs-content>
       <v-tabs-content :id="'tab-1'">
        <time-line></time-line>
      </v-tabs-content>
       <v-tabs-content :id="'tab-2'">
        <time-line></time-line>
      </v-tabs-content>
    </v-tabs>
  
  </div>
</template>
<script>
import TimeLine from './feed/TimeLine'
export default {
  components: {
    TimeLine
  },
  data () {
    return {
      items: ['动态', '活动', '其他'],
      e1: '',
      fab: false
    }
  }
}
</script>
<style lang="stylus">

</style>
