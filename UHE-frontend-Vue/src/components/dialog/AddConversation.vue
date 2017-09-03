<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" persistent fullscreen transition="dialog-bottom-transition" :overlay="false">
        <v-card>
          <v-toolbar dark class="primary">
            <v-btn icon @click.native="onDialogClose()" dark>
              <v-icon>iconfont-close</v-icon>
            </v-btn>
            <v-toolbar-title>搜索</v-toolbar-title>

          </v-toolbar>
          <v-container fluid class="pa-1">
            <v-text-field label="通过学号或姓名搜索你想联系的人..." v-model="search"></v-text-field>

          </v-container>
          <v-container fluid class="pa-0">
            <v-card v-for="user in users" @click="getConversation(user._id)" :key="user._id">
              <v-card-text>{{ user.name }} ({{ user._id }})</v-card-text>
            </v-card>
          </v-container>
        </v-card>
      </v-dialog>
    </v-layout>
  </div>
</template>
<script>
export default {
  props: {
    dialog: {
      type: Boolean,
      default () {
        return false
      }
    }
  },
  data () {
    return {
      search: '',
      publishLoading: false,
      users: []
    }
  },
  watch: {
    search () {
      this.searchUser()
    }
  },
  methods: {
    searchUser () {
      this.$http.get(`/api/users/search/${this.search}`)
        .then((response) => {
          if (response.data.length === 0) {
            if (this.search.length === 8) {
              this.users = [{ _id: this.search, name: '匿名用户' }]
            }
          } else {
            this.users = response.data
          }
        })
    },
    onDialogClose: function () {
      this.$emit('closeDialog')
    },
    getConversation (cardID) {
      this.$http.post('/api/conversations/', {
        to: cardID
      })
        .then((response) => {
          this.$router.push(`/conversation/${response.data.id}`)
        })
    },
    sendMessage () {
      var _this = this
      this.publishLoading = true
      this.$http.post('/api/conversations/', {
        to: this.sendTo,
        message: this.message
      })
        .then((response) => {
          _this.$store.commit('showSnackbar', { text: '发表成功' + response.data.id })
          _this.sendTo = ''
          this.publishLoading = false
          this.$emit('closeDialog')
          this.$emit('sendMessageSucceed')
        })
        .catch((error) => {
          _this.$store.commit('showSnackbar', { text: '发表失败' + error })
        })
    }
  }
}
</script>
