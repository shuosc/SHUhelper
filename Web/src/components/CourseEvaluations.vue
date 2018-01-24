<template lang="pug">
  div
    q-card(flat)
      q-btn.full-width( @click="$router.push('/course-query')" icon="send") 去评价课程
      //- mt-field(class="pb-0" name="input-1" v-model="quickQuery" single-line placeholder="搜索课程" id="testing")
    div(v-infinite-scroll="searchEvaluationQuick" :infinite-scroll-disabled="loading||allLoaded" infinite-scroll-distance="40")
      q-card(v-for="(evaluation,index) in evaluations" :key="index" style="margin:1rem 0 0 0")
          q-item(dense)
            q-item-main
              q-item-tile(label) 
                | {{evaluation.display_name}} {{[evaluation.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}} 评论了  
              q-item-tile(sublabel)  {{evaluation.course.name}}-{{evaluation.course.teacherName}}
            q-item-side()
              q-item-tile.pull-right
                small.text-faded {{evaluation.term|term}}
              q-item-tile
                q-rating(v-model="evaluation.rating" readonly :max="5") 
          q-card-separator
          q-card-main 
            | {{evaluation.text}}
          q-card-separator
          q-card-actions
            q-btn.full-width(flat @click="$router.push(`/courses/${evaluation.course.id}`)") 前往课程主页
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
export default {
  components: {
    QRating,
    QChip,
    QSpinnerDots
  },
  directives: {
    InfiniteScroll
  },
  data() {
    return {
      query: '',
      quickQuery: '',
      evaluations: [],
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
        this.searchEvaluation(val)
        console.log('change', val)
      },
      deep: true
    }
  },
  created() {
    this.searchEvaluationQuick()
  },
  methods: {
    onEvaluationClick(course, term) {
      this.courseLoading = true
      this.course = course
      this.dialog = true
      this.$http
        .get(`/api/evaluations/${course._id.$oid}/${term}`)
        .then(response => {
          this.course = response.data
          this.courseLoading = false
        })
    },
    onLikeClick(id, index) {
      this.$http.get(`/api/evaluations/${id}/like`).then(response => {
        this.evaluations.splice(index, 1, response.data)
        this.evaluations[index].liked = this.evaluations[index].like.includes(
          this.$store.state.user.cardID
        )
      })
    },
    searchEvaluationQuick: _.debounce(function() {
      if (this.loading) return
      this.loading = true
      this.$http
        .get('/api/evaluations/', {
          params: {
            page: this.page
          }
        })
        .then(response => {
          this.evaluations.push(...response.data)
          this.loading = false
          if (response.data.length === 0) {
            this.allLoaded = true
          }
          this.page += 1
        })
        .catch(err => {
          console.log(err)
          this.loading = false
          this.allLoaded = true
        })
    }, 500)
  }
}
</script>
