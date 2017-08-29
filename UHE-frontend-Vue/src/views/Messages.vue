<template>
  <v-container style="height:100%;">
    <v-layout row class="ma-0" style="height:100%;">
      <v-flex xs12 sm6 offset-sm3 class="pa-0">
        <v-list two-line style="height:100%;">
          <div v-for="(conversation,index) in conversations" :key="conversation.conversation" @click.native="$router.push(`/conversation/${conversation.id}`)">
            <v-list-tile avatar :to="`/conversation/${conversation.conversation}`" v-bind:key="conversation.title">
              <v-list-tile-avatar>
                <img v-bind:src="`//static.shuhelper.cn/${conversation.toUser.avatar}`">
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title >{{conversation.toUser.name}} <span v-if="conversation.lastMessage" style="color:grey;font-size:0.8rem;">{{conversation.lastMessage.created.slice(5,19)}}</span></v-list-tile-title> 
                <v-list-tile-sub-title v-html="conversation.lastMessage?conversation.lastMessage.content:''"></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-divider v-bind:inset="true"></v-divider>
          </div>
        </v-list>
        <v-container v-if="loading">
          <v-layout align-center>
            <v-flex xs12 style="text-align:center;">
              <v-progress-circular indeterminate class="primary--text"></v-progress-circular>
            </v-flex>
          </v-layout>
        </v-container>
      </v-flex>
      <v-btn dark fixed fab bottom right class="pink" style="bottom:60px;" @click="dialog=true">
        <v-icon>add</v-icon>
      </v-btn>
      <add-conversation :dialog="dialog" @closeDialog="dialog=false" @sendMessageSucceed="getConversations"></add-conversation>
    </v-layout>  
  </v-container>
</template>
<script>
import AddConversation from '@/components/dialog/AddConversation'
export default {
  components: {
    AddConversation
  },
  data () {
    return {
      dialog: false,
      conversations: [],
      loading: true
    }
  },
  created () {
    this.loading = true
    this.getConversations()
  },
  methods: {
    getConversations () {
      this.$http.get('/api/conversations/')
        .then((response) => {
          this.conversations = response.data
          this.loading = false
          if (this.$route.path === '/messages') {
            setTimeout(this.getConversations, 5000)
          }
        })
    }
  }
}
</script>
<style lang="stylus">

</style>
