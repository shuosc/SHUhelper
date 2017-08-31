<template>
  <div style="height:700px; padding-top:10px;">
    <!-- <v-tabs light fixed centered :scrollable="false">
                    <v-tabs-bar class="white">
                      <v-tabs-slider class="primary"></v-tabs-slider>
                      <v-tabs-item v-for="(item, index) in items" :key="index" :href="'#tab-' + index" class="primary--text">
                        {{ item }}
                      </v-tabs-item>
                    </v-tabs-bar>
                    <v-tabs-items>
                      <v-tabs-content :id="'tab-0'" style="height:600px;" lazy> -->

    <schedule :task-detail="tasks" @showDetail="showDetail"></schedule>
    <popup v-model="popupVisible" popup-transition="popup-fade">
      <v-card style="width:300px;">
        <v-card-title class="py-0">
          <h4 class="pa-0 teal--text ma-0" style="text-align:center; font-size:1rem;">{{popupContent.name}}
            <span class="grey--text" style="font-size:0.8rem;">{{popupContent.no}}
            </span>
          </h4>
        </v-card-title>
        <v-card-text class="pa-2" style="font-size:1rem !important;">
          <cell title="学分">
            {{popupContent.credit}}</cell>
          <cell title="教师名">{{popupContent.teacher}}({{popupContent.teacher_no}})
          </cell>
          <cell title="时间">
            <p class="ma-0" style="font-size:0.8rem;">{{popupContent.time}}</p>
          </cell>
          <cell title="地点">
            {{popupContent.place}}</cell>
          <cell title="答疑时间">
            {{popupContent.q_time}}</cell>
          <cell title="答疑地点">
            {{popupContent.q_place}}</cell>
        </v-card-text>
        <v-card-actions>
          <v-btn flat block class="orange--text" @click="getID()">前往课程主页</v-btn>
        </v-card-actions>
      </v-card>
    </popup>
    <data-status @renewData="renewCourse" :status="status"></data-status>
    <!-- </v-tabs-content> -->
    <!-- <v-tabs-content :id="'tab-1'" lazy>

                        <calendar-events locale="ZH_CN" style="height:20rem;" :events="calendarEvents" :selection="calendarSelection" @action="action"></calendar-events>
                        <v-card>
                          <ul>
                            <li v-for="event in calendarEvents" :style="`color:${event.color};`" :key="event"> {{event.title}} </li>
                          </ul>
                        </v-card>
                      </v-tabs-content> -->
    <!-- </v-tabs-items>
                    </v-tabs-content>
                  </v-tabs> -->
  </div>
</template>
<script>
import { decrypt } from '@/libs/utils.js'
import Schedule from '@/components/Schedule'
import dataStatus from '@/components/dataStatus'
import { Popup, Cell } from 'mint-ui'
// import {convertTimeString} from '@/utils'
import { calendar, calendarRange, calendarEvents } from '@/vue-calendar-picker'
const CNNUM = {
  '一': 1,
  '二': 2,
  '三': 3,
  '四': 4,
  '五': 5
}
export default {
  components: {
    Schedule,
    calendar,
    calendarRange,
    calendarEvents,
    Popup,
    Cell,
    dataStatus
  },
  data () {
    return {
      popupVisible: false,
      popupContent: '',
      // items: ['课表'],
      e1: '',
      status: {
        lastModified: null,
        status: 'loading',
        remark: '17学年秋季学期课程，信息来自教务网，如果你还没有选课，会看到错误'
      },
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
      },
      courses: [],
      active: null
    }
  },
  computed: {
    tasks: function () {
      console.log('courseSelected')
      var selected = [[], [], [], [], []]
      for (var i = this.courses.length - 1; i >= 0; i--) {
        var timelist = this.coursetimeToNum(this.courses[i].time)
        var color = [
          '#2B2E4A',
          '#521262',
          '#903749',
          '#53354A',
          '#40514E',
          '#537780'
        ]
        var course = this.courses[i]
        var rancolor = color[~~(Math.random() * color.length)]
        for (var j = timelist.length - 1; j >= 0; j--) {
          var time = timelist[j]
          var item = {
            day: time.day,
            Start: time.Start,
            End: time.End,
            coursename: course.name,
            courseno: course.no,
            teachname: course.teacher,
            teachno: course.teach_no,
            place: course.place,
            styleObj: {
              height: (time.End - time.Start + 1) * 7.7 + '%',
              top: ((time.Start - 1) * 7.69) + '%',
              backgroundColor: rancolor
            }
          }
          selected[time.day].push(item)
        }
      }
      return selected
    },
    eventsComputed: function () {
      // console.log('computed events')
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
    this.getCourses()
    // var start = new Date(2017, 1, 1, 0, 0)
    // var end = new Date(2018, 9, 15, 0, 0)
    this.getEvents(this.range.start.valueOf() / 1000, this.range.end.valueOf() / 1000)
  },
  methods: {
    showDetail (obj) {
      for (let i in this.courses) {
        if (this.courses[i].no === obj.courseno) {
          this.popupContent = this.courses[i]
        }
      }
      this.popupVisible = true
    },
    getID () {
      this.$http.get('/api/courses/', {
        params: {
          id: true,
          no: this.popupContent.no,
          teacher: this.popupContent.teacher
        }
      })
        .then((response) => {
          this.$router.push(`/courses/${response.data.id}`)
        })
    },
    coursetimeToNum (time) {
      var patt = /([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*/
      var timelist = []
      var str = time
      while (patt.test(str)) {
        var coursetime = patt.exec(str)
        str = str.replace(patt, '')
        var item = {
          day: parseInt(CNNUM[coursetime[1]] - 1),
          Start: parseInt(coursetime[2]),
          End: parseInt(coursetime[3])
        }
        timelist.push(item)
      }
      return timelist
    },
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
    getCourses () {
      // this.$store.commit('showSnackbar', { text: `查询课表中` })
      this.$http.get('/api/my-course/')
        .then((response) => {
          this.status.status = response.data.status
          this.status.time = response.data.last_modified.$date
          this.courses = decrypt(response.data.data, this.$store.state.user.password)
        })
        .catch((err) => {
          if (err.response.status === 404) {
            this.renewCourse()
          } else {
            this.status.status = 'failed'
            this.$store.commit('showSnackbar', { text: `更新失败${err.response.status}` })
          }
        })
    },
    renewCourse () {
      this.status.status = 'loading'
      this.$store.commit('showSnackbar', { text: `更新课表数据中...` })
      this.$http.post('/api/my-course/sync', {
        'card_id': this.$store.state.user.cardID,
        'password': this.$store.state.user.password
      })
        .then((response) => {
          this.getCourses()
        }).catch((err) => {
          this.status.status = 'failed'
          console.log(err)
        })
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

.mint-cell-wrapper {
  font-size: 1rem;
}

.mint-cell {
  min-height: 3rem;
}
</style>
