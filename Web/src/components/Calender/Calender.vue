<template>
  <div>
    <div class="calender-header">
      <q-btn @click="setToLastMonth" color="primary">&lt;</q-btn>
      <span> {{ currentYear }} 年 {{ currentMonth }} 月 </span>
      <q-btn @click="setToNextMonth" color="primary">&gt;</q-btn>
    </div>
    <!--the month we are displaying-->
    <calender-month :calender_data="the_month">
    </calender-month>
  </div>
</template>

<script>
  import CalenderMonth from './CalenderMonth'
  import calenderData from './CalenderData'
  import {QBtn} from 'quasar-framework'
  import _ from 'lodash'

  export default {
    components: {CalenderMonth, QBtn},
    data: function() {
      return {
        the_month: [],
        currentMonthRange: null,
        currentYear: '',
        currentMonth: ''
      }
    },
    name: 'calender',
    methods: {
      setMonthDisplaying: function(firstDayOfTheMonthIndex, lastDayOfTheMonthIndex) {
        let data = calenderData.calenderData
        let dateObject = new Date(data[firstDayOfTheMonthIndex].date)
        this.currentYear = dateObject.getFullYear()
        this.currentMonth = dateObject.getMonth() + 1
        this.the_month = []
        let currentWeek = []
        // eslint-disable-next-line no-unused-vars
        for (let __ in _.range(data[firstDayOfTheMonthIndex].weekday)) {
          currentWeek.push(null)
        }
        _.range(firstDayOfTheMonthIndex, lastDayOfTheMonthIndex + 1).forEach((index) => {
          currentWeek.push(data[index])
          if (data[index].weekday === 6) {
            this.the_month.push(currentWeek)
            currentWeek = []
          }
        })
        if (currentWeek) {
          this.the_month.push(currentWeek)
        }
      },
      indexRangeOfTheMonth: function(theDateToFind) {
        let data = calenderData.calenderData
        let firstDayOfTheMonthIndex = _.findIndex(data, (dateObject) => {
          let theDate = new Date(dateObject.date)
          return theDateToFind.getFullYear() === theDate.getFullYear() && theDateToFind.getMonth() === theDate.getMonth()
        })
        let lastDayOfTheMonthIndex = _.findLastIndex(data, (dateObject) => {
          let theDate = new Date(dateObject.date)
          return theDateToFind.getFullYear() === theDate.getFullYear() && theDateToFind.getMonth() === theDate.getMonth()
        })
        return {firstDayOfTheMonthIndex: firstDayOfTheMonthIndex, lastDayOfTheMonthIndex: lastDayOfTheMonthIndex}
      },
      setToLastMonth: function() {
        let lastDayOfLastMonthIndex = this.currentMonthRange.firstDayOfTheMonthIndex - 1
        let theDate = new Date(calenderData.calenderData[lastDayOfLastMonthIndex].date)
        this.currentMonthRange = this.indexRangeOfTheMonth(theDate)
        this.setMonthDisplaying(this.currentMonthRange.firstDayOfTheMonthIndex, this.currentMonthRange.lastDayOfTheMonthIndex)
      },
      setToNextMonth: function() {
        let firstDayOfNextMonthIndex = this.currentMonthRange.lastDayOfTheMonthIndex + 1
        let theDate = new Date(calenderData.calenderData[firstDayOfNextMonthIndex].date)
        this.currentMonthRange = this.indexRangeOfTheMonth(theDate)
        this.setMonthDisplaying(this.currentMonthRange.firstDayOfTheMonthIndex, this.currentMonthRange.lastDayOfTheMonthIndex)
      }
    },
    mounted: function() {
      this.currentMonthRange = this.indexRangeOfTheMonth(new Date())
      this.setMonthDisplaying(this.currentMonthRange.firstDayOfTheMonthIndex, this.currentMonthRange.lastDayOfTheMonthIndex)
    }
  }
</script>

<style scoped lang='stylus'>
  .calender-header {
    width 100%
    display flex
    justify-content space-between
    margin-top 30px
  }

  .calender-month {
    width 100%
  }
</style>
