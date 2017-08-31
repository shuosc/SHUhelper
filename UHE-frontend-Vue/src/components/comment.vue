<template>
  <v-container fluid class="pa-0 ">
    <div v-if="comments.length" style="padding-bottom:52px;">
      <v-card v-for="comment in comments" :key="comment._id" class="mb-2">
        <v-card-title class="px-3 py-1 teal--text">{{comment.user.name}}:  <br/>
          <span style="font-size:0.8rem;color:grey;">{{$moment(comment.created,'YYYY-MM-DD hh:mm:ss').fromNow()}}</span>
            <v-spacer></v-spacer>
            <v-icon v-show="comment.user.cardID===$store.state.user.cardID" @click="deleteComment(comment.id)">clear</v-icon>
        </v-card-title>
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
          <v-flex xs3 class="mx-1 py-2">
            <v-btn block primary class="white--text ma-0" @click.native="sendComment">评论</v-btn>
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
    deleteComment(id) {
      this.$http.delete(`/api/comments/${id}`).then((response) => {
        this.getComments()
      })
    },
    sendComment () {
      if (this.content === '') return
      this.$http.post('/api/comments/', {
        post: this.post,
        id: this.id,
        content: this.content
      }).then((response) => {
        this.getComments()
      })
    },
    getComments () {
      this.comments = []
      this.$http.get(`/api/comments/?post=${this.post}&id=${this.id}`)
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
