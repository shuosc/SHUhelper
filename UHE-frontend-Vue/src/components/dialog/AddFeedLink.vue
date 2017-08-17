<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" persistent fullscreen transition="dialog-bottom-transition" :overlay="false">
        <v-card>
          <v-toolbar dark class="primary">
            <v-btn icon @click.native="onDialogClose()" dark>
              <v-icon>close</v-icon>
            </v-btn>
            <v-toolbar-title>推荐链接</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon @click.native="publish()" dark>
              <v-progress-circular v-show="publishLoading" :indeterminate="publishLoading" class="red--text"></v-progress-circular>发 布
            </v-btn>
          </v-toolbar>
          <v-container fluid class="pa-1 ma-0">
            <v-text-field name="input-1" counter max="450" autofocus full-width v-model="text" label="说点什么.." multi-line hint="您正在以身份登录<br/>测试阶段 正式运营时您发表的内容可能被移除"></v-text-field>
          </v-container>
          <v-container fluid class="pa-0 ma-0">
            <v-layout row class="pa-0 ma-0" wrap>
              <v-subheader>推荐链接</v-subheader>
              <v-spacer></v-spacer>
              <v-btn flat @click.native="saveLink">获取链接信息</v-btn>
            </v-layout>
          </v-container>
          <v-divider></v-divider>
          <v-container fluid v-if="!link.saved" class="px-3 py-0">
            <v-layout row wrap>
              <v-flex xs12>
                <v-text-field label="复制想要推荐的链接 在此粘贴" hide-details single-line v-model="link.URL"></v-text-field>
              </v-flex>
               <v-flex xs12>
                <v-text-field label="获取标题失败请手动填写" hide-details single-line v-model="link.title"></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
          <v-container grid-list-lg v-else style="border-style:solid;border-width:1px;border-color:#eee;" class="pa-0 ma-2">
            <v-layout row style="min-height:5rem;">
              <v-flex xs3>
                <v-card-media src="/static/107.jpg" style="height:100%;" contain></v-card-media>
              </v-flex>
              <v-flex xs9>
                <p style="font-size:1rem;height:100%;" class="black--text text-xs-left py-2 ma-0">上事记|你要的夏天，会是什么味道</p>
              </v-flex>
            </v-layout>
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
      this.publishLoading = true
      this.$http.post('/api/feeds/', {
        type: 'link',
        text: this.text,
        linkURL: this.link.URL,
        linkImg: this.link.img,
        linkTitle: this.link.title
      })
        .then((response) => {
          this.$store.commit('showSnackbar', { text: '发表成功' })
          this.text = ''
          this.publishLoading = false
          this.$emit('closeDialog')
        })
        .catch((error) => {
          this.$store.commit('showSnackbar', { text: '登陆失败' + error })
        })
    },
    saveLink () {
      this.$http.get(`/api/feeds/link?link=${this.link.URL}`)
        .then((response) => {
          this.link.title = response.data.title
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
