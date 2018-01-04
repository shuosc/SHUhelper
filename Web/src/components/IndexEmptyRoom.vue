<template lang="pug">
  q-card
    q-card-main.text-center
      q-item
        q-item-side.text-center.flex
          q-icon(color='primary', name='fa-xiangtongfangjianrenwu', style='font-size:2rem;')
        q-item-main
          q-item-tile(label) 现在共有{{count}}间空教室
          q-item-tile(sublabel) 其实不一定准确，结果仅供参考
    q-card-separator
    q-card-actions
      q-btn.full-width(style='padding:0 !important;' flat @click="emptyRoom=true")
        | 查看全部空教室
    q-modal(ref="emptyRoomModal" v-model="emptyRoom" :content-css="{minWidth: '80vw', minHeight: '80vh'}")
      q-modal-layout
        q-toolbar(slot="header" color="primary")
          q-btn(color="white" flat @click="emptyRoom=false")
            q-icon(name="close")
            q-toolbar-title
              | 空教室查询
        q-card(flat)
          div.flex.row
            q-select.col-3(:options='campus', v-model='time.campus', float-label='校区')
            q-select.col-3(:options='weeks', v-model='time.week', float-label='周')
            q-select.col-3(:options='days', v-model='time.day', float-label='星期')
            q-select.col-3(:options='courses', v-model='time.course', float-label='节')
          q-card(flat)
            q-card-main.text-center
              | 这时共有{{count}}间空教室
          div(v-if='count')
            q-collapsible.full-width(opened dense='', v-for='building in rooms', :key='building[0][0]', style='padding:0 !important;', :label='building[0][0]')
              q-card-main.py-0
                span(v-for='(room,index) in rooms[building[0][0]]', :key='index') {{ room + ' '}}
          div(v-else='')
            q-card.text-center(flat='')
              q-card-title 啊 现在一间空教室都没有呢

</template>

<script>
function listToSelect(l) {
  return l.map(x => {
    return { label: x, value: x }
  })
}
const campus = listToSelect(['本部', '延长', '嘉定'])
const weeks = listToSelect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
const days = listToSelect([1, 2, 3, 4, 5])
const courses = listToSelect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
export default {
  data() {
    return {
      emptyRoom: false,
      campus: campus,
      weeks: weeks,
      days: days,
      courses: courses,
      rooms: {},
      time: {
        campus: '本部',
        week: '',
        day: '',
        course: ''
      },
      inited: false,
      count: 0
    }
  },
  watch: {
    time: {
      handler: function(val, oldval) {
        if (this.inited) {
          this.getEmptyRooms(val)
        }
      },
      deep: true
    }
  },
  created() {
    this.getEmptyRoomsNow()
  },
  methods: {
    getEmptyRoomsNow() {
      this.rooms = {}
      this.$http.get('/api/empty-room/').then(response => {
        this.count = response.data.rooms.length
        this.$store.commit('updateTime', response.data.time)
        this.time.week = this.$store.state.time.week
        this.time.day = this.$store.state.time.day
        this.time.course = this.$store.state.time.course
        this.$nextTick(() => (this.inited = true))
        for (let room of response.data.rooms) {
          if (this.rooms[room[0]] === undefined) {
            this.$set(this.rooms, room[0], [])
          }
          this.rooms[room[0]].push(room)
        }
      })
    },
    getEmptyRooms(time) {
      this.rooms = {}
      this.$http
        .get('/api/empty-room/', {
          params: {
            campus: time.campus,
            week: time.week,
            day: time.day,
            course: time.course
          }
        })
        .then(response => {
          this.count = response.data.rooms.length
          for (let room of response.data.rooms) {
            if (this.rooms[room[0]] === undefined) {
              this.$set(this.rooms, room[0], [])
            }
            this.rooms[room[0]].push(room)
          }
        })
    }
  }
}
</script>

<style>

</style>
