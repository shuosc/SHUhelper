<template>
  <v-flex xs12 class="pb-5">
    <loadmore :top-method="resetFeeds" :bottom-method="loadBottom"
      @top-status-change="handleTopChange" :bottom-all-loaded="allLoaded"
      ref="loadmore" v-infinite-scroll="getFeeds" infinite-scroll-distance="10">
      <v-card v-for="(feed,index) in feeds" :key="index"
        class="mt-3">
        <v-container fluid grid-list-lg class="py-0">
          <v-layout row>
            <v-flex xs2>
              <v-card-media :src="`//static.shuhelper.cn/${feed.user.avatar}`"
                height="2.5rem" contain></v-card-media>
            </v-flex>
            <v-flex xs10>
              <div>
                <div style="font-size:1.1rem;" class="teal--text">{{feed.user.name}}</div>
                <div style="font-size:0.5rem;" class="grey--text">
                  {{$moment(feed.created,'YYYY-MM-DD hh:mm:ss').fromNow()}}
                </div>
              </div>
            </v-flex>
          </v-layout>
        </v-container>
        <v-container class="pb-0 pt-3 px-3">
          <v-layout row>
            <v-flex xs12>
              {{feed.text}}</v-flex>
          </v-layout>
        </v-container>
        <v-container fluid v-if="feed.img.length !== 0" grid-list-sm
          class="pa-3">
          <v-layout row wrap>
            <v-flex xs4 v-for="(img,key) in feed.img" :key="key">
              <img v-img="{group:index}" :src="`//static.shuhelper.cn/${img}-slim75`"
                style="object-fit: cover;" alt="lorem"
                width="100%" height="100%" />
            </v-flex>
          </v-layout>
        </v-container>
        <v-container grid-list-lg v-if="feed.linkURL !== ''"
          style="border-style:solid;border-width:2px;border-color:#eee;"
          class="pa-0 ma-2">
          <v-layout row style="min-height:5rem;">
            <v-flex xs3>
              <v-card-media v-if="feed.linkImg" src="/static/107.jpg"
                style="height:100%;" contain></v-card-media>
              <v-icon x-large v-else style="height:100%;display:flex;"
                class="blue--text text--darken-2">public</v-icon>
            </v-flex>
            <v-flex xs9>
              <p style="font-size:1rem;height:100%;" class="black--text text-xs-left py-2 ma-0"
                @click="this.window.open(feed.linkURL)">{{feed.linkTitle}}</p>
            </v-flex>
          </v-layout>
        </v-container>
        <v-card-actions class="white">
          <v-spacer></v-spacer>
          <v-btn icon>
            <v-icon>favorite</v-icon>
            <span v-for="people in feed.liked" :key="people.id">{{people}}</span>
          </v-btn>
          <v-btn icon>
            <v-icon>comment</v-icon>{{feed.comments}}
          </v-btn>
        </v-card-actions>
      </v-card>
      <!-- <v-container slot="top" class="mint-loadmore-top">
          <v-layout align-center>
            <v-flex xs12 style="text-align:center;">
              <span v-show="topStatus !== 'loading'" :class="{ 'rotate': topStatus === 'drop' }">↓</span>
              <v-progress-circular v-show="topStatus === 'loading'"
                indeterminate class="primary--text"></v-progress-circular>
            </v-flex>
          </v-layout>
        </v-container> -->
      <v-container slot="bottom">
        <v-layout align-center>
          <v-flex xs12 style="text-align:center;">
            <v-progress-circular v-show="loading&&!allLoaded"
              indeterminate class="primary--text"></v-progress-circular>
            <span v-show="allLoaded">no more data :)</span>
          </v-flex>
        </v-layout>
      </v-container>
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
  </v-flex>
</template>
<script>
import AddFeedText from '@/components/dialog/AddFeedText'
import AddFeedLink from '@/components/dialog/AddFeedLink'
// import InfiniteLoading from 'vue-infinite-loading'
// import VuePullRefresh from 'vue-pull-refresh'
import { Loadmore } from 'mint-ui'

export default {
  components: {
    AddFeedText,
    AddFeedLink,
    Loadmore
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
      topStatus: ''
    }
  },
  methods: {
    handleTopChange (status) {
      this.topStatus = status
    },
    getFeeds () {
      if (this.loading) return
      this.loading = true
      this.$http.get(`/api/feeds/?page=${this.page}`)
        .then((response) => {
          this.feeds = this.feeds.concat(response.data)
          this.loading = false
          this.allLoaded = false
          this.$refs.loadmore.onTopLoaded()
          this.page += 1
          // this.$store.commit('showSnackbar', { text: '获取成功' })
        })
        .catch((error) => {
          console.log(error)
          this.allLoaded = true
          // this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
          this.loading = false
          // this.$store.commit('showSnackbar', { text: error })
        })
    },
    loadBottom () {
      console.log('loadBottom')
    },
    resetFeeds () {
      this.feeds = []
      this.page = 1
      this.loading = false
      this.getFeeds()
    },
    closeDialog () {
      this.addTextDialog = false
      this.addLinkDialog = false
      this.resetFeeds()
    }
  }
}
</script>
