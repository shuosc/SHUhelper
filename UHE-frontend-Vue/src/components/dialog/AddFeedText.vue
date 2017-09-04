<template>
  <v-dialog v-model="dialog" persistent fullscreen :overlay="false">
    <v-card>
      <v-toolbar dark class="dark-primary">
        <v-btn icon @click.native="$router.go(-1)" dark>
          <v-icon>iconfont-close</v-icon>
        </v-btn>
        <v-toolbar-title>发布动态</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click.native="publish()" dark>
          <v-progress-circular v-show="publishLoading" :indeterminate="publishLoading" class="red--text"></v-progress-circular>发 布
        </v-btn>
      </v-toolbar>
      <v-container fluid class="pa-1 ">
        <v-text-field name="input-1"  autofocus full-width v-model="text" label="说点什么.." multi-line></v-text-field>
      </v-container>
      <v-container fluid grid-list-sm>
        <v-layout row wrap>
          <v-flex xs3 v-for="(img,key) in uploadImgs" :key="key">
            <img :src="`//static.shuhelper.cn/${img.url}-slim75`" style="object-fit: cover;" v-if="img.status==='success'" alt="lorem" width="100%" height="100%" />
            <v-progress-circular v-else-if="img.status==='pending'" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
            <v-btn block v-else fab large>
              X</v-btn>
          </v-flex>
          <v-flex xs3>
            <v-btn block fab large @click="onImgAdd">
              添加图片</v-btn>
          </v-flex>

        </v-layout>
      </v-container>
      <form id="testform" ref="testform" method="post" enctype="multipart/form-data">
        <input name="key" id="key" type="hidden" :value="key">
        <input name="token" type="hidden" :value="token">
        <input id="userfile" name="file" type="file" accept="image/*" @change="upload" />
        <!-- take photo with phone -->
        <!-- <input id="userfile" name="file" accept="image/*" type="file" /> -->
        <!-- take video with phone -->
        <!-- <input id="userfile" name="file" type="file" accept="video/*"/> -->
        <input name="accept" type="hidden" />
      </form>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  mounted () {
    this.dialog = true
  },
  beforeDestroy () {
    this.dialog = false
  },
  data () {
    return {
      dialog: true,
      text: '',
      publishLoading: false,
      toggle_text: [
        { text: 'Left', value: 1 },
        { text: 'Center', value: 2 },
        { text: 'Right', value: 3 },
        { text: 'Justify', value: 4 }
      ],
      uploadImgs: [],
      key: '',
      token: '',
      link: {
        URL: '',
        img: '',
        title: '',
        saved: false
      }
    }
  },
  computed: {
    imgs: function () {
      let img = []
      for (let i in this.uploadImgs) {
        if (this.uploadImgs[i].status === 'success') {
          img.push(this.uploadImgs[i].url)
        }
      }
      return img
    }
  },
  methods: {
    onDialogClose: function () {
      this.$emit('closeDialog')
    },
    publish () {
      var _this = this
      _this.publishLoading = true
      this.$http.post('/api/v1/feeds/', {
        type: 'text',
        text: this.text,
        img: this.imgs
      })
        .then((response) => {
          this.$store.commit('showSnackbar', { text: '发表成功' })
          this.text = ''
          this.publishLoading = false
          this.$router.go(-1)
        })
        .catch((error) => {
          _this.$store.commit('showSnackbar', { text: '登陆失败' + error })
        })
    },
    onImgAdd () {
      this.$refs.testform.userfile.click()
    },
    clearImgs () {
      this.uploadImgs = []
      this.$refs.testform.userfile.value = ''
      console.log(this.$refs.testform.userfile.files)
    },
    upload (e) {
      console.log(e.target)
      var userfile = e.target.files[0]
      var selectedFile = userfile.name
      if (selectedFile) {
        var ramdomName = Math.random().toString(36).substr(2) + userfile.name.match(/\.?[^./]+$/)
        this.key = 'feed_' + this.$store.state.user.cardID + '_' + ramdomName
        this.uploadImgs.push({ name: selectedFile, status: 'pending', url: this.key })
      } else {
        return false
      }
      this.$http.get(`/api/v1/upload/token?key=${this.key}`)
        .then((response) => {
          this.token = response.data.uptoken
          this.$nextTick(
            () => {
              var f = new FormData(this.$refs.testform)
              this.$http.post('/upload', f)
                .then((response) => {
                  for (let i in this.uploadImgs) {
                    if (this.uploadImgs[i].url === response.data.key) {
                      this.uploadImgs[i].status = 'success'
                    }
                  }
                })
                .catch((error) => {
                  console.log(error)
                  for (let i in this.uploadImgs) {
                    if (this.uploadImgs[i].url === this.key) {
                      this.uploadImgs[i].status = 'failed'
                    }
                  }
                })
            }
          )
        })
    }
  }
}
</script>

<style>
#testform {
  display: none;
}
</style>
