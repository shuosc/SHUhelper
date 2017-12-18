<template>
  <q-card class="namecard">
    <q-card-main>
      <q-item>
        <q-item-side>
          <q-icon color="primary" name="date_range" style="font-size:2rem;" />
        </q-item-side>
        <q-item-main>
          <q-item-tile label>今天是{{time.year+ '_'+time.term|term}}，第{{time.week}}周，周{{time.day}}</q-item-tile>
          <q-item-tile sublabel>新学期加油~</q-item-tile>
        </q-item-main>
      </q-item>
      <q-item>
        <q-item-main>
          <q-progress :percentage="((time.week-1)*7 + time.day)/84*100" color="teal-4" />
          <q-item-tile sublabel style="text-align:center;">本学期进度 {{((time.week-1)*7 + time.day)}}/84</q-item-tile>
        </q-item-main>
      </q-item>
    </q-card-main>
    <!-- <q-card-separator />
    <q-card-actions>
      <q-btn flat class="full-width" color="primary">查看校历</q-btn>
    </q-card-actions> -->
  </q-card>
</template>

<script>
export default {
  name: 'simpleCalendar',
  filters: {
    term: function(value) {
      let map = {
        '1': '秋',
        '2': '冬',
        '3': '春',
        '4': '夏'
      }
      let year = parseInt(value.slice(2, 4))
      return `${year}-${year + 1}${map[value[5]]}`
    }
  },
  data() {
    return {
      publication: {},
      time: {
        year: '喵喵喵',
        term: '喵喵喵',
        week: '喵喵喵',
        day: '喵喵喵',
        course: '喵喵喵'
      }
    }
  },
  created() {
    this.getTime()
  },
  methods: {
    zeroPadding(num, digit) {
      var zero = ''
      for (var i = 0; i < digit; i++) {
        zero += '0'
      }
      return (zero + num).slice(-digit)
    },
    getTime() {
      this.$http.get('/api/time/').then(response => {
        this.time.year = response.data.year
        this.time.term = response.data.term
        this.time.week = response.data.week
        this.time.day = response.data.day
        this.time.course = response.data.course
      })
    }
  }
}
</script>

<style>

</style>
