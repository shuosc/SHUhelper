<template>
  <div>
    <v-card class="grey lighten-4 elevation-3 mb-2">
      <!-- <v-divider></v-divider> -->
      <v-card-text class="pt-0">
        <v-container fluid class="pa-0 ma-0">
          <v-layout row wrap>
            <v-flex xs12>
              <v-text-field class="pb-0" name="input-1" v-model="quickQuery"
                single-line placeholder="搜索课程" hint="输入课程号／课程名／教师名"
                id="testing"></v-text-field>
            </v-flex>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
    </v-card>
    <v-card flat v-for="course in courses" :key="course.no"
      @click="$router.push(`/courses/${course.no}`)">
      {{course.name}}{{course.no}}{{course.teacher}}
    </v-card>
  </div>
</template>
<script>
import _ from 'lodash'
export default {
  data () {
    return {
      query: '',
      quickQuery: '',
      courses: [],
      page: 1
    }
  },
  watch: {
    query: {
      handler: function (val) {
        this.page = 1
        this.searchCourse(val)
        console.log('change', val)
      },
      deep: true
    },
    quickQuery: function (val) {
      this.page = 1
      this.searchCourseQuick(val)
      console.log('change', val)
    }
  },
  created () {
    this.searchCourseQuick()
  },
  methods: {
    onCourseClick: function (event) {
      console.log(event)
    },
    searchCourseQuick: _.debounce(
      function () {
        this.$http.get('/api/courses/', {
          params: {
            quick: true,
            query: this.quickQuery,
            page: this.page
          }
        })
          .then((response) => {
            this.courses = response.data
            console.log(this.courses)
          })
      }, 500
    ),
    searchCourse: _.debounce(
      function () {
        this.$http.get('/api/courses/', {
          params: {
            quick: true,
            query: this.query,
            page: this.query.page
          }
        })
          .then((response) => {
            this.courses = response.data
            console.log(this.courses)
          })
      }, 500
    )
  }
}
</script>
