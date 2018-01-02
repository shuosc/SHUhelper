<template lang="pug">
  div
    q-card.namecard
      q-card-main
        q-item
          q-item-side
            q-icon(color='primary', name='fa-bus', style='font-size:2rem;')
          q-item-main
            q-item-tile(label='') 校车时刻表
            q-item-tile(sublabel='') 周一到周五
        div.flex.row
          q-select.col-6(
            v-model="station.from"
            float-label="起点站"
            radio
            :options="stations")
          q-select.col-6(
            v-model="station.to"
            float-label="终点站"
            radio
            :options="stations")
      q-item(v-if="nearestDepartures.last||nearestDepartures.next")
        q-item-side(v-if="nearestDepartures.last")
          q-item-tile.text-center
            | 上一趟 
          q-item-tile.text-center
            | {{nearestDepartures.last}}
        q-item-main(v-if="nearestDepartures.next")
          q-item-tile.text-center
            | 离下一趟还有 
          q-item-tile.text-center
            | {{nearestDepartures.wait}}分钟
        q-item-side(v-if="nearestDepartures.next")
          q-item-tile.text-center
            | 下一趟
          q-item-tile.text-center
            | {{nearestDepartures.next}}
      q-card-separator
      q-card-actions
        q-collapsible.full-width(dense='', label='查看完整时刻表')
          q-list(no-border dense)
            q-item(v-for="(departure,index) in departures" :key="departure")
              q-item-side
                | {{index+1}}
              q-item-main
                | {{departure}}
        
</template>
<script>
function listToSelect(l) {
  return l.map(x => {
    return { label: x, value: x }
  })
}
const BusSchedule = {
  嘉定校区南门: {
    校本部: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '17:00', '21:00'],
    延长校区北门: ['18:00', '21:00', '途径校本部']
  },
  校本部: {
    延长校区北门: ['09:30', '10:30', '11:30', '12:30', '13:30', '14:30', '15:30', '18:00', '21:40'],
    嘉定校区南门: ['08:00', '09:30', '10:30', '11:30', '12:30', '13:30', '14:30', '15:30', '18:00', '21:00']
  },
  延长校区北门: {
    校本部: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
    嘉定校区南门: ['21:00']
  }
}
export default {
  name: 'SchoolBus',
  data() {
    return {
      busSchedule: BusSchedule,
      station: {
        from: '嘉定校区南门',
        to: '校本部'
      },
      stations: listToSelect(['校本部', '延长校区北门', '嘉定校区南门']),
      timerID: ''
    }
  },
  created() {
    this.nearestDepartures()
    this.timerID = setInterval(this.nearestDepartures, 30000)
  },
  watch: {
    station: {
      handler: function(val, oldval) {
        this.nearestDepartures()
      },
      deep: true
    }
  },
  beforeDestroy() {
    clearInterval(this.timerID)
  },
  computed: {
    departures: function() {
      return this.busSchedule[this.station.from][this.station.to]
    },
    nearestDepartures: function() {
      let minutes
      let hours
      if (DEV) {
        minutes = 40
        hours = 14
      } else {
        let time = new Date()
        minutes = time.getMinutes()
        hours = time.getHours()
      }
      for (let i = 0; i < this.departures.length; i++) {
        let departure = this.departures[i]
        let dHours = parseInt(departure.slice(0, 2))
        let dMinutes = parseInt(departure.slice(3, 5))
        if (hours < dHours || (dHours === hours && minutes < dMinutes)) {
          return {
            last: i > 0 ? this.departures[i - 1] : null,
            next: this.departures[i],
            wait: dHours * 60 + dMinutes - hours * 60 - minutes
          }
        }
      }
      return {
        last: null,
        next: null
      }
    }
  }
}
</script>
<style scoped>

</style>

