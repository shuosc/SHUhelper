<template>
  <v-card class="mt-3">
    <v-container fluid grid-list-lg class="py-0">
      <v-layout row @click.stop="$router.push(`/profile/${feed.user.cardID}`)">
        <v-flex xs2 style="text-align:center;">
          <v-avatar size="3rem">
            <img :src="`//static.shuhelper.cn/${feed.user.avatar}`" alt="avatar">
          </v-avatar>
          <!-- <v-card-media :src="`//static.shuhelper.cn/${feed.user.avatar}`" height="2.5rem" contain></v-card-media> -->
        </v-flex>
        <v-flex xs4>
          <div style="display:inline-block;">
            <div style="font-size:1.1rem;" class="">{{feed.user.name}}</div>
            <div style="font-size:0.5rem;" class="secondary-text">
              {{[feed.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
            </div>
          </div>
        </v-flex>
        <v-flex xs6 @click.stop>
          <!-- <v-spacer></v-spacer> -->
          <div style="display:inline-block;float:right;" v-show="showDel" @click.stop>
            <v-menu bottom right v-show="feed.user.cardID===$store.state.user.cardID">
              <v-btn icon slot="activator" light>
                <v-icon>more_vert</v-icon>
              </v-btn>
              <v-list>
                <v-list-tile @click.stop="delDialog=true">
                  <v-list-tile-title>删除</v-list-tile-title>
                </v-list-tile>
              </v-list>
            </v-menu>
          </div>
        </v-flex>
        </v-flex>
      </v-layout>
    </v-container>
    <v-dialog v-model="delDialog" lazy absolute style="z-index:10 !important;">
      <v-card>
        <v-card-title>
          <div class="headline">确认删除吗？</div>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="green--text darken-1" flat="flat" @click.native="delDialog = false">返回</v-btn>
          <v-btn class="green--text darken-1" flat="flat" @click.native="deleteFeed(feed.id)">确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-container class="pb-0 pt-3 px-3">
      <v-layout row wrap>
        <v-flex xs12>
          <p v-for="paragraph in feed.text.split('\n')">
            {{ paragraph }}</p>
        </v-flex>
      </v-layout>
    </v-container>
    <v-container fluid v-if="feed.img.length !== 0" grid-list-sm class="pa-3">
      <v-layout row wrap>
        <v-flex xs4 v-for="(img,key) in imgs" :key="key" @click.stop>
          <!-- <lightbox :thumbnail="`${img}-slim75`" :images="imgs"></lightbox> -->
          <img v-img="{group:index}" :src="`${img}-slim75`" style="object-fit: cover;" alt="lorem" width="100%" />
        </v-flex>
      </v-layout>
    </v-container>
    <v-container grid-list-lg v-if="feed.linkURL !== ''" style="border-style:solid;border-width:2px;border-color:#eee;" class="pa-0 ma-2" @click.stop>
      <v-layout row style="min-height:5rem;">
        <v-flex xs3>
          <v-card-media v-if="feed.linkImg" src="/static/107.jpg" style="height:100%;" contain></v-card-media>
          <v-icon x-large v-else style="height:100%;display:flex;" class="blue--text text--darken-2">public</v-icon>
        </v-flex>
        <v-flex xs9>
          <a :href="feed.linkURL" target="_blank">
            <p style="font-size:1rem;height:100%;" class="black--text text-xs-left py-2 ma-0">
              {{feed.linkTitle}}<br/>
              <span style="color:grey;font-size:0.8rem;">{{feed.linkURL|urlHost}} </span>
            </p>
          </a>
        </v-flex>
      </v-layout>
    </v-container>
    <v-card-actions>
      <!-- <span v-for="people in feed.liked" :key="people.id" style="font-size:0.8rem;">{{people.name}}</span> -->
      <v-spacer></v-spacer>
      <v-btn icon @click.stop="onLikeClick()">
        <v-icon :class="{'pink--text':feed.liked}">favorite</v-icon>{{feed.likecount}}
      </v-btn>
      <v-btn icon @click.stop="show=!show">
        <v-icon>comment</v-icon>{{feed.comments.length}}
      </v-btn>
    </v-card-actions>
    <v-card v-if="!show" flat>
      <v-card v-for="comment in feed.comments" :key="comment._id" class="mb-0" flat>
        <v-container fluid class="py-1 px-3">
          <v-layout row @click.stop="$router.push(`/profile/${comment.user.cardID}`)">
            <v-flex xs11>
              <div style="display:block;">
                <div style="font-size:1rem;" class="">
                  <span class="blue--text">{{comment.user.name}}</span>: {{comment.content}}</div>
              </div>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-card>
    <v-slide-y-transition>
      <dense-comment v-if="show" post="feed" :id="feed.id" @delete="$router.go(-1)"></dense-comment>
    </v-slide-y-transition>
  </v-card>
</template>

<script>
import denseComment from '@/components/denseComment.vue'
import { parseURL } from '@/libs/utils.js'
export default {
  components: {
    denseComment
  },
  props: {
    feed: {
      type: Object,
      default () {
        return {
          user: {}
        }
      }
    },
    index: {
      type: Number
    },
    showDel: {
      type: Boolean,
      default () {
        return false
      }
    }
  },
  filters: {
    urlHost: function (value) {
      return parseURL(value).host
    }
  },
  watch: {
    show: function (val) {
      if (val) {
        this.$store.commit('hideBottomNavgation')
      } else {
        this.$store.commit('showBottomNavgation')
      }
    }
  },
  data () {
    return {
      showModal: false,
      delDialog: false,
      show: false
    }
  },
  computed: {
    imgs () {
      // console.log(this.feed.img)
      let img = this.feed.img.map((val) => { return '//static.shuhelper.cn/' + val })
      // console.log(img)
      return img
    }
  },
  methods: {
    deleteFeed (id) {
      this.$http.delete(`/api/v1/feeds/${id}`).then((response) => {
        // this.getComments()
        this.$store.commit('showSnackbar', { text: '删除成功，刷新页面后生效' })
        this.$emit('delete')
        this.delDialog = false
      })
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
