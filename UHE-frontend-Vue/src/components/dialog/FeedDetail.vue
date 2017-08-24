<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" persistent fullscreen transition="dialog-bottom-transition" :overlay="false">
        <v-card>
          <v-toolbar dark class="primary">
            <v-btn icon @click.native="onDialogClose()" dark>
              <v-icon>close</v-icon>
            </v-btn>
            <v-toolbar-title>查看动态</v-toolbar-title>
          </v-toolbar>
          <v-container fluid class="pa-1 ">
            <feed :index="index" :feed="feed" class="mt-3" @onLikeClick="onLikeClick"></feed>
          </v-container>
          <v-container fluid class="pa-1 ">
            <v-card v-for="comment in comments" :key="comment._id">
              <v-card-text>{{comment.content}}</v-card-text>
            </v-card>
          </v-container>
        </v-card>
      </v-dialog>
    </v-layout>
  </div>
</template>
<script>
import feed from '@/components/feed'
export default {
  components: {
    feed
  },
  props: {
    dialog: {
      type: Boolean,
      default () {
        return false
      }
    },
    feed: {
      type: Object
    },
    index: {
      type: Number
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
  methods: {
    onDialogClose: function () {
      this.$emit('closeDialog')
    },
    onFeedClick () {
      this.$emit('onFeedClick', this.index)
    },
    onLikeClick () {
      this.$emit('onLikeClick', this.index)
    }
  }
}
</script>

<style>
#testform {
  display: none;
}
</style>
