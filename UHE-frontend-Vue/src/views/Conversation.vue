<template>
  <div style="height:100%;padding-bottom:52px;overflow-y:scroll;" ref="content" @scroll="handleScroll">
    <infinite-loading direction="top" :on-infinite="getMessagesBefore" ref="infiniteLoading" style="height:50px;"></infinite-loading>
    <v-layout row class="ma-0">
      <v-flex xs12 sm6 offset-sm3>
        <v-card class="mb-0" flat v-for="(message,index) in messages" :key="index">
          <v-container fluid grid-list-lg class="py-0">
            <v-layout row>
              <v-flex xs2 style="text-align:center;" v-show="!message.me" @click="$router.push(`/profile/${message.sender}`)">
                <v-avatar size="3rem">
                  <img :src="`//static.shuhelper.cn/${user[message.sender].avatar}`" alt="avatar">
                </v-avatar>
              </v-flex>
              <v-flex xs10>
                <div :style="{fontSize:'1.1rem',textAlign:message.me?'right':'left'}" class="teal--text">
                  <span style="font-size:0.8rem;" class="grey--text" v-show="message.me">
                    {{ [ message.created.slice(0,19), "YYYY-MM-DD HH:mm:ss"] | moment("MM-DD HH:mm:ss") }}
                  </span>{{user[message.sender].nickname}}
                  <span style="font-size:0.8rem;" class="grey--text" v-show="!message.me">
                    {{ [ message.created.slice(0,19), "YYYY-MM-DD HH:mm:ss"] | moment("MM-DD HH:mm:ss") }}
                  </span>
                </div>
                <v-container class="pb-2 pt-2 px-0">
                  <v-layout row>
                    <v-flex xs12 :style="{fontSize:'1.1rem',color:'grey',textAlign:message.me?'right':'left'}">
                      {{message.content}}</v-flex>
                  </v-layout>
                </v-container>
              </v-flex>
              <v-flex xs2 style="text-align:center;" v-show="message.me" @click="$router.push(`/profile/${message.sender}`)">
                <v-avatar size="3rem">
                  <img :src="`//static.shuhelper.cn/${user[message.sender].avatar}`" alt="avatar">
                </v-avatar>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
    <v-card style="position:fixed;bottom:0;width:100%;">
      <v-container class="px-2 py-0">
        <v-layout row justify-center class="ma-0">
          <v-flex xs9 class="ma-0 py-2">
            <v-text-field name="input-1" hide-details v-model="content" class="pa-0"></v-text-field>
          </v-flex>
          <v-flex xs3 class="px-0 py-2">
            <v-btn block flat :loading="sendLoading" class="indigo--text ma-0" @click.native="sendMessage()">发送</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </div>
</template>
<script>
// import InfiniteLoading from 'vue-infinite-loading'
// import Addmessage from '@/components/dialog/Addmessage'
import InfiniteLoading from '@/vue-infinite-loading/src/components/InfiniteLoading.vue'
export default {
  components: {
    InfiniteLoading
  },
  data () {
    return {
      dialog: false,
      content: '',
      messages: [],
      loading: false,
      scrollByHand: false,
      isPolling: false,
      newest: null,
      count: 0,
      start: 0,
      user: {},
      oldHeight: 0,
      oldTop: 0,
      conversationReady: false,
      sendLoading: false,
      nIntervId: null
    }
  },
  created () {
    this.getConversation()
  },
  beforeDestroy () {
    clearInterval(this.nIntervId)
  },
  methods: {
    handleScroll () {
      let content = this.$refs.content
      if (content.scrollTop !== content.scrollHeight - content.clientHeight) {
        this.scrollByHand = true
      } else {
        this.scrollByHand = false
      }
    },
    getMessagesBefore () {
      if (!this.conversationReady) return
      if (this.start <= 0) {
        this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
        return
      }
      this.$http.get(`/api/v1/conversations/${this.$route.params.id}/before/${this.start}`)
        .then((response) => {
          let messages = response.data.messages.map(this.myMessage)
          this.messages.unshift(...messages)
          let content = this.$refs.content
          this.oldHeight = content.scrollHeight
          this.oldTop = content.scrollTop
          let flag = this.start === this.count
          this.$nextTick(() => {
            if (flag) {
              content.scrollTop = content.scrollHeight
            } else {
              content.scrollTop = content.scrollHeight - this.oldHeight + this.oldTop
            }
            this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
            this.start -= response.data.messages.length
          })
        })
        .catch((err) => {
          console.log(err)
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
        })
    },
    getConversation () {
      this.$http.get(`/api/v1/conversations/${this.$route.params.id}`)
        .then((response) => {
          this.user[response.data.fromUser.cardID] = response.data.fromUser
          this.user[response.data.toUser.cardID] = response.data.toUser
          this.count = response.data.count
          this.start = this.count
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
          this.conversationReady = true
          this.nIntervId = setInterval(this.getMessages, 1000)
        })
    },
    myMessage (message) {
      message.me = message.sender === this.$store.state.user.cardID
      return message
    },
    getMessages () {
      let id = this.$route.params.id
      if (this.$route.path !== `/conversation/${id}`) return
      this.$http.get(`/api/v1/conversations/${id}/after/${this.count}`)
        .then((response) => {
          let messages = response.data.messages.map(this.myMessage)
          this.messages.push(...messages)
          this.count += messages.length
          if (!this.scrollByHand) {
            this.$nextTick(() => {
              var content = this.$refs.content
              content.scrollTop = content.scrollHeight - content.clientHeight
            })
          }
        })
        .catch((err) => {
          console.log(err)
        })
    },
    sendMessage () {
      if (this.content === '') return
      this.sendLoading = true
      this.$http.put(`/api/v1/conversations/${this.$route.params.id}`, {
        content: this.content
      })
        .then((response) => {
          this.content = ''
          this.sendLoading = false
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
