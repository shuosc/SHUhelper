<template>
  <table class="calender-month q-table cell-separator">
    <thead>
    <tr>
      <th class="text-center">一</th>
      <th class="text-center">二</th>
      <th class="text-center">三</th>
      <th class="text-center">四</th>
      <th class="text-center">五</th>
      <th class="text-center">六</th>
      <th class="text-center">日</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="row in calender_data">
      <td v-for="data in row">
        <calender-date v-if="data"
                       :holiday_name="data.holiday_name"
                       :select_course="data.select_course"
                       :can_rest="data.can_rest"
                       :class="((new Date(data.date)).toDateString() === (new Date()).toDateString()) ? 'today' : ''">
          {{ (new Date(data.date)).getDate() }}
        </calender-date>
        <calender-date v-else>{{ null }}</calender-date>
      </td>
    </tr>
    </tbody>
  </table>
</template>

<script>
  import CalenderDate from './CalenderDate'

  export default {
    components: {CalenderDate},
    props: ['calender_data'],
    name: 'calender-month'
  }
</script>

<style scoped lang='stylus'>
  table.q-table.bordered, table.q-table.cell-separator:not(.responsive):not(.flipped) {
    border none
    border-top 1px solid rgba(0,0,0,0.12)
  }
  table.q-table td,
  table.q-table th {
    padding 0
  }

  .calender-date.today {
    outline: 5px solid #7ed522;
    outline-offset -5px
  }
</style>
