<template lang="pug">
  div
    q-modal-layout()
      evaluation-card(:evaluation="evaluation" :comments="false" flat @like="onLikeClick()" @delete="$router.go(-1)")
      q-list
        q-list-header(v-if="evaluation.comments.length > 0") 共有{{evaluation.comments.length}}条评论
        q-item-separator
        q-card(flat v-for="(comment,index) in evaluation.comments" :key="index" style="margin:1rem 0 0 0")
          q-card-title.no-padding 
          q-item(dense)
            //- q-item-side
              q-item-tile(avatar)
                img(:src="`https://static.shuhelper.cn/${comment.user.avatar}`")
            q-item-main
              q-item-tile(label) {{comment.display_name}}
              q-item-tile(sublabel)  {{[comment.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
            q-item-side(:stamp="`\#${index+1}`")
          q-card-separator
          q-card-main 
            | {{comment.text}}
        q-list-header 没有更多评论
      q-toolbar(slot="footer" color="white")
        q-toolbar-title
          mt-field(placeholder="请输入评论" v-model="comment")
        q-btn(flat color="primary" @click="publishComment(evaluation.id)")
          q-icon(name="send")
</template>
<script>
import { QInnerLoading, QSpinnerGears } from 'quasar'
import EvaluationCard from '@/CourseEvaluationCard'
export default {
  components: {
    QSpinnerGears,
    QInnerLoading,
    EvaluationCard
    // PullTo
  },
  data() {
    return {
      evaluation: {
        img: [],
        text: '',
        user: {
          avatar: 'avatar_default.jpg',
          name: ''
        },
        comments: [],
        like: [],
        created: '2018-01-07 12:58:59.359000',
        index: 0
      },
      img: '',
      imgLoading: false,
      comment: ''
    }
  },
  created() {
    this.getEvaluation()
  },
  methods: {
    getEvaluation() {
      this.$http.get(`/api/evaluations/${this.$route.params.id}`).then(response => {
        this.evaluation = response.data
      })
    },
    showImg(img) {
      if (this.img !== img) {
        this.imgLoading = true
      }
      this.img = img
      this.$refs.imgModal.open()
    },
    onLikeClick() {
      this.$http.get(`/api/evaluations/${this.evaluation.id}/like`).then(response => {
        this.evaluation = response.data
      })
    },
    imgLoad() {
      this.imgLoading = false
    },
    publishComment(evaluationID) {
      if (this.comment === '') return
      this.$http
        .post(`/api/evaluations/${this.$route.params.id}/comments`, {
          name: '匿名',
          content: this.comment
        })
        .then(response => {
          this.comment = ''
          this.evaluation = response.data
        })
    }
  }
}
</script>
