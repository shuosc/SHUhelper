<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" persistent fullscreen transition="dialog-bottom-transition" :overlay="false" >
        <v-card >
          <v-toolbar dark fixed class="primary">
            <v-btn icon @click.native="$router.go(-1)" dark>
              <v-icon>close</v-icon>
            </v-btn>
            <v-toolbar-title>查看动态</v-toolbar-title>
          </v-toolbar>
          <v-container fluid class="pa-0 mb-2" style="height:100%;overflow:scroll;margin-top:64px;">
            <feed :index="index" :feed="feed" class="mt-3" @onLikeClick="onLikeClick"></feed>
          </v-container>
          <comment post="feed" :id="$route.params.id" @delete="$router.go(-1)"></comment>
        </v-card>
      </v-dialog>
    </v-layout>
  </div>
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
  mounted () {
    // this.dialog = true
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
  created () {
    this.getFeed()
    // this.getComments()
  },
  methods: {
    onDialogClose: function () {
      this.$emit('closeDialog')
    },
    onLikeClick () {
      this.$http.get(`/api/feeds/${this.$route.params.id}/like`)
      this.getFeed()
    },
    getFeed () {
      this.$http.get(`/api/feeds/${this.$route.params.id}`)
        .then((response) => {
          this.feed = response.data
          this.dialog = true
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
