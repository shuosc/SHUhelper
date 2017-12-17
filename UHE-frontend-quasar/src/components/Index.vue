<template>
  <q-pull-to-refresh :handler="refresher" style="height:100vh;">
    <q-scroll-area class="full-width full-height" style="height:100vh;">
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
          <img src="http://forthebadge.com/images/badges/built-with-love.svg">
          <br/>
          <small>2017 SHU OpenSourceCommnuity</small>
        </q-card-main>
      </q-card>
    </q-scroll-area>
  </q-pull-to-refresh>

</template>

<script>
import Weather from '@/IndexWeather'
import CourseTime from '@/IndexCourseTime'
import SimpleCalendar from '@/IndexSimpleCalendar'
import QuoteCard from '@/IndexQuote'
import EmptyRoom from '@/IndexEmptyRoom'
export default {
  components: {
    Weather,
    CourseTime,
    SimpleCalendar,
    QuoteCard,
    EmptyRoom
  },
  methods: {
    refresher(done) {
      done()
    }
  }
}
</script>

<style>

</style>
