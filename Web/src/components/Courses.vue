<template lang="pug">
  div
    q-card
      mt-field(class="pb-0" name="input-1" v-model="quickQuery" single-line placeholder="搜索课程" id="testing")
    div(v-infinite-scroll="searchCourseQuick" :infinite-scroll-disabled="loading||allLoaded" infinite-scroll-distance="40")
      q-card(v-for="(course,index) in courses" :key="course.no+course.teacher"  @click="$router.push(`/courses/${course._id.$oid}`)")
        q-card-title(dense style="white-space:nowrap;")
          | {{course.name}}
          div(slot="subtitle" )
            q-rating(v-model="course.rating" readonly :max="5") 
            small
              | {{course.rating}}({{course.evaluations_count}}人评分)
          div(slot="right" class="row items-center")
            q-item
              <q-icon name="person" /> {{course.teacher_name}}
        q-card-separator
        q-card-main.no-padding
          q-list( inset-separator no-border)
            q-item
              q-item-side
                | 编号
              q-item-main.text-center
                | {{course.no}}
            q-item
              q-item-side
                | 学分
              q-item-main.text-center
                | {{course.credit}}
            //- q-item
              q-item-side
                | 标签
              q-item-main.text-center
                small(v-for="tag in course.tag")
                  | {{tag}}
            q-item
              q-item-side
                | 学院
              q-item-main.text-center
                | {{course.school}}
            q-item
              q-item-side
                | 学期
              q-item-main.text-center
                q-chip(v-for="term in course.terms",:key="term" color="primary" @click.stop="onCourseClick(course,term)")
                  | {{term|term}} 
            q-item
              q-item-side
                | 简介
              q-item-main.text-center
                | {{course.intro}}
        q-card-actions
          .row.flex.justify-end.full-width
            q-btn( :class="{'text-pink':true}" flat)
              q-icon(name="trending_up")
              span(style="color:grey;font-size:1rem;")
                | {{course.heat}}
            q-btn( :class="{'text-pink':course.liked}" flat @click.stop="onLikeClick(course._id.$oid,index)")
              q-icon(name="favorite")
              span(style="color:grey;font-size:1rem;")
                | {{course.like.length}}
            q-btn(flat)
                q-icon(name="comment")
                span(style="color:grey;font-size:1rem;")
                  | {{course.evaluations_count}}
      div(style="text-align:center;height:60px;")
        q-spinner-dots( v-show="loading" indeterminate :size="40")
        <span v-show="allLoaded" class="primary--text">no more data :)</span>
    q-modal(v-model="dialog" minimized  :content-css="{minWidth: '80vw'}")
      course-term-card(v-if="course&&course.course" :course="course.course" :classes="course.classes")
</template>
<script>
import _ from 'lodash'
import { QRating, QChip, QSpinnerDots } from 'quasar'
import { InfiniteScroll } from 'mint-ui'
import CourseTermCard from '@/CourseTermCard'
export default {
  components: {
    QRating,
    QChip,
    CourseTermCard,
    QSpinnerDots
  },
  directives: {
    InfiniteScroll
  },
  data() {
    return {
      query: '',
      quickQuery: '',
      courses: [],
      course: null,
      page: 1,
      dialog: false,
      courseLoading: false,
      loading: false,
      allLoaded: false,
      classTab: ''
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
      this.courses = []
      this.searchCourseQuick(val)
      this.allLoaded = false
      console.log('change', val)
    }
  },
  created() {
    this.searchCourseQuick()
  },
  methods: {
    onCourseClick(course, term) {
      this.courseLoading = true
      this.course = course
      this.dialog = true
      this.$http
        .get(`/api/courses/${course._id.$oid}/${term}`)
        .then(response => {
          this.course = response.data
          this.courseLoading = false
        })
    },
    onLikeClick(id, index) {
      this.$http.get(`/api/courses/${id}/like`).then(response => {
        this.courses.splice(index, 1, response.data)
        this.courses[index].liked = this.courses[index].like.includes(
          this.$store.state.user.cardID
        )
      })
    },
    searchCourseQuick: _.debounce(function() {
      if (this.loading) return
      this.loading = true
      this.$http
        .get('/api/courses/', {
          params: {
            type: 'quick',
            query: this.quickQuery,
            page: this.page
          }
        })
        .then(response => {
          this.page += 1
          response.data.courses.forEach(item => {
            item.liked = item.like.includes(this.$store.state.user.cardID)
          })
          this.courses.push(...response.data.courses)
          this.loading = false
          if (response.data.length === 0) {
            this.allLoaded = true
          }
          // console.log(this.courses)
        })
        .catch(err => {
          console.log(err)
          this.loading = false
          this.allLoaded = true
        })
    }, 500),
    searchCourse: _.debounce(function() {
      this.$http
        .get('/api/courses/', {
          params: {
            type: 'quick',
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
