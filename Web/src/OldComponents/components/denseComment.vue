<template>
  <v-container fluid class="pa-0 ">
    <div v-if="comments.length" >
      <v-card v-for="comment in comments" :key="comment._id" class="mb-0" flat>
        <v-container fluid  class="py-1 px-3">
          <v-layout row @click.stop="$router.push(`/profile/${comment.user.cardID}`)">
            <v-flex xs11>
              <div style="display:block;">
                <div style="font-size:1rem;" class=""><span class="blue--text">{{comment.user.name}}</span>: {{comment.content}}</div>
              </div>
            </v-flex>
            <v-flex xs1 @click.stop>
              <v-icon style="display:inline-block;float:right;" v-show="comment.user.cardID===$store.state.user.cardID" @click="deleteComment(comment.id)">clear</v-icon>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </div>
    <v-card v-else flat>
      <v-card-title>无评论</v-card-title>
    </v-card>
    <v-card style="width:100%;" flat>
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
