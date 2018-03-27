<template lang="pug">
  div
    div(v-if="course")
      q-card(flat)
        q-card-title(dense )
          | {{course.name}}
          div(slot="subtitle" style="white-space:nowrap;")
            q-rating(v-model="course.rating" readonly :max="5") 
            small
              | {{course.rating.toFixed(2)}}({{course.evaluations_count}}人评分)
          div(slot="right" class="row items-center")
            q-item
              <q-icon name="person" /> {{course.teacher_name}}
        q-card-separator
        q-card-main.no-padding
          .row
            .col-12
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
      //- q-btn.full-width(flat color="black" @click="addEvalation")
            q-icon(name="add") 写点评
      q-list
        q-list-header(v-if="evaluations.length > 0") 共有{{evaluations.length}}条点评
        q-item-separator
        q-card(  v-for="(evaluation,index) in evaluations" @click="$router.push(`/evaluations/${evaluation._id.$oid}`)" :key="index")
          q-card-title.no-padding 
          q-item(dense)
            //- q-item-side
              //- q-item-tile(avatar)
                | {{evaluation.display_name}}
                //- img(:src="`https://static.shuhelper.cn/${evaluation.user.avatar}`")
            q-item-main
              q-item-tile(label) {{evaluation.display_name}} 
                //- q-rating(v-model="evaluation.rating" readonly :max="5") 
                //- small.text-faded {{evaluation.term|term}}
              q-item-tile(sublabel)  {{new Date(evaluation.created.$date - 8*3600*1000)|moment("from")}}
            q-item-side()
              q-item-tile.pull-right
                small.text-faded {{evaluation.term|term}}
              q-item-tile
                q-rating(v-model="evaluation.rating" readonly :max="5") 
          q-card-separator
          q-card-main
            p(v-for="paragraph in evaluation.text.split('\\n')")
              | {{ paragraph }}
          q-card-separator
          q-card-actions.justify-end
            q-btn(small :class="{'text-pink':evaluation.liked}" flat @click.stop="onLikeClick(index)")
              q-icon(name="favorite")
              span(style="color:grey;font-size:1rem;")
                | {{evaluation.like.length}}
            q-btn(flat small)
              q-icon(name="comment")
              span(style="color:grey;font-size:1rem;")
                | {{evaluation.comments.length}}
         
        q-list-header.text-center 没有更多评论
      q-modal(v-model="dialog" minimized  :content-css="{minWidth: '80vw'}")
        course-term-card(v-if="course&&classes" :course="course" :classes="classes")
      q-modal(v-model="evalationModal" minimized  :content-css="{minWidth: '80vw'}")
        q-card.no-margin
          q-card-title
            | 正在评价 {{course.name}}-{{course.teacher_name}}
          q-card-separator
          q-card-main
            q-field(icon="person" label="名字")
              mt-field( v-model="evaluation.name" placeholder="匿名")
            q-field(icon="thumb_up"
              :label="'评分: '+evaluation.rating")
              q-rating(v-model="evaluation.rating" :max="5" size="2rem")  
              //- span(style="font-size:1rem")
                | {{evaluation.rating}}分
            q-field(icon="schedule"
              label="选择上这门课的学期")
              q-select(
                v-model="evaluation.term"
                :options="termOptions")
            q-field(icon="rate_review"
              label="这门课的内容、亮点和你的吐槽")
              mt-field(placeholder="" type="textarea" rows="4" v-model="evaluation.text")
            q-field
              q-btn.full-width(@click="publish") 发布
      q-toolbar(style="position:fixed;bottom:0;" color="white")
        q-toolbar-title
          q-btn.full-width(flat color="primary" @click="addEvalation")
            q-icon(name="add") 写点评
    
</template>
<script>
import { QChip, QRating } from 'quasar'
import CourseTermCard from '@/CourseTermCard'
export default {
  components: {
    QChip,
    CourseTermCard,
    QRating
  },
  data() {
    return {
      course: null,
      evalationModal: false,
      evaluations: [],
      classes: null,
      dialog: false,
      evaluation: {
        rating: 5,
        term: '其他学期',
        name: '匿名',
        text: ''
      }
    }
  },
  created() {
    this.getCourse()
  },
  computed: {
    termOptions: function() {
      let options = []
      options.push({
        label: '其他学期',
        value: '其他学期'
      })
      for (let term of this.course.terms) {
        options.push({
          label: term,
          value: term
        })
      }
      return options
    }
  },
  methods: {
    addEvalation() {
      this.evalationModal = true
    },
    getCourse() {
      this.$http.get(`/api/courses/${this.$route.params.id}`).then(response => {
        this.course = response.data.course
      })
      this.$http
        .get(`/api/evaluations/?course=${this.$route.params.id}`)
        .then(response => {
          this.evaluations = response.data
        })
    },
    onCourseClick(course, term) {
      this.dialog = true
      this.$http
        .get(`/api/courses/${course._id.$oid}/${term}`)
        .then(response => {
          this.classes = response.data.classes
          this.courseLoading = false
        })
    },
    onLikeClick(index) {
      let id
      if (index) {
        id = this.$store.state.courses[index].id
      } else {
        id = this.$route.params.id
      }
      this.$http.get(`/api/courses/${id}/like`)
      this.getCourse()
      if (this.course.liked) {
        this.$store.commit('cancelCourseLike', index)
      } else {
        this.$store.commit('clickCourseLike', index)
      }
    },
    publish() {
      if (this.evaluation.text === '') return
      this.$http
        .post(`/api/evaluations/`, {
          course: this.$route.params.id,
          name: this.evaluation.name,
          text: this.evaluation.text,
          rating: this.evaluation.rating,
          term: this.evaluation.term
        })
        .then(response => {
          this.evaluation = {
            rating: 5,
            text: '',
            term: '其他学期',
            name: '匿名'
          }
          this.getCourse()
          this.evalationModal = false
        })
    }
  }
}
</script>
