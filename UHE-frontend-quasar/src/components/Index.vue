<template>
  <q-pull-to-refresh :handler="refresher" style="height:100vh;">
    <q-card flat class="namecard">
      <q-card-main>
        <q-icon name="room" /> 宝山
      </q-card-main>
    </q-card>
    <q-card class="namecard">
      <q-card-main>
        <q-item>
          <q-item-side>
            <q-spinner-hearts color="red" :size="30" />
          </q-item-side>
          <q-item-main>
            <q-item-tile label>{{$store.state.user.name}}，我们为你准备了这些</q-item-tile>
          </q-item-main>
        </q-item>
      </q-card-main>
    </q-card>
    <simple-calendar/>
    <course-time/>
    <empty-room/>
    <quote-card/>
    <q-card flat>
      <q-card-main style="text-align:center;">
        <img src="https://forthebadge.com/images/badges/built-with-love.svg">
        <br/>
        <small>2017 SHU OpenSourceCommnuity</small>
      </q-card-main>
    </q-card>
  </q-pull-to-refresh>
</template>

<script>
import Weather from '@/IndexWeather'
import CourseTime from '@/IndexCourseTime'
import SimpleCalendar from '@/IndexSimpleCalendar'
import QuoteCard from '@/IndexQuote'
import EmptyRoom from '@/IndexEmptyRoom'
import LeftPanel from '@/LayoutLeftPanel'
export default {
  components: {
    Weather,
    CourseTime,
    SimpleCalendar,
    QuoteCard,
    EmptyRoom,
    LeftPanel
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
  opacity: 0.9;
  // background #EDE574 /* fallback for old browsers */
  // background -webkit-linear-gradient(to left, #E1F5C4, #EDE574) /* Chrome 10-25, Safari 5.1-6 */
  // background linear-gradient(to left, #E1F5C4, #EDE574) /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
</style>
