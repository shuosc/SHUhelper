<template lang="pug">
  div
    q-modal-layout()
      feed-card(:feed="feed" :comments="false" flat @like="onLikeClick()" @delete="$router.push('/square')")
      q-list
        q-list-header(v-if="feed.comments.length > 0") 共有{{feed.comments.length}}条评论
        q-item-separator
        q-card(flat v-for="(comment,index) in feed.comments" :key="index" style="margin:1rem 0 0 0")
          q-card-title.no-padding 
          q-item(dense @click.stop="$router.push(`/profile/${comment.user.cardID}`) || $refs.feedModal.close()")
            q-item-side
              q-item-tile(avatar)
                img(:src="`https://static.shuhelper.cn/${comment.user.avatar}`")
            q-item-main
              q-item-tile(label) {{comment.user.name}}
              q-item-tile(sublabel)  {{[comment.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
            q-item-side(:stamp="`\#${index+1}`")
          q-card-separator
          q-card-main 
            | {{comment.text}}
        q-list-header 没有更多评论
      q-toolbar(slot="footer" color="white")
        q-toolbar-title
          mt-field(placeholder="请输入评论" v-model="comment")
        q-btn(flat color="primary" @click="publishComment(feed.id)")
          q-icon(name="send")
</template>
<script>
import { QInnerLoading, QSpinnerGears } from 'quasar'
import FeedCard from '@/SquareFeedCard'
export default {
  components: {
    QSpinnerGears,
    QInnerLoading,
    FeedCard
    // PullTo
  },
  data() {
    return {
      feed: {
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
    this.getFeed()
  },
  methods: {
    getFeed() {
      this.$http.get(`/api/feeds/${this.$route.params.id}`).then(response => {
        this.feed = response.data
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
      this.$http.get(`/api/feeds/${this.feed.id}/like`).then(response => {
        this.feed = response.data
      })
    },
    imgLoad() {
      this.imgLoading = false
    },
    publishComment(feedID) {
      if (this.comment === '') return
      this.$http
        .put(`/api/feeds/${this.$route.params.id}`, {
          text: this.comment
        })
        .then(response => {
          this.comment = ''
          this.feed = response.data
        })
    }
  }
}
</script>
