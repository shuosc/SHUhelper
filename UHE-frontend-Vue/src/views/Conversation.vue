<template>
  <div style="padding-bottom:52px;">
    <v-layout row
              class="ma-0">
      <v-flex xs12
              sm6
              offset-sm3>
        <v-card>
          <v-list two-line>
            <div 
                 v-for="message in messages"
                 :key="message">
              <v-list-tile avatar
                           v-bind:key="message.title"
                           href="javascript:;"
                           download
                           target="_blank">
                           <v-list-tile-avatar v-if="message.sender.cardID !== $store.state.user.cardID">
                  <img v-bind:src="`//static.shuhelper.cn/${message.sender.avatar}`">
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-sub-title v-html="message.content"></v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-avatar v-if="message.sender.cardID === $store.state.user.cardID">
                  <img v-bind:src="`//static.shuhelper.cn/${message.sender.avatar}`">
                </v-list-tile-avatar>
              </v-list-tile>
            </div>
          
          </v-list>
        </v-card>
      </v-flex>
    </v-layout>
    <v-card style="position:fixed;bottom:0;width:100%;">
      <v-container class="px-2 py-0">
        <v-layout row
                  justify-center
                  class="ma-0">
          <v-flex xs9
                  class="ma-0 py-2">
            <v-text-field name="input-1"
                          hide-details
                          v-model="content"
                          class="pa-0"></v-text-field>
          </v-flex>
          <v-flex xs3
                  class="px-0 py-2">
            <v-btn block
                   flat
                   class="indigo--text ma-0"
                   @click.native="sendMessage">发送</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </div>
</template>
<script>
// import Addmessage from '@/components/dialog/Addmessage'
export default {
  data () {
    return {
      dialog: false,
      content: '',
      messages: []
    }
  },
  created () {
    // this.getMessages()
    this.getMessagesPoll()
  },
  methods: {
    getMessages () {
      this.$http.get(`/api/conversations/${this.$route.params.id}`)
        .then((response) => {
          this.messages = response.data.messages
        })
    },
    getMessagesPoll () {
      this.$http.get(`/api/conversations/${this.$route.params.id}`)
        .then((response) => {
          this.messages = response.data.messages
          if (this.$route.path === `/conversation/${this.$route.params.id}`) {
            setTimeout(this.getMessagesPoll, 3000)
          }
        })
    },
    sendMessage () {
      if (this.content === '') return
      this.$http.put(`/api/conversations/${this.$route.params.id}`, {
        content: this.content
      })
        .then((response) => {
          this.content = ''
          this.getMessages()
        })
        .catch((error) => {
          this.$store.commit('showSnackbar', { text: '发送失败' + error })
        })
    }
  }
}
</script>
<style lang="stylus">

</style>
