<template lang="pug">
  q-pull-to-refresh(:handler='refresher')
    //- q-scroll-area.window-height
    //- pull-to(:top-load-method="refresher" :is-bottom-bounce="false" :is-top-bounce="false")
    q-card.namecard(flat='')
      q-card-main
        q-icon(name='room')
          | 宝山
    q-card.namecard
      q-card-main
        q-item
          q-item-side
            q-spinner-hearts(color='red', :size='30')
          q-item-main
            q-item-tile(label='') {{$store.state.user.name}}，我们为你准备了这些
    simple-calendar
    course-time
    empty-room(v-if="$store.state.time.updated")
    sport-card
    quote-card
    q-card(flat='')
      q-card-main(style='text-align:center;')
        //- img(src="https://forthebadge.com/images/badges/built-with-love.svg")
        //- br
        small(style='color:grey;') 2017 SHU OpenSourceCommnuity

</template>

<script>
import SportCard from '@/IndexSportCard'
import PullTo from 'vue-pull-to'
import Weather from '@/IndexWeather'
import CourseTime from '@/IndexCourseTime'
import SimpleCalendar from '@/IndexSimpleCalendar'
import QuoteCard from '@/IndexQuote'
import EmptyRoom from '@/IndexEmptyRoom'
import LeftPanel from '@/LayoutLeftPanel'
export default {
  components: {
    Weather,
    PullTo,
    CourseTime,
    SimpleCalendar,
    QuoteCard,
    EmptyRoom,
    LeftPanel,
    SportCard
  },
  methods: {
    refresher(done) {
      done()
    }
  }
}
</script>

<style lang="stylus" scoped>
.namecard {
  transform: translateZ(0);
  opacity: 0.9;
  // background #EDE574 /* fallback for old browsers */
  // background -webkit-linear-gradient(to left, #E1F5C4, #EDE574) /* Chrome 10-25, Safari 5.1-6 */
  // background linear-gradient(to left, #E1F5C4, #EDE574) /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
</style>
