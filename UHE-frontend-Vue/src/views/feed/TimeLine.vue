<template>
  <v-flex xs12 class="pb-5">
    <loadmore :top-method="resetFeeds" @top-status-change="handleTopChange"
      ref="loadmore">
      <feed v-for="(feed,index) in feeds" :key="index"
        :index="index" :feed="feed" class="mt-3" @onFeedClick="onFeedClick"
        @onLikeClick="onLikeClick"></feed>

    </loadmore>
    <v-speed-dial v-model="fab" fixed right direction="top"
      style="bottom:60px;" transition="slide-y-reverse-transition"
      v-show="$store.state.ui.bottomNavigationVisible">
      <v-btn slot="activator" class="blue darken-2" dark
        fab v-model="fab">
        <v-icon>add</v-icon>
        <v-icon>close</v-icon>
      </v-btn>
      <v-btn fab dark small class="green" @click="addTextDialog=true">
        <v-icon>edit</v-icon>
      </v-btn>
      <v-btn fab dark small class="indigo" @click="addLinkDialog=true">
        <v-icon>link</v-icon>
      </v-btn>
    </v-speed-dial>
    <add-feed-text :dialog="addTextDialog" @closeDialog="closeDialog"></add-feed-text>
    <add-feed-link :dialog="addLinkDialog" @closeDialog="closeDialog"></add-feed-link>
    <feed-detail :dialog="FeedDialog" @closeDialog="closeFeedDialog"
      :feed="feed"> </feed-detail>
  </v-flex>
</template>
<script>
import FeedDetail from '@/components/dialog/FeedDetail'
import feed from '@/components/feed'
import AddFeedText from '@/components/dialog/AddFeedText'
import AddFeedLink from '@/components/dialog/AddFeedLink'
import InfiniteLoading from 'vue-infinite-loading'
// import VuePullRefresh from 'vue-pull-refresh'
import { Loadmore } from 'mint-ui'

export default {
  components: {
    AddFeedText,
    AddFeedLink,
    Loadmore,
    FeedDetail,
    feed,
    InfiniteLoading
  },
  created () {
    // this.resetFeeds()
  },
  data () {
    return {
      addLinkDialog: false,
      addTextDialog: false,
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
      }
    }
  },
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
      console.log('onFeedClick')
      this.feed = this.feeds[index]
      this.FeedDialog = true
      console.log(this.feed)
    },
    handleTopChange (status) {
      this.topStatus = status
    },
    loadContent () {
      this.getFeeds()
    },
    getFeeds () {
      if (this.loading) return
      this.loading = true
      this.$http.get(`/api/feeds/?page=${this.page}`)
        .then((response) => {
          for (let i in response.data) {
            let feed = response.data[i]
            var cardID = this.$store.state.user.cardID
            feed.liked = feed.like.findIndex((user) => { return user._id === cardID }) !== -1
            feed.likecount = feed.like.length
            this.feeds.push(feed)
            // console.log(feed)
          }
          this.$emit('loaded')
          // this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
          this.loading = false
          this.allLoaded = false
          this.$refs.loadmore.onTopLoaded()
          this.page += 1
          // this.$store.commit('showSnackbar', { text: '获取成功' })
        })
        .catch((error) => {
          console.log(error)
          this.allLoaded = true
          // console.log(this.allLoaded)
          this.$emit('loadingComplete')
          // this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
          this.loading = false
          // this.$store.commit('showSnackbar', { text: error })
        })
    },
    loadBottom () {
      console.log('loadBottom')
    },
    resetFeeds () {
      this.allLoaded = false
      this.feeds = []
      this.page = 1
      this.loading = false
      this.$emit('loadingReset')
      // this.$refs.infiniteLoading.$emit('$InfiniteLoading:reset')
      this.getFeeds()
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
