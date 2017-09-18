<template>
  <div>
    <v-card style="text-align:center;">
      <v-card-title>
        <v-container>
          <v-layout row wrap>
            <v-flex xs12>
              <v-avatar size="100px" @click="onImgAdd">
                <v-progress-circular v-if="img.status==='pending'" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
                <img v-else :src="`//static.shuhelper.cn/${img.url}`" alt="avatar">
              </v-avatar>
            </v-flex>
            <!-- <v-flex v-if="$route.params.id===$store.state.user.cardID" xs12>
                      <v-btn flat @click="onImgAdd">更换头像</v-btn>
                    </v-flex> -->
            <v-flex v-if="$route.params.id===$store.state.user.cardID" xs12>
              <v-btn flat @click.stop="themeDialog=true">更换主题</v-btn>
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
    <v-dialog v-model="themeDialog" lazy absolute>
      <v-card>
        <v-card-title>
          <div class="headline">更换皮肤主题(实验性)</div>
        </v-card-title>
        <v-card-text>
          <v-radio-group v-model="theme" column>
            <v-radio label="经典白" color="white" value="whitetheme"></v-radio>
            <v-radio label="经典蓝" color="blue" value="bluetheme"></v-radio>
          </v-radio-group>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="green--text darken-1" flat="flat" @click.native="themeDialog = false">取消</v-btn>
          <v-btn class="green--text darken-1" flat="flat" @click.native="onThemeChange">提交</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
      token: '',
      themeDialog: false,
      theme: ''
    }
  },
  created () {
    this.theme = this.$store.state.user.custom.theme
    this.getProfile()
  },
  methods: {
    onImgAdd () {
      if (this.$route.params.id === this.$store.state.user.cardID) {
        this.$refs.testform.userfile.click()
      }
    },
    getConversation () {
      this.$http.post('/api/v1/conversations/', {
        to: this.$route.params.id
      })
        .then((response) => {
          this.$router.replace(`/conversation/${response.data.id}`)
        })
    },
    upload (e) {
      // console.log(e.target)
      var userfile = e.target.files[0]
      var selectedFile = userfile.name
      if (selectedFile) {
        var ramdomName = Math.random().toString(36).substr(2) + userfile.name.match(/\.?[^./]+$/)
        this.key = 'feed_' + this.$store.state.user.cardID + '_' + ramdomName
        this.img = { name: selectedFile, status: 'pending', url: this.key }
      } else {
        return false
      }
      /* eslint-disable no-new */
      /* eslint-disable new-cap */
      /* eslint-disable no-undef */
      new html5ImgCompress(e.target.files[0], {
        before: function (file) {
          console.log('压缩前...')
          // 这里一般是对file进行filter，例如用file.type.indexOf('image') > -1来检验是否是图片
          // 如果为非图片，则return false放弃压缩（不执行后续done、fail、complete），并相应提示
        },
        done: (file, base64) => {
          console.log('压缩成功...')
          this.$http.get(`/api/v1/upload/token?key=${this.key}`)
            .then((response) => {
              this.token = response.data.uptoken
              this.$nextTick(
                () => {
                  var f = new FormData(this.$refs.testform)
                  f
                  let index = base64.indexOf(',') + 1
                  this.key = btoa(this.key)
                  this.key.replace('+', '-')
                  this.key.replace('/', '_')
                  this.key.replace('=', '')
                  this.$http.post(`/upload/putb64/-1/key/${this.key}`, base64.slice(index), {
                    headers: {
                      'Authorization': 'UpToken ' + this.token,
                      'Content-Type': 'application/octet-stream'
                    }
                  })
                    .then((response) => {
                      if (this.img.url === response.data.key) {
                        this.img.status = 'success'
                      }
                      this.$http.get(`/api/v1/users/replace-avatar`, {
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
          // ajax和服务器通信上传base64图片等操作
        },
        fail: function (file) {
          console.log('压缩失败...')
        },
        complete: function (file) {
          console.log('压缩完成...')
        },
        notSupport: function (file) {
          console.log('浏览器不支持！')
          // 不支持操作，例如PC在这里可以采用swfupload上传
        }
      })
    },
    getProfile () {
      this.$http.get(`/api/v1/users/${this.$route.params.id}`)
        .then((response) => {
          this.user = response.data
          this.img.url = this.user.avatar
        })
    },
    onThemeChange () {
      this.$http.get(`/api/v1/users/set-custom-theme?theme=${this.theme}`)
        .then((response) => {
          this.$store.commit('showSnackbar', { text: `更换主题成功` })
          this.themeDialog = false
          this.$store.commit('changeTheme', this.theme)
        })
    }
  }
}

</script>
