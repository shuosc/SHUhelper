<template>
  <v-tabs light fixed centered>
    <v-tabs-bar slot="activators" class="grey lighten-3">
      <v-tabs-slider class="primary"></v-tabs-slider>
      <v-tabs-item v-for="(item, index) in items" :key="index"
        :href="'#tab-' + index" class="primary--text">
        {{ item }}
      </v-tabs-item>
    </v-tabs-bar>
    <v-tabs-content :id="'tab-0'" style="height:550px;">
      <!-- <schedule :task-detail="courseSelected"
                                      @showDetail="showDetail"></schedule> -->
    </v-tabs-content>
    <v-tabs-content :id="'tab-1'">
      <!-- <calendar locale="ZH_CN"
                                                                                                                                  campact>
                                                                                                                          <template scope="scope">
                                                                                                                          </template>
                                                                                                                        </calendar> -->
      <calendar-events locale="ZH_CN" style="height:20rem;"
        :events="calendarEvents" :selection="calendarSelection"
        @action="action"></calendar-events>
      <v-card>
        <ul>
          <li v-for="event in calendarEvents" :style="`color:${event.color};`"
            :key="event"> {{event.title}} </li>
        </ul>
      </v-card>
      <!-- <calendar-range :events="calendarEvents" style="width:100%;display:block;" compact 
                                                                                                                                                              locale="ZH_CN"
                                                                                                                                                              :selection="calendarSelection"></calendar-range> -->
    </v-tabs-content>
    <!-- <v-tabs-content v-for="i in items" :key="i" :id="'tab-' + i">
                                                                                                                                                    <v-card flat>
                                                                                                                                                      <v-card-text>{{ text }}</v-card-text>
                                                                                                                                                    </v-card>
                                                                                                                                                  </v-tabs-content> -->
  </v-tabs>
</template>
<script>
import Schedule from '@/components/Schedule'
// import {convertTimeString} from '@/utils'
import { calendar, calendarRange, calendarEvents } from '@/vue-calendar-picker'
export default {
  components: {
    Schedule,
    calendar,
    calendarRange,
    calendarEvents
  },
  data () {
    return {
      items: ['课表', '月历'],
      e1: '',
      fab: false,
      events: {},
      calendarSelection: {
        start: new Date(2000, 4, 2), end: new Date(2000, 4, 7, 12)
      },
      enableCategory: {
        'school_calendar': true,
        'course': false,
        'vacation': false
      },
      range: {
        start: null,
        end: null
      },
      enableSchoolCalendar: {
        year: true,
        term: true,
        week: true
      }
    }
  },
  computed: {
    eventsComputed: function () {
      console.log('computed events')
      return this.events
    },
    calendarEvents: {
      get: function () {
        var randomColor = require('randomcolor')
        var events = []
        for (let id in this.events) {
          let event = this.events[id]
          let category = event.category
          let start = new Date(event.start * 1000)
          let end = new Date(event.end * 1000)
          // console.log(start, end)
          if (this.enableCategory[category]) {
            var endbeforeRange = end.valueOf() <= this.range.start.valueOf()
            var startAfterRange = start.valueOf() >= this.range.end.valueOf()
            // console.log(startBetweenRange,endBetweenRange)
            if (!(endbeforeRange || startAfterRange)) {
              var color = randomColor()
              if (event.key === 'year') {
                color = '#000'
              } else if (event.key === 'term') {

              }
              events.push({
                color: color,
                start: start,
                end: end,
                title: event.title,
                place: event.place,
                category: event.category
              })
            }
          }
        }
        console.log(events, 'computed')
        return events
      },
      set: function (range) {
        this.range.start = range.start
        this.range.end = range.end
        console.log('setter')
      }
    }
  },
  created () {
    this.resetRange()
    // var start = new Date(2017, 1, 1, 0, 0)
    // var end = new Date(2018, 9, 15, 0, 0)
    this.getEvents(this.range.start.valueOf() / 1000, this.range.end.valueOf() / 1000)
  },
  methods: {
    action (ev) {
      if (this.range.start.valueOf() !== ev.range.start.valueOf()) {
        // console.log(this.range.start !== ev.range.start)
        this.range.start = ev.range.start
        this.range.end = ev.range.end
        this.getEvents(this.range.start.valueOf() / 1000, this.range.end.valueOf() / 1000)
        console.log('not equal')
      }
      console.log(this.range)
      console.log(ev)
    },
    resetRange () {
      let now = new Date()
      let start = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      let end = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1)
      this.range.start = start
      this.range.end = end
    },
    getEvents (start, end) {
      this.$http.get('/api/events/', {
        params: {
          start: start,
          end: end
        }
      })
        .then((response) => {
          for (var i in response.data) {
            this.$set(this.events, response.data[i].id, response.data[i])
          }
        })
    }
    // ,
    // selectColor(category){
    //   if(category==='year'){
    //     return
    //   } else if (category === 'term')
    // }
  }
}
</script>
<style>
.calendar {
  /* border: 2px solid #000; */
  width: 100% !important;
  border-radius: 0.5em;
  padding: 0.5em;
}
</style>
