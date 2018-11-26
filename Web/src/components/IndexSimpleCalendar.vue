<template lang="pug">
  div
    q-card.namecard
      q-card-main
        q-item
          q-item-side
            q-icon(color='primary', name='date_range', style='font-size:2rem;')
          q-item-main
            q-item-tile(label='') 今天是{{time.year+ '_' + time.term|term}}，第{{time.week|cnWeek}}周，周{{time.day|cnWeekDay}}
            q-item-tile(sublabel='') 今天努力学习了吗
        q-item
          q-item-main
            q-progress(:percentage='((time.week-1)*7 + time.day)/84*100', color='teal-4')
            q-item-tile(sublabel='', style='text-align:center;') 本学期进度 {{((time.week-1)*7 + time.day)}}/84
      q-card-separator
      q-card-actions
        q-btn.full-width(flat @click="open()")
          | 查看本学年校历
    q-modal(ref="calendar" :content-css="{minWidth: '80vw', minHeight: '80vh'}")
      q-modal-layout
        q-toolbar(slot="header" color="primary")
          q-btn(color="white" flat @click="close")
            q-icon(name="close")
            q-toolbar-title
              | 17-18学年校历
        div(v-if="calendarOpen")
          img.responsive(src="/statics/2018-2019-1.jpeg")
          img.responsive(src="/statics/2018-2019-2.jpeg")
          //- calender
</template>

<script>
  import {mapState} from 'vuex'
  import {QProgress} from 'quasar'
  import Calender from './Calender/Calender'

  export default {
    components: {
      Calender,
      QProgress
    },
    name: 'simpleCalendar',
    data() {
      return {
        publication: {},
        calendarOpen: false
      }
    },
    computed: mapState(['time']),
    created() {
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
      }
    }
  }
</script>

<style>

</style>
