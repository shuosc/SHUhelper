<template>
  <div>
    <v-card>
      <p class="pt-2 teal--text ma-0" style="text-align:center; font-size:1.1rem;">
        {{course.course.name}}
      </p>
      <h5 style="text-align:center;" class="ma-0">
        <span class="grey--text" style="font-size:0.9rem;">{{course.course.no}} </span>
        <span class="teal--text" style="font-size:0.9rem;">{{course.course.teacher}} 17-18秋</span>
      </h5>
      <v-card-text class="px-0 pt-0">
        <div class="text-xs-center">
          <v-chip small class="primary white--text" v-for="term in terms"
            :key="term" @click="getTermCourse(term)">{{term|term}}</v-chip>
          <v-chip small v-show="terms.indexOf('2017_1')==-1" @click="getTermCourse('2017_1')"
            class="orange white--text">本学期未开</v-chip>
        </div>
        <navbar v-model="active">
          <tab-item v-for="(courseClass,index) in termCourse[term]"
            :id="index" :key="index">{{courseClass.teacher_no}}班</tab-item>
        </navbar>
        <tab-container v-model="active">
          <tab-container-item v-for="(courseClass,index) in termCourse[term]"
            :id="index" :key="index">
            <cell title="学分">
              {{course.course.credit}}</cell>
            <cell title="时间">
              <p class="ma-0" style="font-size:0.8rem;">{{courseClass.time}}</p>
            </cell>
            <cell title="校区">
              {{courseClass.campus}}</cell>
            <cell title="地点">
              {{courseClass.place}}</cell>
            <cell title="答疑时间">
              {{courseClass.q_time}}</cell>
            <cell title="答疑地点">
              {{courseClass.q_place}}</cell>
          </tab-container-item>
        </tab-container>
      </v-card-text>
    </v-card>
     <comment post="course" :id="$route.params.id"></comment>
  </div>
</template>
<script>
// import _ from 'lodash'
import comment from '@/components/comment.vue'
import { Popup, Cell, TabContainer, TabContainerItem, Navbar, TabItem, InfiniteScroll } from 'mint-ui'
export default {
  components: {
    Popup,
    Cell,
    TabContainer,
    TabContainerItem,
    Navbar,
    TabItem,
    InfiniteScroll,
    comment
  },
  filters: {
    term: function (value) {
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
  data () {
    return {
      course: {
        course: {
        }
      },
      terms: {},
      termCourse: {},
      term: '2017_1',
      active: 0
    }
  },
  watch: {
  },
  created () {
    this.getCourse()
  },
  methods: {
    getCourse () {
      this.$http.get(`/api/courses/${this.$route.params.id}`)
        .then((response) => {
          this.course = response.data
          this.terms = response.data.terms
          console.log(this.terms.indexOf('2017_1') !== -1)
          this.getTermCourse(this.term)
          // console.log(this.courses)
        })
    },
    getTermCourse (term) {
      this.$http.get(`/api/courses/${this.$route.params.id}/${term}`)
        .then((response) => {
          this.$set(this.termCourse, this.term, response.data.classes)
          console.log(this.termCourse)
          this.$nextTick(() => {
            this.active = 0
          })
        })
    }
  }
}
</script>
