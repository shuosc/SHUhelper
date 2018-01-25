<template lang="pug">
  q-card(:key="feed.id" :flat="flat" style="margin:0.8rem 0 0 0 ;" @click="$router.push(`/feeds/${feed.id}`)")
    q-card-title.no-padding 
    q-item(dense @click.stop="$router.push(`/profile/${feed.user.cardID}`)")
      q-item-side
        q-item-tile(avatar)
          img(:src="`https://static.shuhelper.cn/${feed.user.avatar}`")
      q-item-main
        q-item-tile(label) {{feed.user.name}}
        q-item-tile(sublabel)  {{[feed.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
      q-item-side
        q-btn(icon="delete" flat v-if="feed.user.cardID == $store.state.user.cardID" @click.stop="deleteFeed")
    q-card-separator
    q-card-main 
      p(v-for="paragraph in feed.text.split('\\n')")
        | {{ paragraph }}
    div.row.flex.xs-gutter(v-if="feed.img.length !== 0" style="padding:0.5rem;")
      div.col-4(v-for="(img,key) in feed.img" :key="key" @click.stop="")
        img(:src="`${img}-slim75`" @click="showImg(img)"
        style="object-fit: cover;width:100%;height:100%;" 
        alt="lorem")
    q-card-separator
    q-card-actions.justify-between
      q-item.no-padding(dense)
          <q-item-main>
          //- <q-item-tile label>Notifications</q-item-tile>
          <q-item-tile sublabel>{{feed.hits}}次浏览</q-item-tile>
          </q-item-main>
      div
        q-btn(small :class="{'text-pink':feed.liked}" flat @click.stop="onLikeClick(index)")
          q-icon(name="favorite")
          span(style="color:grey;font-size:1rem;")
            | {{feed.likecount}}
        q-btn(flat small)
          q-icon(name="comment")
          span(style="color:grey;font-size:1rem;")
            | {{feed.comments.length}}
    q-card(flat)
      small.text-faded(v-if="feed.like.length")
        span(v-for="(user,ui) in feed.like")
          span(v-show="ui!==0") 、
          | {{user.name}}
        span 喜欢了这条动态
      q-list(dense v-if="comments")
        q-item.no-padding(v-for="(comment,index) in feed.comments" :key="index")
          q-item-main
            small
              span.text-primary
                | {{comment.user.name}}: 
              | {{ comment.text }}

  //- <!-- <v-card class="mt-3"> -->
    <v-container grid-list-lg v-if="feed.linkURL !== ''" style="border-style:solid;border-width:2px;border-color:#eee;" class="pa-0 ma-2" @click.stop>
      <v-layout row style="min-height:5rem;">
        <v-flex xs3>
          <v-card-media v-if="feed.linkImg" src="/static/107.jpg" style="height:100%;" contain></v-card-media>
          <v-icon x-large v-else style="height:100%;display:flex;" class="blue--text text--darken-2">public</v-icon>
        </v-flex>
        <v-flex xs9>
          <a :href="feed.linkURL" target="_blank" style="text-decoration:none;">
            <p style="font-size:1rem;height:100%;" class="black--text text-xs-left py-2 ma-0">
              {{feed.linkTitle}}<br/>
              <span style="color:grey;font-size:0.8rem;">{{feed.linkURL|urlHost}} </span>
            </p>
          </a>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
// import denseComment from '@/components/denseComment.vue'
import { parseURL } from '@/../libs/utils.js'
import { Dialog } from 'quasar'
export default {
  components: {
    // denseComment
  },
  props: {
    feed: {
      type: Object,
      default() {
        return {
          user: {}
        }
      }
    },
    index: {
      type: Number
    },
    comments: {
      type: Boolean
    },
    flat: {
      type: Boolean
    },
    showDel: {
      type: Boolean,
      default() {
        return false
      }
    }
  },
  filters: {
    urlHost: function(value) {
      return parseURL(value).host
    }
  },
  watch: {
    show: function(val) {
      if (val) {
        this.$store.commit('hideBottomNavgation')
      } else {
        this.$store.commit('showBottomNavgation')
      }
    }
  },
  data() {
    return {
      showModal: false,
      delDialog: false,
      show: false,
      delete: false
    }
  },
  computed: {
    imgs() {
      // console.log(this.feed.img)
      let img = this.feed.img.map(val => {
        return '//static.shuhelper.cn/' + val
      })
      // console.log(img)
      return img
    }
  },
  methods: {
    showImg(img) {
      this.$q.events.$emit('app:showImg', img)
    },
    onLikeClick(index) {
      let id = this.feed.id
      this.$http.get(`/api/feeds/${id}/like`).then(response => {
        this.feed = response.data
      })
    },
    deleteFeed() {
      Dialog.create({
        title: '提示',
        message: '确定要删除吗',
        buttons: [
          '取消',
          {
            label: '删除',
            handler: () => {
              this.$http.delete(`/api/feeds/${this.feed.id}`).then(response => {
                this.$emit('delete')
              })
            }
          }
        ]
      })
    }
  }
}
</script>
