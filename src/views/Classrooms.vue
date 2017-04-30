<template>
  <scroller lock-x
            scrollbar-y
            height="-96"
            ref="scroller">
    <div>
      <group gutter="0">
        <selector title="周数"
                  :options="[1,2,3,4,5,6,7,8,9,10]"
                  v-model="week"></selector>
        <selector title="天数"
                  :options="[1,2,3,4,5]"
                  v-model="day"></selector>
        <selector title="节数"
                  :options="[1,2,3,4,5,6,7,8,9,10,11,12,13]"
                  v-model="time"></selector>
        <x-button type="primary"
                  @click.native="getEmptyRooms()">查询</x-button>
      </group>
      <divider>查询结果</divider>
      <div id="info">
        目前参数是 第{{ week }}周 周{{ day }} 第{{ time }}节
      </div>
      <div id="rooms"><span v-if="!rooms.length">所在时段没有任何空教室呢</span><span v-for="room in rooms">{{ room + ' '}}</span></div>
    </div>
  </scroller>
</template>

<script>
import { Group, Divider, XButton, Scroller, Selector } from 'vux'

export default {
  components: {
    Group,
    Divider,
    XButton,
    Selector,
    Scroller
  },
  data() {
    return {
      week: null,
      day: null,
      time: null,
      rooms: []
    }
  },
  computed: {
  },
  created: function () {
    this.getEmptyRooms()
  },
  methods: {
    resetScroller() {
      this.$nextTick(() => {
        this.$refs.scroller.reset()
      })
    },
    getEmptyRooms() {
      this.$http.get('/api/classrooms/empty', {
        params: {
          week: this.week,
          day: this.day,
          time: this.time
        }
      }).then((response) => {
        this.week = response.data.week
        this.day = response.data.day
        this.time = response.data.time
        this.rooms = response.data.rooms
        this.$vux.toast.show({
          position: 'bottom',
          type: 'text',
          text: '查询成功'
        })
        this.resetScroller()
      })
    }
  }
}
</script>

<style>
#info {
  color: #fff;
  border-radius: 15px;
  margin: 10px;
  padding: 5px;
  font-size: 1rem;
  background-color: rgba(83, 134, 139, 0.90);
  text-shadow: 0px 0px 0px #000;
  text-align: center;
}

#rooms {
  color: #fff;
  border-radius: 15px;
  margin: 10px;
  padding: 5px;
  font-size: 0.8rem;
  background-color: rgba(100, 109, 237, 0.70);
  text-shadow: 0px 0px 0px #000;
  text-align: center;
}
</style>
