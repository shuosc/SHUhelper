<template>
  <div>
    <v-tabs light centered grow>
      <v-tabs-bar slot="activators" class="grey lighten-3"  >
        <v-tabs-slider class="primary" ></v-tabs-slider>
        <v-tabs-item v-for="(item, index) in items" :key="index" :href="'#tab-' + index" class="primary--text">
          {{ item }}
        </v-tabs-item>
      </v-tabs-bar>
      <v-tabs-content :id="'tab-0'" >
        <time-line></time-line>
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
export default {
  components: {
    TimeLine,
    others,
    activities
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
<style>
.tabs__items{
   /* height:100% !important;  */
  /* position: static; */
  /* padding-top:40px; */
  /* clear: both; */
}
</style>
