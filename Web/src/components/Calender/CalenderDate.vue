<template>
  <span class="calender-date" :class="can_rest?'can-rest':''">
    <span class="holiday-name" v-if="holiday_name">
      {{ holiday_name }}
    </span>
    <span class="select-course" v-if="select_course">
      选课
    </span>
    <span class="calender-date-day">
      <slot></slot>
    </span>
  </span>
</template>

<script>
  export default {
    props: ['holiday_name', 'select_course', 'can_rest'],
    name: 'calender-date'
  }
</script>

<style scoped lang='stylus'>
  .calender-date {
    &.can-rest {
      background #CC0033
      color white
    }
    position relative
    display inline-flex
    flex-direction row
    align-items center
    justify-content center
    min-width 60px
    min-height 75px
    width 100%
    text-align center
    .calender-date-day {
      font-size 20pt
      font-family Serif
    }

    .holiday-name, .select-course {
      font-size 10pt
      position absolute
      top 0
      background rgba(100, 100, 100, 0.5)
      color white
      padding-bottom 2px
      padding-top 2px
    }

    .holiday-name {
      right 0
      border-bottom-left-radius 2px
    }

    .select-course {
      left 0
      border-bottom-right-radius 2px
    }
  }
</style>
