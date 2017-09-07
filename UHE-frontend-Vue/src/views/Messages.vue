<template>
  <div>
    <v-container class="pa-0">
      <v-layout row class="ma-0">
        <v-flex xs12 sm6 offset-sm3 class="pa-0">
          <v-list two-line style="height:100%;">
            <div v-for="(conversation,index) in conversations" :key="conversation.id">
              <v-list-tile avatar :to="`/conversation/${conversation.id}`" v-bind:key="conversation.title">
                <v-list-tile-avatar>
                  <img v-bind:src="`//static.shuhelper.cn/${conversation.toUser.avatar}`">
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{conversation.toUser.nickname}}
                    <span v-if="conversation.lastMessage" class="secondary-text" style="font-size:0.8rem;">{{conversation.lastMessage.created.slice(5,19)}}</span>
                  </v-list-tile-title>
                  <v-list-tile-sub-title class="secondary-text">{{conversation.lastMessage?conversation.lastMessage.content:''}}</v-list-tile-sub-title>

                </v-list-tile-content>
                <v-list-tile-action @click.prevent="alert('ss')">
                  <v-menu bottom right>
                    <v-btn icon slot="activator" light>
                      <v-icon>more_vert</v-icon>
                    </v-btn>
                    <v-list>
                      <v-list-tile @click="idToDel=conversation.id,delDialog=true">
                        <v-list-tile-title>删除</v-list-tile-title>
                      </v-list-tile>
                    </v-list>
                  </v-menu>
                </v-list-tile-action>
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
      </v-layout>
    </v-container>
    <v-btn fixed fab right bottom class="dark-primary" style="bottom:60px;" @click="dialog=true">
      <v-icon>add</v-icon>
    </v-btn>
    <add-conversation :dialog="dialog" @closeDialog="dialog=false" @sendMessageSucceed="getConversations"></add-conversation>
    <v-dialog v-model="delDialog" lazy absolute style="z-index:10 !important;">
      <v-card>
        <v-card-title>
          <div class="headline">确认删除吗？</div>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="green--text darken-1" flat="flat" @click.native="delDialog = false">返回</v-btn>
          <v-btn class="green--text darken-1" flat="flat" @click.native="delConversation(idToDel)">确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
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
      loading: true,
      delDialog: false,
      idToDel: ''
    }
  },
  created () {
    this.loading = true
    this.getConversations()
  },
  methods: {
    delConversation (id) {
      this.$http.delete(`/api/v1/conversations/${id}`)
      .then((response) => {
        this.delDialog = false
        this.flushConversations()
      })
    },
    flushConversations () {
      this.$http.get('/api/v1/conversations/')
        .then((response) => {
          this.conversations = response.data
          this.loading = false
        })
    },
    getConversations () {
      this.$http.get('/api/v1/conversations/')
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
