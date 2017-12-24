<template>
  <!-- <v-dialog v-model="dialog" persistent fullscreen transition="slide-x-reverse-transition" :overlay="false"> -->
    <v-card>
      <!-- <v-toolbar dark class="dark-primary">
        <v-btn icon @click.native="$router.go(-1)" dark>
          <v-icon>iconfont-close</v-icon>
        </v-btn>
        <v-toolbar-title>查看动态</v-toolbar-title>
      </v-toolbar> -->
      <feed :index="index" :feed="feed" class="mt-3" @onLikeClick="onLikeClick" showDel></feed>
      <comment post="feed" :id="$route.params.id" @delete="$router.go(-1)"></comment>
    </v-card>
  <!-- </v-dialog> -->
</template>
<script>
import comment from '@/components/comment.vue'
import feed from '@/components/feed'
export default {
  components: {
    feed,
    comment
  },
  props: {
    index: {
      type: Number
    }
  },
  beforeDestroy () {
    this.dialog = false
  },
  data () {
    return {
      dialog: false,
      feed: {
        user: {},
        created: 'null',
        img: []
      },
      content: '',
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
      },
      comments: []
    }
  },
  // watch: {
  //   dialog: function (val) {
  //     if (val) {
  //       this.getFeed()
  //       this.getComments()
  //     }
  //   }
  // },
  // created () {
  //   this.dialog = true
  // },
  mounted () {
    // this.dialog = true
    this.getFeed()
    // this.getComments()
  },
  methods: {
    onDialogClose: function () {
      this.$emit('closeDialog')
    },
    onLikeClick () {
      this.$http.get(`/api/v1/feeds/${this.$route.params.id}/like`)
      this.getFeed()
    },
    getFeed () {
      this.$http.get(`/api/v1/feeds/${this.$route.params.id}`)
        .then((response) => {
          this.feed = response.data
          this.$nextTick(function () {
            this.dialog = true
          })
        })
        .catch((error) => {
          console.log(error)
          this.$router.go(-1)
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
