<template>
  <q-card>
    <q-card-main style="text-align:center;">
      <q-item>
        <q-item-side style="text-align:center;display:flex;">          <q-icon color="primary" name="fa-xiangtongfangjianrenwu" style="font-size:2rem;" />
        </q-item-side>
        <q-item-main>
          <q-item-tile label>现在共有{{count}}间空教室</q-item-tile>
          <q-item-tile sublabel>其实不一定准确，结果仅供参考</q-item-tile>
        </q-item-main>
      </q-item>
    </q-card-main>
    <q-card-separator/>
    <q-card-actions>
      <q-collapsible dense class="full-width " style="padding:0 !important;" label="查看全部空教室">
        <q-card flat class="no-margin">
          <!-- <q-card-main> -->
          <q-select :options="campus" v-model="time.campus" float-label="校区" class="full-width"></q-select>
          <div v-if="count">
            <q-collapsible dense class="full-width "  v-for="building in rooms" :key="building" style="padding:0 !important;" :label="building[0][0]">
              <q-card-main class="py-0">
                <span v-for="room in rooms[building[0][0]]" :key="room">{{ room + ' '}}</span>
              </q-card-main>
             </q-collapsible>
          </div>
          <div v-else>
            <q-card flat>
              <q-card-title>该时间没有任何可用教室</q-card-title>
            </q-card>
          </div>
          <!-- </q-card-main> -->
        </q-card>
      </q-collapsible>
    </q-card-actions>
  </q-card>
</template>

<script>
export default {
  data() {
    return {
      campus: [
        {
          label: '本部',
          value: '本部'
        },
        {
          label: '延长',
          value: '延长'
        },
        {
          label: '嘉定',
          value: '嘉定'
        }
      ],
      weeks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      days: [1, 2, 3, 4, 5],
      courses: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
      rooms: {},
      time: {
        campus: '本部',
        week: '',
        day: '',
        course: ''
      },
      count: 0
    }
  },
  watch: {
    time: {
      handler: function(val, oldval) {
        this.getEmptyRooms(val)
      },
      deep: true
    }
  },
  created() {
    this.$http.get('/api/time/').then(response => {
      this.time.week = response.data.week
      this.time.day = response.data.day
      this.time.course = response.data.course
      // this.time.week = 1
      // this.time.day = 1
      // this.time.course = 2
      this.getEmptyRooms(this.time)
    })
  },
  methods: {
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
            // console.log(room[0])
            if (this.rooms[room[0]] === undefined) {
              this.$set(this.rooms, room[0], [])
            }
            // console.log(this.rooms[room[0]])
            this.rooms[room[0]].push(room)
          }
        })
    }
  }
}
</script>

<style>

</style>
