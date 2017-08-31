<template>
  <v-flex xs12 class="">
    <loadmore :top-method="resetFeeds" @top-status-change="handleTopChange" ref="loadmore">
      <!-- v-infinite-scroll="getFeeds" infinite-scroll-disabled="loading" infinite-scroll-distance="10" -->
      <!-- <scroller :on-refresh="resetFeeds" :on-infinite="getFeeds" ref="loadmore"> -->
      <feed v-for="(feed,index) in feeds" :key="index" :index="index" :feed="feed" class="mt-3" @onFeedClick="onFeedClick" @onLikeClick="onLikeClick" @delete="onFeedDelete"></feed>
      <!-- </scroller> -->
    </loadmore>
    <infinite-loading :on-infinite="getFeeds" ref="infiniteLoading"></infinite-loading>
    <v-speed-dial v-model="fab" fixed right direction="top" style="bottom:60px;" transition="slide-y-reverse-transition" v-show="$store.state.ui.bottomNavigationVisible">
      <v-btn slot="activator" class="blue darken-2" dark fab v-model="fab">
        <v-icon>add</v-icon>
        <v-icon>close</v-icon>
      </v-btn>
      <v-btn fab dark small class="green" @click="$router.push('/square/feed-add-text')">
        <v-icon>edit</v-icon>
      </v-btn>
      <v-btn fab dark small class="indigo" @click="$router.push('/square/feed-add-link')">
        <v-icon>link</v-icon>
      </v-btn>
    </v-speed-dial>
    <router-view></router-view>
    </v-layout>
  </v-flex>
</template>
<script>
import FeedDetail from '@/components/dialog/FeedDetail'
import feed from '@/components/feed'
import AddFeedText from '@/components/dialog/AddFeedText'
import AddFeedLink from '@/components/dialog/AddFeedLink'
import InfiniteLoading from '@/vue-infinite-loading/src/components/InfiniteLoading.vue'
// import VuePullRefresh from 'vue-pull-refresh'
import { Loadmore, InfiniteScroll } from 'mint-ui'
import comment from '@/components/comment.vue'
export default {
  components: {
    AddFeedText,
    AddFeedLink,
    Loadmore,
    FeedDetail,
    InfiniteScroll,
    feed,
    InfiniteLoading,
    comment
  },
  created () {
    // this.resetFeeds()
  },
  watch: {
    // '$route' (to, from) {
    //   if (to.matched.some(record => record.meta.dialog)) {
    //     this.dialog = true
    //   } else {
    //     this.dialog = false
    //   }
    // }
  },
  data () {
    return {
      fab: false,
      feeds: [],
      loading: false,
      page: 1,
      allLoaded: false,
      topStatus: '',
      FeedDialog: false,
      feed: {
        user: {},
        img: []
      },
      model: false,
      fresh: false
    }
  },
  // beforeRouteLeave(to, from, next) {
  //   console.log(to)
  //   // 导航离开该组件的对应路由时调用
  //   // 可以访问组件实例 `this`
  // },
  computed: {
    // liked: function (feed) {
    //   console.log(feed)
    //   function checkIn (user) {
    //     return user._id === this.$store.state.user.cardID
    //   }
    //   if (feed.like.findIndex(checkIn) !== -1) {
    //     return true
    //   } else {
    //     return false
    //   }
    // }
  },
  methods: {
    onLikeClick (index) {
      let id = this.feeds[index].id
      this.$http.get(`/api/feeds/${id}/like`)
      if (this.feeds[index].liked) {
        this.feeds[index].likecount -= 1
        this.feeds[index].liked = false
      } else {
        this.feeds[index].likecount += 1
        this.feeds[index].liked = true
      }
    },
    onFeedClick (index) {
      // console.log('onFeedClick')
      this.feed = this.feeds[index]
      this.$router.push(`/square/feed-detail/${this.feed.id}`)
      // console.log(this.$route)
      // this.FeedDialog = true
      // console.log(this.feed)
    },
    onFeedDelete (index) {
      this.feeds.splice(index, 1)
    },
    handleTopChange (status) {
      this.topStatus = status
    },
    loadContent () {
      this.getFeeds()
    },
    getFeedsRAF () {
      requestAnimationFrame(this.getFeedsReal)
    },
    getFeeds () {
      this.loading = true
      var now = new Date()
      this.$http.get(`/api/feeds/?page=${this.page}`)
        .then((response) => {
          console.log('request complete', new Date() - now)
          // var cardID = this.$store.state.user.cardID
          for (let i in response.data) {
            let feed = response.data[i]
            feed.likecount = feed.like.length
            this.feeds.push(feed)
          }
          console.log('loaded')
          this.$emit('loaded')
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
          this.loading = false
          this.allLoaded = false
          if (this.fresh) {
            // this.$refs.loadmore.finishPullToRefresh()
            this.$refs.loadmore.onTopLoaded()
            this.fresh = false
          }
          // this.$refs.loadmore.onTopLoaded()
          // this.$refs.loadmore.finishInfinite()
          this.page += 1
          // this.$store.commit('showSnackbar', { text: '获取成功' })
        })
        .catch((error) => {
          console.log(error)
          this.allLoaded = true
          // console.log(this.allLoaded)
          this.$emit('loadingComplete')
          // this.$refs.loadmore.finishInfinite(true)
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
          this.loading = true
          // this.$store.commit('showSnackbar', { text: error })
        })
    },
    loadBottom () {
      console.log('loadBottom')
    },
    resetFeeds () {
      this.fresh = true
      this.allLoaded = false
      this.feeds = null
      this.feeds = []
      this.page = 1
      this.loading = false
      this.$emit('loadingReset')
      this.$refs.infiniteLoading.$emit('$InfiniteLoading:reset')
      // this.getFeeds()
    },
    closeDialog () {
      this.addTextDialog = false
      this.addLinkDialog = false
      this.resetFeeds()
    },
    closeFeedDialog () {
      this.FeedDialog = false
    }
  }
}
</script>
