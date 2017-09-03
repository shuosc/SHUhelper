<template>
  <div>
    <v-card style="text-align:center;">
      <v-card-title>
        <v-container>
          <v-layout row wrap>
            <v-flex xs12>
              <v-avatar size="100px">
                <v-progress-circular v-if="img.status==='pending'" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
                <img v-else :src="`//static.shuhelper.cn/${img.url}`" alt="avatar">
              </v-avatar>
            </v-flex>
            <v-flex v-if="$route.params.id===$store.state.user.cardID" xs12>
              <v-btn flat @click="onImgAdd">更换头像</v-btn>
            </v-flex>
            <v-flex xs12>
              <h4>{{user.nickname}}</h4>
            </v-flex>
            <v-flex xs12>{{$route.params.id}}</v-flex>
          </v-layout>
        </v-container>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-layout row wrap>
        </v-layout>
      </v-card-text>
      <v-card-actions>
        <v-btn primary block @click.native="getConversation">发消息</v-btn>
      </v-card-actions>
    </v-card>
    <form id="testform" ref="testform" method="post" enctype="multipart/form-data" style="display:none;">
      <input name="key" id="key" type="hidden" :value="key">
      <input name="token" type="hidden" :value="token">
      <input id="userfile" name="file" type="file" accept="image/*" @change="upload" />
      <input name="accept" type="hidden" />
    </form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      user: {},
      img: {
        name: '',
        url: '',
        status: ''
      },
      key: '',
      token: ''
    }
  },
  created () {
    this.getProfile()
  },
  methods: {
    onImgAdd () {
      this.$refs.testform.userfile.click()
    },
    getConversation () {
      this.$http.post('/api/conversations/', {
        to: this.$route.params.id
      })
        .then((response) => {
          this.$router.replace(`/conversation/${response.data.id}`)
        })
    },
    upload (e) {
      console.log(e.target)
      var userfile = e.target.files[0]
      var selectedFile = userfile.name
      if (selectedFile) {
        var ramdomName = Math.random().toString(36).substr(2) + userfile.name.match(/\.?[^./]+$/)
        this.key = 'feed_' + this.$store.state.user.cardID + '_' + ramdomName
        this.img = { name: selectedFile, status: 'pending', url: this.key }
      } else {
        return false
      }
      this.$http.get(`/api/upload/token?key=${this.key}`)
        .then((response) => {
          this.token = response.data.uptoken
          this.$nextTick(
            () => {
              var f = new FormData(this.$refs.testform)
              this.$http.post('/upload', f)
                .then((response) => {
                  if (this.img.url === response.data.key) {
                    this.img.status = 'success'
                  }
                  this.$http.get(`/api/users/replace-avatar`, {
                    params: {
                      avatar: this.img.url
                    }
                  }).then((reponse) => {
                    this.$store.commit('showSnackbar', { text: `更新头像成功` })
                  })
                })
                .catch((error) => {
                  console.log(error)
                  if (this.img.url === this.key) {
                    this.img.status = 'failed'
                  }
                })
            }
          )
        })
    },
    getProfile () {
      this.$http.get(`/api/users/${this.$route.params.id}`)
        .then((response) => {
          this.user = response.data
          this.img.url = this.user.avatar
        })
    }
  }
}

</script>
