<template lang="pug">
  div
    q-card.namecard
      q-card-main
        q-item
          q-item-side
            q-icon(color='primary', name='date_range', style='font-size:2rem;')
          q-item-main
            q-item-tile(label='') 今天是{{time.year+ '_'+time.term|term}}，第{{time.week|cnNum}}周，周{{time.day|cnNum}}
            q-item-tile(sublabel='') 新学期加油~
        q-item
          q-item-main
            q-progress(:percentage='((time.week-1)*7 + time.day)/84*100', color='teal-4')
            q-item-tile(sublabel='', style='text-align:center;') 本学期进度 {{((time.week-1)*7 + time.day)}}/84
      q-card-separator
      q-card-actions
        q-btn.full-width(flat @click="open()")
          | 查看本学年校历（图片）
    q-modal(ref="calendar" :content-css="{minWidth: '80vw', minHeight: '80vh'}")
      q-modal-layout
        q-toolbar(slot="header" color="primary")
          q-btn(color="white" flat @click="close")
            q-icon(name="close")
            q-toolbar-title
              | 17-18学年校历
        div(v-if="calendarOpen")
          img.responsive(src="/statics/2017-2018秋.jpg")
          img.responsive(src="/statics/2017-2018冬.jpg")
          img.responsive(src="/statics/2017-2018春.jpg")
          img.responsive(src="/statics/2017-2018夏.jpg")
</template>

<script>
export default {
  name: 'simpleCalendar',
  data() {
    return {
      publication: {},
      calendarOpen: false,
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
    open() {
      this.calendarOpen = true
      this.$refs.calendar.open()
    },
    close() {
      this.calendarOpen = false
      this.$refs.calendar.close()
    },
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
