<template lang="pug">
  q-pull-to-refresh(:handler='refresher')
    div(v-if="refresh")
      q-card.namecard(flat='')
        q-card-main
          q-icon(name='room')
            | 宝山
      //- <q-gallery-carousel :src="slider"></q-gallery-carousel>
      q-card.namecard
        q-card-main
          q-item
            q-item-side
              q-spinner-hearts(color='red', :size='30')
            q-item-main
              q-item-tile(label='') {{$store.state.user.name}}，{{welcome}}
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
      course-card
      sport-card(v-if="$store.state.user.cardID!==''")
      //- navigator-card
      //- sport-card(v-if="$store.state.user.cardID!=='' && parseInt($store.state.user.cardID)>=16120000")
      school-bus
      map-card
      random-choice
      //- quote-card
      q-card(flat='')
        q-card-main(style='text-align:center;')
          //- img(src="https://forthebadge.com/images/badges/built-with-love.svg")
          //- br
          small(style='color:grey;') 2018 SHU OpenSourceCommnuity

</template>

<script>
import SportCard from '@/IndexSportCard'
import Weather from '@/IndexWeather'
import CourseTime from '@/IndexCourseTime'
import SimpleCalendar from '@/IndexSimpleCalendar'
import QuoteCard from '@/IndexQuote'
import EmptyRoom from '@/IndexEmptyRoom'
import LeftPanel from '@/LayoutLeftPanel'
import IndexMerryChristmas from '@/IndexMerryChristmas'
import SchoolBus from '@/IndexSchoolBus'
import MapCard from '@/IndexMapCard'
import CourseCard from '@/IndexCourseCard'
import RandomChoice from '@/IndexRandomChoice'
import NavigatorCard from '@/IndexNavigator'
import { QSpinnerHearts } from 'quasar'
// q-gallery-carousel
export default {
  components: {
    Weather,
    CourseTime,
    CourseCard,
    SimpleCalendar,
    QuoteCard,
    EmptyRoom,
    LeftPanel,
    SportCard,
    SchoolBus,
    RandomChoice,
    IndexMerryChristmas,
    NavigatorCard,
    MapCard,
    QSpinnerHearts
  },
  data() {
    return {
      refresh: true
    }
  },
  computed: {
    welcome: function() {
      let d = new Date()
      let str = ''
      let hours = d.getHours()
      let day = d.getDay()
      if (hours <= 2) {
        str = '不睡觉在干嘛'
      } else if (hours <= 5) {
        str = '😰你真的不睡觉吗'
      } else if (hours <= 8) {
        str = '早上好，看看今天的课程吧'
      } else if (hours <= 11) {
        str = '上午好~'
      } else if (hours <= 13) {
        str = '中午好，睡午觉吗'
      } else if (hours <= 18) {
        str = '下午好'
      } else if (hours <= 22) {
        str = '晚上好，早点休息'
      } else if (hours <= 24) {
        str = '夜深了，早点睡吧'
      }
      if (day === 0 || day === 6) {
        str = '今天好像放假来着'
      }
      return str
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
