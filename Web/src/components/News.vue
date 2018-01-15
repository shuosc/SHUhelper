<template>
  <div>
    <q-toolbar color="primary">
      <q-toolbar-title>
        <q-btn flat round small class="primary" v-go-back="'/index'">
          <q-icon name="keyboard_backspace" /></q-btn>
        新闻
      </q-toolbar-title>
    </q-toolbar>
    <q-tabs v-model="selectedTab">
      <!-- Tabs - notice slot="title" -->
      <q-tab default slot="title" label="通知公告" name="tab-1" />
      <q-tab slot="title" label="学工办通告" name="tab-2" />
      <q-tab slot="title" label="教务通知" name="tab-3" />
      <!-- <q-tab slot="title" label="实习就业" name="tab-4" /> -->
      <!-- Targets -->
      <q-tab-pane name="tab-1" class="no-padding">
        <!-- <q-toolbar slot="header">...</q-toolbar> -->
        <q-infinite-scroll :handler="loadMoreSHU" ref="infiniteScrollSHU" style="text-align:center;">
          <news-card v-for="(news,index) in news.SHU" :news="news" :key="index" @click.native="onNewsClick('SHU',index)"></news-card>
          <q-spinner-dots slot="message" :size="40"></q-spinner-dots>
        </q-infinite-scroll>
      </q-tab-pane>
      <q-tab-pane name="tab-2" class="no-padding">
        <q-infinite-scroll :handler="loadMoreXGB" ref="infiniteScrollXGB" style="text-align:center;">
          <news-card v-for="(news,index) in news.XGB" :news="news" :key="index" @click.native="onNewsClick('XGB',index)"></news-card>
          <q-spinner-dots slot="message" :size="40"></q-spinner-dots>
        </q-infinite-scroll>
      </q-tab-pane>
      <q-tab-pane name="tab-3" class="no-padding">
        <q-infinite-scroll :handler="loadMoreJWC" ref="infiniteScrollJWC" style="text-align:center;">
          <news-card v-for="(news,index) in news.JWC" :news="news" @click.native="onNewsClick('JWC',index)" :key="index"></news-card>
          <q-spinner-dots slot="message" :size="40"></q-spinner-dots>
        </q-infinite-scroll>
      </q-tab-pane>
      <q-tab-pane name="tab-4" class="no-padding">
        <q-infinite-scroll :handler="loadMoreJYB" ref="infiniteScrollJYB" style="text-align:center;">
          <news-card v-for="(news,index) in news.JYB" :news="news" @click.native="onNewsClick('JYB',index)" :key="index"></news-card>
          <q-spinner-dots slot="message" :size="40"></q-spinner-dots>
        </q-infinite-scroll>
      </q-tab-pane>
      <q-btn v-back-to-top v-back-to-top.animate="{offset: 500, duration: 200}" round color="teal-5" class="fixed-bottom-right" style="margin: 0 15px 15px 0">
        <q-icon name="keyboard_arrow_up" />
      </q-btn>
      <q-modal v-model="open">
        <q-modal-layout>
          <q-toolbar slot="header" inverted>
            <q-btn color="primary" flat @click="open = false">
              <q-icon name="close" />
              <q-toolbar-title>
                新闻详情
              </q-toolbar-title>
            </q-btn>
          </q-toolbar>
          <q-card>
            <q-card-title>{{newsSingle.title}}</q-card-title>
            <q-card-main v-html="newsSingle.detail"></q-card-main>
          </q-card>
          <q-inner-loading :visible="loading">
            <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
          </q-inner-loading>
        </q-modal-layout>
      </q-modal>
    </q-tabs>
  </div>
</template>

<script>
import NewsCard from '@/NewsCard.vue'
import {
  QTabs,
  QTab,
  QTabPane,
  QSpinnerGears,
  QInnerLoading,
  BackToTop,
  GoBack
} from 'quasar'
export default {
  components: {
    NewsCard,
    QTabs,
    QTab,
    QTabPane,
    QSpinnerGears,
    QInnerLoading
  },
  directives: {
    BackToTop,
    GoBack
  },
  data() {
    return {
      loading: false,
      selectedTab: 'tab-1',
      open: false,
      news_all: [],
      news: {
        XGB: [],
        SHU: [],
        JYB: [],
        JWC: [],
        SHUNEWS: []
      },
      page: 1,
      newsSingle: {
        title: '',
        detail: '',
        type: ''
      }
    }
  },
  created() {},
  methods: {
    onNewsClick(category, index) {
      this.newsSingle = this.news[category][index]
      this.newsSingle.type = category
      this.open = true
      this.loading = true
      if (category === 'XGB') {
        this.$http
          .get('/mobile/campusmessage/GetXgbCampusMessageById', {
            params: {
              MsgID: this.newsSingle.MsgID
            }
          })
          .then(response => {
            this.newsSingle.detail = response.data.Summary
            this.loading = false
            // this.$nextTick(() => {
            // })
          })
      } else if (category === 'SHU') {
        this.$http
          .get('/mobile/campusmessage/GetCampusMessageById', {
            params: {
              MsgID: this.newsSingle.MsgID
            }
          })
          .then(response => {
            this.newsSingle.detail = response.data.Summary
            this.loading = false
            // this.$nextTick(() => {
            //   this.open = true
            // })
          })
      } else if (category === 'SHUNEWS') {
        this.open = false
        this.loading = false
        window.open(this.newsSingle.url)

        // this.$http
        //   .get('/shu/info/', {
        //     params: {
        //       category: this.newsSingle.url.slice(27, 31),
        //       msgID: this.newsSingle.url.slice(32, 37)
        //     }
        //   })
        //   .then(response => {
        //     this.newsSingle.detail = response.data.content
        //     this.loading = false
        //   })
        //   .catch(err => {
        //     this.loading = false
        //     console.log(err)
        //   })
      } else if (category === 'JWC') {
        this.$http
          .get('/mobile/campusmessage/GetJwcMessageById', {
            params: {
              MsgID: this.newsSingle.MsgID
            }
          })
          .then(response => {
            this.newsSingle.detail = response.data.Summary
            this.loading = false
          })
      } else if (category === 'JYB') {
        this.loading = false
      }
    },
    // getNews(done) {
    //   this.$http
    //     .get('/api/TongZGG/TongZGG/GetJiuYXW', {
    //       params: {
    //         infoTitle: '',
    //         infoType: '通知公告',
    //         pageSize: 20,
    //         pageNumber: this.page
    //       }
    //     })
    //     .then(response => {
    //       console.log(response)
    //       for (let item of response.data.data.xinw) {
    //         let news = {
    //           title: item.InfoTitle,
    //           detail: item.InfoContent
    //         }
    //         this.news_all.push(news)
    //         done()
    //       }
    //       this.count += 10
    //       this.page += 1
    //     })
    // },
    loadMoreXGB: function(index, done) {
      this.page = index
      this.$http
        .get('/mobile/campusmessage/getxgbmessagelist', {
          params: {
            limit: 10,
            currentPage: index
          }
        })
        .then(response => {
          console.log(response)
          if (response.data.messagelist.length === 0) {
            this.$refs.infiniteScrollXGB.stop()
          }
          for (let item of response.data.messagelist) {
            let news = {
              title: item.Title,
              detail: item.InfoContent,
              MsgID: item.MsgID
            }
            this.news.XGB.push(news)
            done()
          }
        })
    },
    loadMoreSHUNEWS: function(index, done) {
      this.page = index
      this.$http
        .get('/TongZGG/TongZGG/GetShuNews', {
          params: {
            pageSize: 10,
            pageNumber: index
          }
        })
        .then(response => {
          if (response.data.data.total === 0) {
            this.$refs.infiniteScrollXGB.stop()
          }
          for (let item of response.data.data.tongzgg) {
            let news = {
              title: item.Title,
              url: item.Link
            }
            this.news.SHUNEWS.push(news)
            done()
          }
        })
    },
    loadMoreJWC: function(index, done) {
      this.page = index
      this.$http
        .get('/mobile/campusmessage/getJwcmessagelist', {
          params: {
            limit: 10,
            currentPage: index
          }
        })
        .then(response => {
          console.log(response)
          if (response.data.messagelist.length === 0) {
            this.$refs.infiniteScrollJWC.stop()
          }
          for (let item of response.data.messagelist) {
            let news = {
              title: item.Title,
              detail: item.InfoContent,
              MsgID: item.MsgID
            }
            this.news.JWC.push(news)
            done()
          }
        })
    },
    loadMoreSHU: function(index, done) {
      this.page = index
      this.$http
        .get('/mobile/campusmessage/getcampusmessagelist', {
          params: {
            limit: 10,
            currentPage: index
          }
        })
        .then(response => {
          console.log(response)
          if (response.data.messagelist.length === 0) {
            this.$refs.infiniteScrollSHU.stop()
          }
          for (let item of response.data.messagelist) {
            let news = {
              title: item.Title,
              detail: item.InfoContent,
              MsgID: item.MsgID
            }
            this.news.SHU.push(news)
            done()
          }
        })
    },
    loadMoreJYB: function(index, done) {
      this.page = index
      this.$http
        .get('/TongZGG/TongZGG/GetJiuYXW', {
          params: {
            infoTitle: '',
            infoType: '通知公告',
            pageSize: 20,
            pageNumber: this.page
          }
        })
        .then(response => {
          console.log(response)
          if (response.data.data.xinw.length === 0) {
            this.$refs.infiniteScrollJYB.stop()
          }
          for (let item of response.data.data.xinw) {
            let news = {
              title: item.InfoTitle,
              detail: item.InfoContent
            }
            this.news.JYB.push(news)
            done()
          }
        })
    }
  }
}
</script>

<style>

</style>
