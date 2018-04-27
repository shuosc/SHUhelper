<template lang="pug">
  div.schedule
    div.time-ground
      div.infobox
      div(v-for="time in timeGround", class="time-row", :key="time.no")
        div#time
          div {{time.start}}
          div(style="color:black;flex-grow:3;") {{time.no}}
          div {{time.end}}
    div.task-ground
      div(v-for="(week,index) in weekGround", class="task-list", :key="week")
        div.week
          p {{week}}
        div.taskListSty
          div(class="task-list-item" 
            v-for="(detail,no) in tasks[index]",:key="no",
            :style="{height:detail.styleObj.height,top:detail.styleObj.top,backgroundColor:detail.styleObj.backgroundColor,}",
            @click="showDetail(detail)")
            div
              p#name {{detail.coursename}}
                br
                | ({{detail.teachname}})
              p @{{detail.place}}
</template>

<script>
import { coursetimeToNum, hashCode } from '@/utils/index.js'
export default {
  name: 'TimeTable',
  props: {
    timeGround: {
      default() {
        return [
          { no: 1, start: '08:00', end: '08:45' },
          { no: 2, start: '08:55', end: '09:40' },
          { no: 3, start: '10:00', end: '10:45' },
          { no: 4, start: '10:55', end: '11:40' },
          { no: 5, start: '12:10', end: '12:55' },
          { no: 6, start: '13:05', end: '13:50' },
          { no: 7, start: '14:10', end: '14:55' },
          { no: 8, start: '15:05', end: '15:50' },
          { no: 9, start: '16:00', end: '16:45' },
          { no: 10, start: '16:55', end: '17:40' },
          { no: 11, start: '18:00', end: '18:45' },
          { no: 12, start: '18:55', end: '19:40' },
          { no: 13, start: '19:50', end: '20:35' }
        ]
      }
    },
    weekGround: {
      type: Array,
      default() {
        return ['周一', '周二', '周三', '周四', '周五']
      }
    },
    courses: {
      type: Array,
      default() {
        return []
      }
    },
    color: {
      type: Array,
      default() {
        return [
          '#4DC7C0',
          '#9BD3C0',
          '#E2E0BA',
          '#FFB3B2',
          '#FF4A9B',
          '#BED1FA',
          '#78FFB5',
          '#7A00CB',
          '#f6b067',
          '#443453',
          '#A2B9B2'
        ]
      }
    }
  },
  data() {
    return {
      showModal: false
    }
  },
  computed: {
    tasks: function() {
      let selected = [[], [], [], [], []]
      for (let i = this.courses.length - 1; i >= 0; i--) {
        let timelist = coursetimeToNum(this.courses[i].time)
        var color = [
          '#2B2E4A',
          '#521262',
          '#903749',
          '#53354A',
          '#40514E',
          '#537780',
          '#3765a4',
          '#76a5a4',
          '#579870',
          '#e391b4',
          '#b8954e'
        ]
        var course = this.courses[i]
        // var rancolor = color[~~(Math.random() * color.length)]
        let colorIndex = hashCode(course.name) % color.length
        let rancolor = color[colorIndex]
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
            place: time.thisWeek ? course.place : course.place + course.time,
            styleObj: {
              height: `${(time.End - time.Start + 1) * 60}px`,
              top: `${(time.Start - 1) * 60}px`,
              backgroundColor: time.thisWeek ? rancolor : '#aaa'
            }
          }
          selected[time.day].push(item)
        }
      }
      return selected
    }
  },
  methods: {
    showDetail(obj) {
      // console.log('showDetail raw')
      this.$emit('showDetail', obj)
    }
  }
}
</script>

<style scoped>
.week {
  height: 30px;
  width: 100%;
}
.week p {
  margin: 0;
  font-size: 1.5rem !important;
}
.schedule {
  width: 100%;
  max-width: 1400px;
  /* margin: 0 auto; */
  position: relative;
  /* padding-left: 4rem; */
  box-sizing: border-box;
}
.infobox {
  height: 30px;
}
.time-ground {
  display: block;
  width: calc(100% - 4rem);
  /* height: 100%; */
  margin-left: 4rem;
}
.time-row {
  height: 60px;
  box-sizing: border-box;
  margin: 0;
}
#time {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: absolute;
  font-size: 0.7rem;
  width: 4rem;
  left: -4rem;
  /* transform:translateY(-15%); */
  /* width: 2rem; */
}
#time > div {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: grey;
}

.time-ground > div {
  position: relative;
  box-sizing: border-box;
  border-bottom-style: solid;
  border-color: #eaeaea;
  border-width: 1px;
}

.time-ground > div div#no {
  /* position: absolute; */
  /* top: 50%; */
  /* text-align: center; */
  /* width: 100%; */
  /* transform: translateY(-50%); */
}

.time-ground > div span:first-of-type {
  position: absolute;
  top: 0;
}

.time-ground > div span:last-of-type {
  position: absolute;
  bottom: 0;
}

.task-ground {
  width: calc(100% - 4rem);
  height: 100%;
  position: absolute;
  left: 4rem;
  top: 0;
}

.task-list {
  float: left;
  width: 20%;
  box-sizing: border-box;
  border-top: 1px solid #eaeaea;
  border-right: 1px solid #eaeaea;
  height: 100%;
  border-color: #eaeaea;
  border-width: 1px;
}

.task-list:first-child {
  float: left;
  width: 20%;
  box-sizing: border-box;
  border-left: 1px solid #eaeaea;
  height: 100%;
  border-color: #eaeaea;
  border-width: 1px;
}
.task-list p {
  text-align: center;
  font-size: 0.9rem;
}

.task-list-item {
  position: absolute;
  background-color: #577f92;
  /* border-bottom: 0.3rem solid #577F92; */
  width: 100%;
  cursor: pointer;
  box-sizing: border-box;
  text-align: center;
  vertical-align: middle;
}

.task-list-item p {
  padding: 0;
  font-size: 1.3rem;
  color: #edf2f6;
  margin-bottom: 0.5rem;
}

.task-list-item #name {
  font-size: 1.2rem;
  font-weight: bold;
  line-height: 2rem;
  /* color: #E0E7E9; */
  color: #e0e7e9;
  margin-bottom: 0.1rem;
  /* padding: 0.1rem; */
  padding-left: 0.3rem;
  padding-right: 0.3rem;
  padding-bottom: 0.5rem;
  padding-top: 1rem;
  text-overflow: ellipsis;
  /* white-space: nowrap; */
  overflow: hidden;
}

ul {
  list-style-type: none;
}

.taskListSty {
  box-sizing: border-box;
  position: relative;
  height: 96.2%;
  width: 100%;
}
</style>
