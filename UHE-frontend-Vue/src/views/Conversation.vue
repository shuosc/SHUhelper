<template>
  <div style="height:100%;padding-bottom:52px;overflow-y:scroll;" ref="content" @scroll="handleScroll">
    <infinite-loading direction="top" :on-infinite="getMessagesBefore" ref="infiniteLoading" style="height:50px;"></infinite-loading>
    <v-layout row class="ma-0">
      <v-flex xs12 sm6 offset-sm3>
        <v-card class="mb-0" flat v-for="(message,index) in messages" :key="index">
          <v-container fluid grid-list-lg class="py-0">
            <v-layout row>
              <v-flex xs2 v-show="!message.me">
                <v-card-media :src="`//static.shuhelper.cn/${user[message.sender].avatar}`" height="100%" contain></v-card-media>
              </v-flex>
              <v-flex xs10>
                <div :style="{fontSize:'1.1rem',textAlign:message.me?'right':'left'}" class="teal--text">
                  <span style="font-size:0.8rem;" class="grey--text" v-show="message.me">
                    {{ [ message.created.slice(0,19), "YYYY-MM-DD HH:mm:ss"] | moment("MM-DD HH:mm:ss") }}
                  </span>{{user[message.sender].name}}
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
              <v-flex xs2 v-show="message.me">
                <v-card-media :src="`//static.shuhelper.cn/${user[message.sender].avatar}`" height="100%" contain></v-card-media>
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
            <v-btn block flat class="indigo--text ma-0" @click.native="sendMessage">发送</v-btn>
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
      conversationReady: false
    }
  },
  created () {
    this.getMessages()
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
      this.$http.get(`/api/conversations/${this.$route.params.id}/before/${this.start}`)
        .then((response) => {
          this.messages.unshift(...response.data.messages)
          let content = this.$refs.content
          this.oldHeight = content.scrollHeight
          this.oldTop = content.scrollTop
          console.log(this.start, this.count)
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
          // setTimeout(() => { this.getMessagesPoll(id) }, 1000)
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
        })
    },
    getMessages () {
      this.$http.get(`/api/conversations/${this.$route.params.id}`)
        .then((response) => {
          this.user[response.data.fromUser.cardID] = response.data.fromUser
          this.user[response.data.toUser.cardID] = response.data.toUser
          this.count = response.data.count
          this.start = this.count
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
          this.conversationReady = true
          this.getMessagesPoll(this.$route.params.id)
        })
    },
    getMessagesPoll (id) {
      if (this.isPolling) return
      if (this.$route.path !== `/conversation/${id}`) return
      this.isPolling = true
      this.$http.get(`/api/conversations/${id}/after/${this.count}`)
        .then((response) => {
          this.messages.push(...response.data.messages)
          this.count += response.data.messages.length
          this.isPolling = false
          if (!this.scrollByHand) {
            this.$nextTick(() => {
              var content = this.$refs.content
              content.scrollTop = content.scrollHeight - content.clientHeight
              // console.log(content.scrollTop, content.scrollHeight - content.clientHeight)
            })
          }
          setTimeout(() => { this.getMessagesPoll(id) }, 1000)
        })
        .catch((err) => {
          console.log(err)
          setTimeout(() => { this.getMessagesPoll(id) }, 1000)
        })
    },
    sendMessage () {
      if (this.content === '') return
      this.$http.put(`/api/conversations/${this.$route.params.id}`, {
        content: this.content
      })
        .then((response) => {
          this.content = ''
          // this.getMessages()
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
