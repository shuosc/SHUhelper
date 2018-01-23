<template lang="pug">
  div
    q-modal-layout(v-if="course")
      q-card
        q-card-title(dense style="white-space:nowrap;")
          | {{course.name}}
          div(slot="subtitle" )
            q-rating(v-model="course.rating" readonly :max="5") 
            small
              | {{course.rating}}({{course.evaluations.length}}人评分)
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
      q-list
        q-list-header(v-if="course.evaluations.length > 0") 共有{{course.evaluations.length}}条点评
        q-item-separator
        q-card(flat v-for="(evaluation,index) in course.evaluations" :key="index" style="margin:1rem 0 0 0")
          q-card-title.no-padding 
          q-item(dense @click.stop="$router.push(`/profile/${evaluation.user.cardID}`) || $refs.courseModal.close()")
            q-item-side
              q-item-tile(avatar)
                img(:src="`https://static.shuhelper.cn/${evaluation.user.avatar}`")
            q-item-main
              q-item-tile(label) {{evaluation.user.name}} 
                q-rating(v-model="evaluation.rating" readonly :max="5") 
                small.text-faded {{evaluation.term|term}}
              q-item-tile(sublabel)  {{new Date(evaluation.created.$date - 8*3600*1000)|moment("from")}}
            q-item-side(:stamp="`\#${index+1}`")
          q-card-separator
          q-card-main 
            p
            | {{evaluation.text}}
        q-list-header 没有更多评论
      q-modal(v-model="dialog" minimized  :content-css="{minWidth: '80vw'}")
        course-term-card(v-if="course&&classes" :course="course" :classes="classes")
      q-modal(v-model="evalationModal" minimized  :content-css="{minWidth: '80vw'}")
        q-card.no-margin
          q-card-title
            | 正在评价 {{course.name}}-{{course.teacher_name}}
          q-card-separator
          q-card-main
            .row
              .col-12
                span.text-faded 评分: {{evaluation.rating}}
                br
                q-rating(v-model="evaluation.rating" :max="5" size="2rem")   
                //- span(style="font-size:1rem")
                  | {{evaluation.rating}}分
              .col-12
                q-select(
                  v-model="evaluation.term"
                  float-label="选择上这门课的学期"
                  radio
                  :options="termOptions")
              .col-12
                mt-field(placeholder="这门课的内容、亮点和你的吐槽" type="textarea" rows="4" v-model="evaluation.text")
              .col-12
                q-btn.full-width(@click="publish") 发布
      q-toolbar(slot="footer" color="white")
        q-toolbar-title
          q-btn(flat color="black" @click="addEvalation")
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
      classes: null,
      dialog: false,
      evaluation: {
        rating: 5,
        term: ''
      }
    }
  },
  created() {
    this.getCourse()
  },
  computed: {
    termOptions: function() {
      let options = []
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
        .put(`/api/courses/${this.$route.params.id}`, {
          text: this.evaluation.text,
          rating: this.evaluation.rating,
          term: this.evaluation.term
        })
        .then(response => {
          this.evaluation = {}
          this.getCourse()
          this.evalationModal = false
        })
    }
  }
}
</script>
