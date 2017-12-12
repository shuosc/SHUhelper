<template>
  <div>
    <v-subheader>当前学期 16-17冬</v-subheader>
    <v-card class="grey lighten-4 elevation-0">
      <!-- <v-card-text> -->
      <v-container fluid class="py-0 px-2">
        <v-layout row wrap>
          <v-flex xs3>
            <v-select v-bind:items="campus" v-model="time.campus" label="校区" bottom hide-details></v-select>
          </v-flex>
          <v-flex xs3>
            <v-select v-bind:items="weeks" v-model="time.week" label="周" bottom hide-details></v-select>
          </v-flex>
          <v-flex xs3>
            <v-select v-bind:items="days" v-model="time.day" label="星期" bottom hide-details></v-select>
          </v-flex>
          <v-flex xs3>
            <v-select v-bind:items="courses" v-model="time.course" label="节" bottom hide-details></v-select>
          </v-flex>
          <v-flex xs12>
            <v-btn primary block @click.native="getEmptyRooms(time)">查询空教室~</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
      <!-- </v-card-text> -->
    </v-card>
    <div v-if="count">
      <v-card v-for="building in ['A','B','C','D','E','F','G','计','通']" :key="building" class="grey lighten-4">
        <v-card-title>{{building}}</v-card-title>
        <v-card-text class="py-0">
          <span v-for="room in rooms[building]" :key="room">{{ room + ' '}}</span>
        </v-card-text>
      </v-card>
    </div>
    <div v-else>
      <v-card>
        <v-card-title>该时间没有任何可用教室</v-card-title>
      </v-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      campus: ['本部', '延长', '嘉定'],
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
    this.$http.get('/api/v1/time/').then(response => {
      this.time.week = response.data.week
      this.time.day = response.data.day
      this.time.course = response.data.course
      this.getEmptyRooms()
    })
  },
  methods: {
    getEmptyRooms(time) {
      this.rooms = {}
      this.$http
        .get('/api/v1/empty-room/', {
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
