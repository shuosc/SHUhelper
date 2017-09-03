<template>
  <v-container fluid class="pa-0 ">
    <div v-if="comments.length" style="padding-bottom:52px;">
      <v-card v-for="comment in comments" :key="comment._id" class="mb-2">
        <v-container fluid  class="py-1 px-1">
          <v-layout row @click.stop="$router.push(`/profile/${comment.user.cardID}`)">
            <v-flex xs2 style="text-align:center;vertical-align:middle;">
              <v-avatar size="2rem">
                <img :src="`//static.shuhelper.cn/${comment.user.avatar}`" alt="avatar">
              </v-avatar>
              <!-- <v-card-media :src="`//static.shuhelper.cn/${feed.user.avatar}`" height="2.5rem" contain></v-card-media> -->
            </v-flex>
            <v-flex xs4>
              <div style="display:block;">
                <div style="font-size:1rem;" class="">{{comment.user.name}}</div>
                <div style="font-size:0.5rem;" class="secondary-text">
                  {{[comment.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
                </div>
              </div>
            </v-flex>
            <v-flex xs6 @click.stop>
              <v-icon style="display:inline-block;float:right;" v-show="comment.user.cardID===$store.state.user.cardID" @click="deleteComment(comment.id)">clear</v-icon>
            </v-flex>
          </v-layout>
        </v-container>
        <!-- <v-card-title class="px-3 py-1 teal--text">
          <v-avatar size="3rem">
            <img :src="`//static.shuhelper.cn/${comment.user.avatar}`" alt="avatar">
          </v-avatar>{{comment.user.name}}: <br/>
          <span style="font-size:0.8rem;color:grey;">{{$moment(comment.created,'YYYY-MM-DD hh:mm:ss').fromNow()}}</span>
          
          <v-icon v-show="comment.user.cardID===$store.state.user.cardID" @click="deleteComment(comment.id)">clear</v-icon>
        </v-card-title> -->
        <v-divider></v-divider>
        <v-card-text>{{comment.content}}</v-card-text>
      </v-card>
    </div>
    <v-card v-else>
      <v-card-title>无评论</v-card-title>
    </v-card>
    <v-card style="position:fixed;bottom:0;width:100%;">
      <v-container class="px-0 py-0">
        <v-layout row justify-center class="mx-1">
          <v-flex xs9 class="ma-0 py-2">
            <v-text-field name="input-1" hide-details v-model="content" class="pa-0"></v-text-field>
          </v-flex>
          <v-flex xs3 class="mx-0 py-2">
            <v-btn block flat class="blue--text ma-0" @click.native="sendComment">
              <v-icon>send</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
export default {
  props: {
    post: {
      type: String
    },
    id: {
      type: String
    }
  },
  data () {
    return {
      comments: [],
      content: ''
    }
  },
  created () {
    this.getComments()
  },
  methods: {
    deleteComment (id) {
      this.$http.delete(`/api/v1/comments/${id}`).then((response) => {
        this.getComments()
      })
    },
    sendComment () {
      if (this.content === '') return
      this.$http.post('/api/v1/comments/', {
        post: this.post,
        id: this.id,
        content: this.content
      }).then((response) => {
        this.content = ''
        this.getComments()
      })
    },
    getComments () {
      this.comments = []
      this.$http.get(`/api/v1/comments/?post=${this.post}&id=${this.id}`)
        .then((response) => {
          this.comments = response.data
          // this.comments = this.comments.length
        })
    }
  }
}
</script>

<style>

</style>
