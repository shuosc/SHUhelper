<template lang="pug">
      
  div()
    //- q-pull-to-refresh(:handler="refresher", :refresh-icon="false")
    //- pull-to(:top-load-method='refresher' :wrapper-height="'500px'" :is-bottom-bounce="false" :is-top-bounce="false")
    //- div(style="height: calc(100vh - 105px)")
    div.bg-grey-5(v-if="snow" style="position:fixed;top:0;height:100vh;width:100vw;z-index:-1;")
      section(:id="'snow'" )
    div(v-if="refresh" style="z-index:1;" )
      q-card.namecard(flat='')
        q-card-main
          q-icon(name='room')
            | 宝山
      //- <q-gallery-carousel :src="slider"></q-gallery-carousel>
      q-card.namecard
        q-card-main
          q-item
            q-item-side
              q-spinner-hearts(color='red', :size='30')
            q-item-main
              q-item-tile(label='') {{$store.state.user.name}}，{{welcome}} 
            q-item-side
              q-toggle(v-model="snow"  left-label :label="snow?'雪停吧！':'下点大雪吧！'")
      simple-calendar
      q-card()
        q-card-media
          q-parallax(:src="'/statics/course-back.jpg'" :height="150")
          q-card-title(slot="overlay")
            | 评课社区 现已上线
        q-card-actions
          q-btn.full-width(flat @click="$router.push('/course-evaluations')" icon="send" color="primary") 开始评课
      // q-card.no-margin
        q-card-title.text-center.full-width.no-margin(flat style="padding-bottom:0;")
          q-icon(name="card_giftcard")
          | 圣诞快乐&元旦快乐
        index-merry-christmas 
        q-btn.full-width(@click="$router.push('/2018')")
          | 写下你的新年愿望
      course-time(v-if="$store.state.time.day<=5")
      empty-room(v-if="$store.state.time.updated&&$store.state.time.day<=5")
      q-card
        q-card-main.text-center
          q-item
            q-item-side
              q-icon(color='primary', name='fa-book', style='font-size:2rem;')
            q-item-main
              q-item-tile(label='') 课程查询
              q-item-tile(sublabel='') 查询本学期的，其他学期的课程，蹭课必备
        q-card-separator
        q-card-actions
          q-btn.full-width(flat @click="$router.push('/course-query')" icon="send" color="primary") 开始查询
      course-card
      sport-card(v-if="$store.state.user.cardID!==''")
      //- navigator-card
      //- sport-card(v-if="$store.state.user.cardID!=='' && parseInt($store.state.user.cardID)>=16120000")
      school-bus
      map-card
      random-choice
      //- quote-card
      q-card(flat='')
        q-card-main(style='text-align:center;')
          //- img(src="https://forthebadge.com/images/badges/built-with-love.svg")
          //- br
          small(style='color:grey;') 2018 SHU OpenSourceCommnuity

</template>

<script>
import SportCard from '@/IndexSportCard'
import Weather from '@/IndexWeather'
import CourseTime from '@/IndexCourseTime'
import SimpleCalendar from '@/IndexSimpleCalendar'
import QuoteCard from '@/IndexQuote'
import EmptyRoom from '@/IndexEmptyRoom'
import LeftPanel from '@/LayoutLeftPanel'
import IndexMerryChristmas from '@/IndexMerryChristmas'
import SchoolBus from '@/IndexSchoolBus'
import MapCard from '@/IndexMapCard'
import CourseCard from '@/IndexCourseCard'
import RandomChoice from '@/IndexRandomChoice'
import NavigatorCard from '@/IndexNavigator'
import { QSpinnerHearts, QToggle, QCardMedia, QParallax } from 'quasar'
// import PullTo from 'vue-pull-to'
// q-gallery-carousel
export default {
  components: {
    // PullTo,
    Weather,
    CourseTime,
    CourseCard,
    SimpleCalendar,
    QuoteCard,
    EmptyRoom,
    QCardMedia,
    LeftPanel,
    SportCard,
    SchoolBus,
    QParallax,
    RandomChoice,
    IndexMerryChristmas,
    NavigatorCard,
    MapCard,
    QSpinnerHearts,
    QToggle
  },
  data() {
    return {
      refresh: true,
      snow: false
    }
  },
  activated() {
    this.$q.events.$on('app:refresh:index', this.refresher)
  },
  deactivated: function() {
    this.$q.events.$off('app:refresh:index', this.refresher)
  },
  computed: {
    welcome: function() {
      let d = new Date()
      let str = ''
      let hours = d.getHours()
      let day = d.getDay()
      if (hours <= 2) {
        str = '不睡觉在干嘛'
      } else if (hours <= 5) {
        str = '😰你真的不睡觉吗'
      } else if (hours <= 8) {
        str = '早上好，看看今天的课程吧'
      } else if (hours <= 11) {
        str = '上午好~'
      } else if (hours <= 13) {
        str = '中午好，睡午觉吗'
      } else if (hours <= 18) {
        str = '下午好'
      } else if (hours <= 22) {
        str = '晚上好，早点休息'
      } else if (hours <= 24) {
        str = '夜深了，早点睡吧'
      }
      if (day === 0 || day === 6) {
        str = '今天好像放假来着'
      }
      return str
    }
  },
  methods: {
    refresher(done) {
      this.refresh = false
      this.$nextTick(() => {
        this.refresh = true
      })
      done()
    }
  }
}
</script>

<style  scoped>
.namecard {
  transform: translateZ(0);
  opacity: 0.9;
}
.course {
  background: #0cebeb; /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #29ffc6, #20e3b2, #0cebeb); /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #29ffc6, #20e3b2, #0cebeb); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
#snow {
  background: none;
  font-family: Androgyne;
  background-image: url('/statics/s1.png'),
    url('/statics/s2.png'),
    url('/statics/s3.png');
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
  z-index: 1;
  -webkit-animation: snow 12s linear infinite;
  -moz-animation: snow 12s linear infinite;
  -ms-animation: snow 12s linear infinite;
  animation: snow 12s linear infinite;
}
@keyframes snow {
  0% {
    background-position: 0px 0px, 0px 0px, 0px 0px;
  }
  50% {
    background-position: 500px 500px, 100px 200px, -100px 150px;
  }
  100% {
    background-position: 500px 1000px, 200px 400px, -100px 300px;
  }
}
@-moz-keyframes snow {
  0% {
    background-position: 0px 0px, 0px 0px, 0px 0px;
  }
  50% {
    background-position: 500px 500px, 100px 200px, -100px 150px;
  }
  100% {
    background-position: 400px 1000px, 200px 400px, 100px 300px;
  }
}
@-webkit-keyframes snow {
  0% {
    background-position: 0px 0px, 0px 0px, 0px 0px;
  }
  50% {
    background-position: 500px 500px, 100px 200px, -100px 150px;
  }
  100% {
    background-position: 500px 1000px, 200px 400px, -100px 300px;
  }
}
@-ms-keyframes snow {
  0% {
    background-position: 0px 0px, 0px 0px, 0px 0px;
  }
  50% {
    background-position: 500px 500px, 100px 200px, -100px 150px;
  }
  100% {
    background-position: 500px 1000px, 200px 400px, -100px 300px;
  }
}
</style>
