<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" persistent fullscreen transition="dialog-bottom-transition" :overlay="false" >
        <v-card >
          <v-toolbar dark fixed class="primary">
            <v-btn icon @click.native="$router.go(-1)" dark>
              <v-icon>close</v-icon>
            </v-btn>
            <v-toolbar-title>查看动态</v-toolbar-title>
          </v-toolbar>
          <v-container fluid class="pa-0 mb-2" style="height:100%;overflow:scroll;margin-top:64px;">
            <feed :index="index" :feed="feed" class="mt-3" @onLikeClick="onLikeClick"></feed>
          </v-container>
          <v-container fluid class="pa-0 ">
            <div v-if="comments.length" style="padding-bottom:52px;">
              <v-card v-for="comment in comments" :key="comment._id" class="mb-2">
                <v-card-title class="pa-1 teal--text">{{comment.user.name}}:
                  <v-spacer></v-spacer>{{$moment(comment.created,'YYYY-MM-DD hh:mm:ss').fromNow()}}</v-card-title>
                <v-divider></v-divider>
                <v-card-text>{{comment.content}}</v-card-text>
              </v-card>
            </div>
            <v-card v-else>
              <v-card-title>无评论</v-card-title>
            </v-card>
            <v-card style="position:fixed;bottom:0;width:100%;">
              <v-container class="px-0 py-0">
                <v-layout row justify-center class="ma-0">
                  <v-flex xs9 class="ma-0 py-2">
                    <v-text-field name="input-1" hide-details v-model="content" class="pa-0"></v-text-field>
                  </v-flex>
                  <v-flex xs3 class="px-0 py-2">
                    <v-btn block flat class="indigo--text ma-0" @click.native="sendComment">评论</v-btn>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card>
          </v-container>
        </v-card>
      </v-dialog>
    </v-layout>

  </div>
</template>
<script>
import feed from '@/components/feed'
export default {
  components: {
    feed
  },
  props: {
    index: {
      type: Number
    }
  },
  mounted () {
    this.dialog = true
  },
  beforeDestroy () {
    this.dialog = false
  },
  data () {
    return {
      dialog: false,
      feed: {},
      content: '',
      text: '',
      publishLoading: false,
      toggle_text: [
        { text: 'Left', value: 1 },
        { text: 'Center', value: 2 },
        { text: 'Right', value: 3 },
        { text: 'Justify', value: 4 }
      ],
      uploadImgs: [],
      key: '',
      token: '',
      link: {
        URL: '',
        img: '',
        title: '',
        saved: false
      },
      comments: []
    }
  },
  // watch: {
  //   dialog: function (val) {
  //     if (val) {
  //       this.getFeed()
  //       this.getComments()
  //     }
  //   }
  // },
  created () {
    this.getFeed()
    this.getComments()
  },
  methods: {
    sendComment () {
      this.$http.post('/api/comments/', {
        post: 'feed',
        id: this.feed.id,
        content: this.content
      }).then((response) => {
        this.getComments()
      })
    },
    getComments () {
      this.comments = []
      this.$http.get(`/api/comments/?post=feed&id=${this.$route.params.id}`)
        .then((response) => {
          this.comments = response.data
          this.feed.comments = this.comments.length
        })
    },
    onDialogClose: function () {
      this.$emit('closeDialog')
    },
    onLikeClick () {
      this.$http.get(`/api/feeds/${this.$route.params.id}/like`)
      this.getFeed()
    },
    getFeed () {
      this.$http.get(`/api/feeds/${this.$route.params.id}`)
        .then((response) => {
          this.feed = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style>
#testform {
  display: none;
}
</style>
