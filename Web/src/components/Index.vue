<template lang="pug">
  q-pull-to-refresh(:handler='refresher')
    div(v-if="refresh")
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
      // q-card.no-margin
        q-card-title.text-center.full-width.no-margin(flat style="padding-bottom:0;")
          q-icon(name="card_giftcard")
          | 圣诞快乐&元旦快乐
        index-merry-christmas
        q-btn.full-width(@click="$router.push('/2018')")
          | 写下你的新年愿望
      course-time(v-if="$store.state.time.day<=5")
      empty-room(v-if="$store.state.time.updated&&$store.state.time.day<=5")
      sport-card(v-if="$store.state.user.cardID!=='' && parseInt($store.state.user.cardID)>=16120000")
      //- sport-card(v-if="$store.state.user.cardID!=='' && parseInt($store.state.user.cardID)>=16120000")
      school-bus
      map-card
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
import IndexMerryChristmas from '@/IndexMerryChristmas'
import SchoolBus from '@/IndexSchoolBus'
import MapCard from '@/IndexMapCard'
import { QSpinnerHearts } from 'quasar'
export default {
  components: {
    Weather,
    PullTo,
    CourseTime,
    SimpleCalendar,
    QuoteCard,
    EmptyRoom,
    LeftPanel,
    SportCard,
    SchoolBus,
    IndexMerryChristmas,
    MapCard,
    QSpinnerHearts
  },
  data() {
    return {
      refresh: true
    }
  },
  methods: {
    refresher(done) {
      this.refresh = false
      this.$nextTick(() => {
        this.refresh = true
      })
      done()
    }
  }
}
</script>

<style lang="stylus" scoped>
.namecard
  transform translateZ(0)
  opacity 0.9
  // background #EDE574 /* fallback for old browsers */
  // background -webkit-linear-gradient(to left, #E1F5C4, #EDE574) /* Chrome 10-25, Safari 5.1-6 */
  // background linear-gradient(to left, #E1F5C4, #EDE574) /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
</style>
