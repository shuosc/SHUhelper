<template lang="pug">
  div
    q-modal-layout()
      q-toolbar(slot="header" color="primary")
        q-btn(slot="left" flat round small color="white" v-back="")
            q-icon( name="keyboard_backspace")
        q-toolbar-title
            | 详情
      q-card(flat style="margin:1rem 0 0 0")
        q-card-title.no-padding 
        q-item(dense)
          q-item-side
            q-item-tile(avatar)
              img(:src="`https://static.shuhelper.cn/${feed.user.avatar}`")
          q-item-main
            q-item-tile(label) {{feed.user.name}}
            q-item-tile(sublabel)  {{[feed.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
        q-card-separator
        q-card-main 
          p(v-for="paragraph in feed.text.split('\\n')")
            | {{ paragraph }}
        div.row.flex.xs-gutter(v-if="feed.img.length !== 0" style="padding:0.5rem;")
          div.col-4(v-for="(img,index) in feed.img" :key="index" @click.stop="")
            img(:src="`https://static.shuhelper.cn/${img}-slim75`" @click="showImg(img)"
            style="object-fit: cover;width:100%;height:100%;" 
            alt="lorem")
        q-card-separator
        q-card-actions
          div.full-width
            q-btn.pull-right(flat)
              q-icon(name="comment")
              span(style="color:grey;font-size:1rem;")
                | {{feed.comments.length}}
            q-btn.pull-right( :class="{'text-pink':feed.liked}" flat @click.stop="onLikeClick($route.query.index)")
              q-icon(name="favorite")
              span(style="color:grey;font-size:1rem;")
                | {{feed.likecount}}
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
export default {
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
    onLikeClick(index) {
      let id
      if (index) {
        id = this.$store.state.feeds[index].id
      } else {
        id = this.$route.params.id
      }
      this.$http.get(`/api/feeds/${id}/like`)
      this.getFeed()
      if (this.feed.liked) {
        this.$store.commit('cancelFeedLike', index)
      } else {
        this.$store.commit('clickFeedLike', index)
      }
    },
    publishComment(feedID) {
      if (this.comment === '') return
      this.$http
        .put(`/api/feeds/${this.$route.params.id}`, {
          text: this.comment
        })
        .then(response => {
          this.comment = ''
          this.getFeed(feedID)
        })
    }
  }
}
</script>
