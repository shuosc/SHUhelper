<template lang="pug">
  q-card
    q-card-main.text-align
      q-item
        q-item-side.text-align.flex
          q-knob(readonly='', size='2rem', style='font-size: 1rem', color='secondary', track-color='yellow-3', v-model='timeLeft', :min='0', :max='total')
        q-item-main
          q-item-tile(label='')
            | 还有{{timeLeft}}分钟进行第{{parseInt(point)%2===1?(parseInt(point)+1)/2+'节课':parseInt(point)/2+'节课间休息'}}
          q-item-tile(sublabel='') 好好上课不要看手机( •̀ ω •́ )y
    q-card-separator
    q-card-actions
      q-collapsible.full-width(dense='', label='查看你今天的课程安排')
        q-btn.full-width(flat='', @click="$router.push('/schedule')")  查看完整课程表
  //- <q-list separator dense no-border>
  //- <q-item>
  //- <q-item-side>8:00~16:00 </q-item-side>
  //- <q-item-main>
  //- <q-item-tile label>Java程序设计</q-item-tile>
  //- <q-item-tile sublabel>@计408</q-item-tile>
  //- </q-item-main>
  //- </q-item>
  //- <q-item-separator />
  //- <q-item>
  //- <q-item-side>8:00~16:00 </q-item-side>
  //- <q-item-main>
  //- <q-item-tile label>John Doe</q-item-tile>
  //- <q-item-tile sublabel>Administrator</q-item-tile>
  //- </q-item-main>
  //- </q-item>
  //- </q-list>
</template>

<script>
const timeSChedule = [
  800,
  845,
  855,
  940,
  1000,
  1045,
  1055,
  1140,
  1210,
  1255,
  1305,
  1350,
  1410,
  1455,
  1505,
  1550,
  1600,
  1645,
  1655,
  1740,
  1800,
  1845,
  1855,
  1940,
  1950,
  2035
]
export default {
  name: 'courseTime',
  filters: {
    term: function(value) {
      let map = {
        '1': '秋',
        '2': '冬',
        '3': '春',
        '4': '夏'
      }
      let year = parseInt(value.slice(2, 4))
      return `${year}-${year + 1}${map[value[5]]}`
    }
  },
  data() {
    return {
      timerID: 0,
      clock: 0,
      timeLeft: 0,
      point: 0,
      total: 0
    }
  },
  created() {
    this.updateTime()
    this.timerID = setInterval(this.updateTime, 1000)
  },
  beforeDestroy() {
    clearInterval(this.timerID)
  },
  methods: {
    zeroPadding(num, digit) {
      var zero = ''
      for (var i = 0; i < digit; i++) {
        zero += '0'
      }
      return (zero + num).slice(-digit)
    },
    updateTime() {
      var cd = new Date()
      var time = parseInt(
        this.zeroPadding(cd.getHours(), 2) +
          this.zeroPadding(cd.getMinutes(), 2)
      )
      for (let i in timeSChedule) {
        let lastScheduleMinutes =
          timeSChedule[i - 1] % 100 + parseInt(timeSChedule[i - 1] / 100) * 60
        let scheduleMinutes =
          timeSChedule[i] % 100 + parseInt(timeSChedule[i] / 100) * 60
        let timeMinutes = time % 100 + parseInt(time / 100) * 60
        if (scheduleMinutes - timeMinutes > 0) {
          this.timeLeft = scheduleMinutes - timeMinutes
          this.point = parseInt(i) + 1
          this.total = scheduleMinutes - lastScheduleMinutes
          break
        }
      }
      this.clock =
        this.zeroPadding(cd.getHours(), 2) +
        ':' +
        this.zeroPadding(cd.getMinutes(), 2) +
        ':' +
        this.zeroPadding(cd.getSeconds(), 2)
    }
  }
}
</script>

<style>

</style>
