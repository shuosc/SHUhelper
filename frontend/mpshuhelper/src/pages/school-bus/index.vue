<template lang="pug">
div.bus
  div.row.center.card
    div.col-12
      picker(mode="multiSelector",:range="choice", @change="bindMultiPickerChange", :value="placeIndex")
        view.picker.row
          div.col-6 起点站
          div.col-6 终点站
          div.col-6 {{choice[0][placeIndex[0]]}}
          div.col-6 {{choice[1][placeIndex[1]]}}
    div.col-4
      div 上一趟
      div(v-if="last!==null") {{last}}
    div.col-4 
      div 当前时间
      div {{time}}
    div.col-4
      div 下一趟
      div(v-if="next!==null") {{next}}
    div.col-12(v-if="wait!==null") 还需要等待 {{wait}} 分钟
  div.row.center.card(v-if="placeIndex[0]!==placeIndex[1]")
    div.col-12 所有时刻表
    div.col-12(v-for="item in result",:key="item") {{item}}
</template>

<script>
  import BusSchedule from '../../../static/bus.json'
  export default {
    data() {
      return {
        last: null,
        next: null,
        wait: null,
        choice: [
          ['宝山校区', '延长校区北门', '嘉定校区南门'],
          ['宝山校区', '延长校区北门', '嘉定校区南门']
        ],
        placeIndex: [0, 0],
        result: []
      }
    },
    methods: {
      getSchedule() {
        const from = this.choice[0][this.placeIndex[0]]
        const to = this.choice[1][this.placeIndex[1]]
        console.log('From', from)
        console.log('To', to)
        if (from === to) {
          this.result = []
        } else {
          const timeTable = BusSchedule[from][to]
          this.result = timeTable
        }
      },
      nearestDepartures() {
        let minutes = this.time.slice(3, 5)
        let hours = this.time.slice(0, 2)
        for (let i = 0; i < this.result.length; i++) {
          let departure = this.result[i]
          let dHours = parseInt(departure.slice(0, 2))
          let dMinutes = parseInt(departure.slice(3, 5))
          console.log('hours:', hours)
          console.log('minutes:', minutes)
          if (hours < dHours || (dHours === hours && minutes < dMinutes)) {
            return {
              last: i > 0 ? this.result[i - 1] : null,
              next: this.result[i],
              wait: dHours * 60 + dMinutes - hours * 60 - minutes
            }
          }
        }
        return {
          last: null,
          next: null,
          wait: null
        }
      },
      bindMultiPickerChange(e) {
        this.placeIndex = e.mp.detail.value
        this.getSchedule()
        const nearestDepartures = this.nearestDepartures()
        console.log(nearestDepartures)
        this.last = nearestDepartures.last
        this.next = nearestDepartures.next
        this.wait = nearestDepartures.wait
      }
    },
    computed: {
      time() {
        const date = new Date()
        let hour = date.getHours()
        if (hour < 10) {
          hour = '0' + hour
        }
        let minute = date.getMinutes()
        if (minute < 10) {
          minute = '0' + minute
        }
        return `${hour}:${minute}`
      }
    }
  }
</script>

<style scoped>
  .card {
    background-color: #ffffff;
    padding: 11px 16px 11px 16px;
    box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
    border-radius: 8px;
    margin: 0 0 10px 0;
  }
  .center {
    text-align: center
  }
  .bus {
    background-color: #dedede;
    height: calc(100vh - 20px);
    padding: 10px;
  }
</style>
