<template>
  <div>
    <v-card class="white lighten-4 elevation-3 mb-2 mt-2">
      <!-- <v-divider></v-divider> -->
      <v-card-text class="pt-0">
        <v-container fluid class="pa-0 ma-0">
          <v-layout row wrap>
            <v-flex xs12>
              <v-text-field class="pb-0" name="input-1" v-model="quickQuery" single-line placeholder="搜索课程" hint="输入课程号／课程名／教师名" id="testing"></v-text-field>
            </v-flex>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
    </v-card>
    <v-card>
      <v-card-text class="px-1">
        <v-layout row>
          <v-flex xs2>课程号</v-flex>
          <v-flex xs5>课程名</v-flex>
          <v-flex xs2>教师名</v-flex>
          <v-flex xs2>备注</v-flex>
        </v-layout>
      </v-card-text>
      <v-divider></v-divider>

    </v-card>
    <div v-infinite-scroll="searchCourseQuick" :infinite-scroll-disabled="loading||allLoaded" infinite-scroll-distance="40">
      <v-card flat v-for="course in courses" :key="course.no" @click.native.stop="onCourseClick(course)">
        <v-card-text class="px-1">
          <v-layout row>
            <v-flex xs2>
              <span class="teal--text" style="font-size:0.8rem;">{{course.no}}
              </span>
            </v-flex>
            <v-flex xs5>{{course.name}}</v-flex>
            <v-flex xs2> {{course.teacher}}
            </v-flex>
            <v-flex xs3>
              <span v-if="!course.this_term">本学期未开</span>
            </v-flex>
          </v-layout>
        </v-card-text>
        <v-divider></v-divider>
      </v-card>
      <div style="text-align:center;height:60px;">
        <v-progress-circular v-show="loading" indeterminate class="primary--text"></v-progress-circular>
        <span v-show="allLoaded" class="primary--text">no more data :)</span>
      </div>
    </div>
    <popup v-model="dialog" popup-transition="popup-fade">
      <v-layout row justify-center style="position: relative;">
        <v-card style="width:300px;" v-show="courseLoading">
          <div>
            <v-progress-circular indeterminate class="primary--text"></v-progress-circular>
          </div>
        </v-card>
        <v-card style="width:300px;" v-show="!courseLoading">
          <p class="pt-2 teal--text ma-0" style="text-align:center; font-size:1.1rem;">
            {{course.course.name}}
          </p>
          <h5 style="text-align:center;" class="ma-0">
            <span class="grey--text" style="font-size:0.9rem;">{{course.course.no}} </span>
            <span class="teal--text" style="font-size:0.9rem;">{{course.course.teacher}} 17-18秋</span>
          </h5>
          <v-card-text class="px-0 pt-0">
            <div class="text-xs-center" v-show="!course.classes.length">
              <v-chip small class="orange   white--text">本学期未开</v-chip>
            </div>
            <navbar v-model="active">
              <tab-item v-for="(courseClass,index) in course.classes" :id="index" :key="index">{{courseClass.teacher_no}}班</tab-item>
            </navbar>
            <tab-container v-model="active">
              <tab-container-item v-for="(courseClass,index) in course.classes" :id="index" :key="index">
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
          <v-card-actions>
            <v-btn class="green--text darken-1" flat="flat" block @click.native="$router.push(`/courses/${course.course._id.$oid}`)">前往该课程主页</v-btn>
          </v-card-actions>
        </v-card>
      </v-layout>
    </popup>
  </div>
</template>
<script>
import _ from 'lodash'
import {
  Popup,
  Cell,
  TabContainer,
  TabContainerItem,
  Navbar,
  TabItem,
  InfiniteScroll
} from 'mint-ui'
export default {
  components: {
    Popup,
    Cell,
    TabContainer,
    TabContainerItem,
    Navbar,
    TabItem,
    InfiniteScroll
  },
  data() {
    return {
      query: '',
      quickQuery: '',
      courses: [],
      page: 1,
      dialog: false,
      course: {
        course: {},
        classes: []
      },
      active: 0,
      courseLoading: false,
      loading: false,
      allLoaded: false
    }
  },
  watch: {
    active: function(val) {
      console.log(val)
    },
    query: {
      handler: function(val) {
        this.page = 1
        this.searchCourse(val)
        console.log('change', val)
      },
      deep: true
    },
    quickQuery: function(val) {
      this.page = 1
      this.courses = null
      this.courses = []
      this.searchCourseQuick(val)
      this.allLoaded = false
      console.log('change', val)
    }
  },
  created() {
    // this.searchCourseQuick()
  },
  methods: {
    onCourseClick(course) {
      this.courseLoading = true
      this.course = course
      this.dialog = true
      this.$http
        .get(`/api/v1/courses/${course._id.$oid}/2017_1`)
        .then(response => {
          this.course = response.data
          this.courseLoading = false
          this.$nextTick(() => {
            this.active = 0
          })
          // console.log(this.courses)
        })
    },
    searchCourseQuick: _.debounce(function() {
      if (this.loading) return
      this.loading = true
      this.$http
        .get('/api/v1/courses/', {
          params: {
            quick: true,
            query: this.quickQuery,
            page: this.page
          }
        })
        .then(response => {
          this.page += 1
          this.courses.push(...response.data)
          this.loading = false
          if (response.data.length === 0) {
            this.allLoaded = true
          }
          console.log(this.courses)
        })
        .catch(err => {
          console.log(err)
          this.loading = false
          this.allLoaded = true
        })
    }, 500),
    searchCourse: _.debounce(function() {
      this.$http
        .get('/api/v1/courses/', {
          params: {
            quick: true,
            query: this.query,
            page: this.query.page
          }
        })
        .then(response => {
          this.courses = response.data
          console.log(this.courses)
        })
    }, 500)
  }
}
</script>
