<template lang="pug">
  div
    //- q-pull-to-refresh(:handler='refresher')
    //- pull-to(:top-load-method="refresher")
    q-infinite-scroll(:handler="loadMore" ref="infiniteScroll")
      q-card.quote-card
        blockquote.no-margin
          //- p 欢迎来到广场，在这里您可以畅所欲言
          small
            | 欢迎来到广场，在这里您可以畅所欲言
      q-scroll-area.text-center(style="width: 100%; height: 5rem;white-space:nowrap;overflow:scroll;")
        q-card.news(inline style="height:4rem;min-width:20vw;width:6.5rem;" @click="$router.push('/news')")
          div.row.flex.full-height
            div.col-5.self-center
              q-icon(name="public" size="2.5rem" color="white")
            div.col-5.self-center.text-white(style="font-size:1rem;")
              | 新闻
        //- q-card.news(inline style="height:4rem;min-width:20vw;width:6.5rem;" @click="$router.push('/news')")
          div.row.flex.full-height
            div.col-5.self-center
              q-icon(name="public" size="2.5rem" color="white")
            div.col-5.self-center.text-white(style="font-size:1rem;")
              | 活动
        q-card.tree-hole.text-center(inline style="height:4rem;min-width:20vw;width:6.5rem;"  @click="$router.push('/tree-hole')")
          div.row.flex.full-height
            div.col-5.self-center
              q-icon(name="fa-shu" size="2.5rem" color="white")
            div.col-5.self-center.text-white(style="font-size:1rem;")
              | 树洞
        q-card.love.text-center(inline style="height:4rem;min-width:20vw;width:6.5rem;" @click="$router.push('/love-board')")
          div.row.flex.full-height
            div.col-5.self-center
              q-icon(name="favorite" size="2.5rem" color="white")
            div.col-5.self-center.text-white(style="font-size:1rem;")
              | 表白墙 
      feed-card(v-for="(feed,index) in feeds" :key="feed.id" :comments="true" v-if="!feed.deleted" @delete="onFeedDelete(index)" :index="index" :feed="feed" @like="onLikeClick(index)" v-scroll-fire="onFeedFire(feed.id)" )
      div.text-center(slot="message")
        q-spinner-dots( :size="40")
    q-modal(ref="modal" maximized)
      q-modal-layout
        q-toolbar(slot="header" color="primary")
          q-btn(color="white" flat @click="$refs.modal.close()")
            q-icon(name="close")
          q-toolbar-title
              | 发布动态
          q-btn(flat @click="publish") 发布
        q-card(flat)
          q-card-main
            q-field(helper="分享你的见闻")
              mt-field(placeholder="想说的话" type="textarea" rows="4" v-model="text")
            //- text-area(v-model.lazy="text")
            //- q-input( stack-label="想说的话" type="textarea" :min-rows="5" v-model.lazy="text")
        q-card(flat)
          q-card-main
            div.row.flex.xs-gutter
              div.col-4.text-center(v-for="(img,key) in uploadImgs" style="height:20vh;background-color:#eee;" :key="key")
                img(:src="`//static.shuhelper.cn/${img.url}-slim75`" style="object-fit: cover;height:100%;width:100%;" v-if="img.status==='success'")
                q-spinner(v-else-if="img.status==='pending'" style="height:100%" color="secondary" :size="50")
                q-btn(v-else round block big) X
              div.col-4.flex( style="height:20vh;")
                q-btn.text-center( big flat style="background-color:#eee;height:100%;width:100%;" @click="$refs.imgform.userfile.click()") 添加图片
        form(id="imgform" ref="imgform" method="post" style="display:none;" enctype="multipart/form-data")
          input(name="key" id="key" type="hidden" :value="key")
          input(name="token" type="hidden" :value="token")
          input(id="userfile" name="file" type="file" accept="image/*" @change="upload")
          input(id="takephoto" name="file" accept="image/*" type="file")
          input(id="takevideo" name="file" type="file" accept="video/*")
          input(name="accept" type="hidden")
    q-fixed-position(corner="bottom-right" :offset="[18, 18]" style="z-index: 2;")
      q-btn(round color="primary" @click="$refs.modal.open()" icon="add")
</template>

<script>
import { Toast, QScrollArea, ScrollFire } from 'quasar'
import FeedCard from '@/SquareFeedCard'
// import PullTo from 'vue-pull-to'
import { mapGetters } from 'vuex'
export default {
  components: {
    QScrollArea,
    FeedCard
    // PullTo
  },
  directives: {
    ScrollFire
  },
  activated() {
    this.active = true
    this.$q.events.$on('app:refresh:square', this.refresher)
  },
  created() {
    this.refresher(() => {})
  },
  deactivated: function() {
    this.active = false
    this.$q.events.$off('app:refresh:square', this.refresher)
  },
  beforeRouteUpdate(to, from, next) {
    if (to.name === 'Square' && from.name !== 'feedDetail') {
      this.resetFeeds()
    }
    next()
  },
  computed: {
    ...mapGetters(['feeds']),
    imgs: function() {
      let img = []
      for (let i in this.uploadImgs) {
        if (this.uploadImgs[i].status === 'success') {
          img.push(this.uploadImgs[i].url)
        }
      }
      return img
    },
    feed: function() {
      if (this.currentIndex === -1) {
        return {
          img: [],
          text: '',
          user: {
            avatar: 'avatar_default.jpg',
            name: ''
          },
          comments: [],
          like: [],
          created: '2018-01-07 12:58:59.359000',
          index: 0
        }
      } else {
        return this.feeds[this.currentIndex]
      }
    }
  },
  data() {
    return {
      comment: '',
      // feeds: [],
      uploadImgs: [],
      text: '',
      token: '',
      key: '',
      img: '',
      imgLoading: false,
      currentIndex: -1,
      active: false
    }
  },
  methods: {
    onFeedFire(id) {
      return element => {
        if (this.active) {
          this.$http.post(`/api/feeds/${id}/hits`)
        }
      }
    },
    onLikeClick(index) {
      let id = this.feeds[index].id
      this.$http.get(`/api/feeds/${id}/like`)
      if (this.feeds[index].liked) {
        this.$store.commit('cancelFeedLike', index)
      } else {
        this.$store.commit('clickFeedLike', index)
      }
    },
    getFeed(feedID) {
      this.$http.get(`/api/feeds/${this.feed.id}`).then(response => {
        let feed = response.data
        this.$set(this.feeds, this.currentIndex, feed)
        this.feeds[this.currentIndex].likecount = feed.like.length
      })
    },
    onCommentClick(index) {
      this.currentIndex = index
      // this.$refs.commentModal.open()
    },
    refresher(done) {
      document.documentElement.scrollTop = 0
      document.body.scrollTop = 0
      this.currentIndex = -1
      this.$store.commit('clearFeeds')
      this.$refs.infiniteScroll.reset()
      this.$refs.infiniteScroll.resume()
      if (done !== undefined) {
        done()
      }
    },
    onFeedClick(index) {
      // this.currentIndex = index
      // this.$refs.feedModal.open()
      this.$router.push(`/feeds/${this.feeds[index].id}?index=${index}`)
      console.log('on feed click' + this.feeds[index].id)
    },
    onFeedDelete(index) {
      this.$store.commit('deleteFeed', index)
    },
    publish() {
      if (this.text === '' && this.imgs.length === 0) {
        Toast.create('内容不能为空')
        return
      }
      this.$http
        .post('/api/feeds/', {
          type: 'text',
          text: this.text,
          img: this.imgs
        })
        .then(response => {
          this.text = ''
          this.$refs.modal.close()
          Toast.create('发表成功')
          this.refresher(() => {})
        })
        .catch(error => {
          Toast.create('发布失败' + error)
        })
    },
    loadMore(index, done) {
      this.$http
        .get(`/api/feeds/?page=${index}`)
        .then(response => {
          let feeds = response.data.feeds
          for (let i in feeds) {
            let feed = feeds[i]
            feed.likecount = feed.like.length
            this.$store.commit('addFeed', feed)
            // this.feeds.push(feed)
          }
          // console.log('loaded')
          done()
        })
        .catch(error => {
          console.log(error)
          this.$refs.infiniteScroll.stop()
          done()
        })
    },
    transformKey(key) {
      key = btoa(key)
      key.replace('+', '-')
      key.replace('/', '_')
      key.replace('=', '')
      return key
    },
    uploadImg(file, base64) {
      this.$http.get(`/api/upload/token?key=${this.key}`).then(response => {
        this.token = response.data.uptoken
        this.$nextTick(() => {
          let index = base64.indexOf(',') + 1
          this.key = this.transformKey(this.key)
          this.$http
            .post(`/upload/putb64/-1/key/${this.key}`, base64.slice(index), {
              headers: {
                Authorization: 'UpToken ' + this.token,
                'Content-Type': 'application/octet-stream'
              }
            })
            .then(response => {
              console.log(response)
              for (let i in this.uploadImgs) {
                console.log(this.uploadImgs[i].url, response.data.key)
                if (this.uploadImgs[i].url === response.data.key) {
                  this.uploadImgs[i].status = 'success'
                }
              }
            })
            .catch(error => {
              console.log(error)
              for (let i in this.uploadImgs) {
                if (this.uploadImgs[i].url === this.key) {
                  this.uploadImgs[i].status = 'failed'
                }
              }
            })
        })
      })
    },
    upload(e) {
      // console.log(e.target)
      /* eslint-disable no-new */
      /* eslint-disable new-cap */
      /* eslint-disable no-undef */
      // console.log(html5ImgCompress)
      new html5ImgCompress(e.target.files[0], {
        before: function(file) {
          console.log('压缩前...')
          // 这里一般是对file进行filter，例如用file.type.indexOf('image') > -1来检验是否是图片
          // 如果为非图片，则return false放弃压缩（不执行后续done、fail、complete），并相应提示
        },
        done: (file, base64) => {
          console.log('压缩成功...')
          this.uploadImg(file, base64)
          // ajax和服务器通信上传base64图片等操作
        },
        fail: function(file) {
          console.log('压缩失败...')
        },
        complete: function(file) {
          console.log('压缩完成...')
        },
        notSupport: function(file) {
          console.log('浏览器不支持！')
          // 不支持操作，例如PC在这里可以采用swfupload上传
        }
      })
      var userfile = e.target.files[0]
      var selectedFile = userfile.name
      if (selectedFile) {
        var ramdomName =
          Math.random()
            .toString(36)
            .substr(2) + userfile.name.match(/\.?[^./]+$/)
        this.key = 'feed_' + this.$store.state.user.cardID + '_' + ramdomName
        this.uploadImgs.push({
          name: selectedFile,
          status: 'pending',
          url: this.key
        })
      } else {
        return false
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.news
  background #4e54c8 /* fallback for old browsers */
  background -webkit-linear-gradient(to right, #8f94fb, #4e54c8) /* Chrome 10-25, Safari 5.1-6 */
  background linear-gradient(to right, #8f94fb, #4e54c8) /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

.tree-hole
  background #9D50BB /* fallback for old browsers */
  background -webkit-linear-gradient(to right, #6E48AA, #9D50BB) /* Chrome 10-25, Safari 5.1-6 */
  background linear-gradient(to right, #6E48AA, #9D50BB) /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

.love
  // background: #FF5F6D;  /* fallback for old browsers */
  // background: -webkit-linear-gradient(to right, #FFC371, #FF5F6D);  /* Chrome 10-25, Safari 5.1-6 */
  // background: linear-gradient(to right, #FFC371, #FF5F6D); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
  background #E44D26 /* fallback for old browsers */
  background -webkit-linear-gradient(to right, #F16529, #E44D26) /* Chrome 10-25, Safari 5.1-6 */
  background linear-gradient(to right, #F16529, #E44D26) /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

@media screen and (max-height: 750px)
  .schedule-container
    height 750px

@media screen and (min-height: 750px)
  .schedule-container
    height 100vh

img
  margin-left auto
  margin-right auto
  display block
</style>
