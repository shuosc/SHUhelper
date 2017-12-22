<template lang="pug">
  q-pull-to-refresh(:handler='refresher')
    .flex.column.items-center.no-wrap
      q-card.no-margin(flat='', color='primary', style='text-align:center;height:40vh;width:100vw;')
        q-card-main
          q-item
            q-item-main.flex.justify-center
              q-item-tile(avatar='', style='height:150px;width:150px;', @click='onImgAdd')
                q-spinner(style='color: #e2aa6f', v-if="img.status==='pending'")
                img(v-else='', style='width:100%;height:100%;', :src='`//static.shuhelper.cn/${img.url}`', alt='avatar')
      q-card.bg-white(style='position:relative;top:-10vh;width:80vw;padding:20px;')
        q-card-main
          q-btn.full-width(disable='', flat='')
            | {{user.nickname}}
          // <p class="content-center item-center">
          small.text-center(style='display:block;') {{$route.params.id}}
          // </p>
        q-card-actions
          q-btn.full-width(disable='', color='primary', @click='getConversation') 发消息(维护中 暂不可用)
    form#upload(ref='upload', method='post', enctype='multipart/form-data', style='display:none;')
      input#key(name='key', type='hidden', :value='key')
      input(name='token', type='hidden', :value='token')
      input#userfile(name='file', type='file', accept='image/*', @change='upload')
      input(name='accept', type='hidden')
</template>
<script>
import { Toast } from 'quasar'
import LeftPanel from '@/LayoutLeftPanel'
export default {
  components: {
    LeftPanel
  },
  data() {
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
  created() {
    this.theme = this.$store.state.user.custom.theme
    this.getProfile()
  },
  methods: {
    onImgAdd() {
      if (this.$route.params.id === this.$store.state.user.cardID) {
        this.$refs.upload.userfile.click()
      }
    },
    refresher(done) {
      done()
    },
    getConversation() {
      this.$http
        .post('/api/conversations/', {
          to: this.$route.params.id
        })
        .then(response => {
          this.$router.replace(`/conversation/${response.data.id}`)
        })
    },
    upload(e) {
      // console.log(e.target)
      var userfile = e.target.files[0]
      var selectedFile = userfile.name
      if (selectedFile) {
        var ramdomName =
          Math.random()
            .toString(36)
            .substr(2) + userfile.name.match(/\.?[^./]+$/)
        this.key = 'feed_' + this.$store.state.user.cardID + '_' + ramdomName
        this.img = { name: selectedFile, status: 'pending', url: this.key }
      } else {
        return false
      }
      /* eslint-disable no-new */
      /* eslint-disable new-cap */
      /* eslint-disable no-undef */
      new html5ImgCompress(e.target.files[0], {
        before: function(file) {
          console.log('压缩前...')
          // 这里一般是对file进行filter，例如用file.type.indexOf('image') > -1来检验是否是图片
          // 如果为非图片，则return false放弃压缩（不执行后续done、fail、complete），并相应提示
        },
        done: (file, base64) => {
          console.log('压缩成功...')
          this.$http.get(`/api/upload/token?key=${this.key}`).then(response => {
            this.token = response.data.uptoken
            this.$nextTick(() => {
              var f = new FormData(this.$refs.upload)
              console.log(f)
              let index = base64.indexOf(',') + 1
              this.key = btoa(this.key)
              this.key.replace('+', '-')
              this.key.replace('/', '_')
              this.key.replace('=', '')
              this.$http
                .post(
                  `/upload/putb64/-1/key/${this.key}`,
                  base64.slice(index),
                  {
                    headers: {
                      Authorization: 'UpToken ' + this.token,
                      'Content-Type': 'application/octet-stream'
                    }
                  }
                )
                .then(response => {
                  if (this.img.url === response.data.key) {
                    this.img.status = 'success'
                  }
                  this.$http
                    .get(`/api/users/replace-avatar`, {
                      params: {
                        avatar: this.img.url
                      }
                    })
                    .then(reponse => {
                      Toast.create(`更新头像成功`)
                      this.$store.commit('setAvatar', this.img.url)
                    })
                })
                .catch(error => {
                  console.log(error)
                  if (this.img.url === this.key) {
                    this.img.status = 'failed'
                  }
                })
            })
          })
          // ajax和服务器通信上传base64图片等操作
        },
        fail: function(file) {
          console.log('压缩失败...')
        },
        complete: function(file) {
          console.log('压缩完成...')
        },
        notSupport: function(file) {
          console.log('浏览器不支持！')
          // 不支持操作，例如PC在这里可以采用swfupload上传
        }
      })
    },
    getProfile() {
      this.$http.get(`/api/users/${this.$route.params.id}`).then(response => {
        this.user = response.data
        this.img.url = this.user.avatar
      })
    },
    onThemeChange() {
      this.$http
        .get(`/api/users/set-custom-theme?theme=${this.theme}`)
        .then(response => {
          this.$store.commit('showSnackbar', { text: `更换主题成功` })
          this.themeDialog = false
          this.$store.commit('changeTheme', this.theme)
        })
    }
  }
}
</script>

<style lang="stylus" scoped>
</style>
