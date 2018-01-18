<template lang="pug">
  div(style="min-height: calc(100vh - 105px)")
    q-pull-to-refresh(:handler='refresher')
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
        q-card(v-for="(feed,index) in feeds" :key="feed.id" style="margin:0.8rem 0 0 0 ;" @click="onFeedClick(index)")
          q-card-title.no-padding 
          q-item(dense)
            q-item-side
              q-item-tile(avatar)
                img(:src="`https://static.shuhelper.cn/${feed.user.avatar}`")
            q-item-main
              q-item-tile(label) {{feed.user.name}}
              q-item-tile(sublabel)  {{[feed.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
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
          q-card-actions
            div.full-width
              q-btn.pull-right(flat small)
                q-icon(name="comment")
                span(style="color:grey;font-size:1rem;")
                  | {{feed.comments.length}}
              q-btn.pull-right(small :class="{'text-pink':feed.liked}" flat @click.stop="onLikeClick(index)")
                q-icon(name="favorite")
                span(style="color:grey;font-size:1rem;")
                  | {{feed.likecount}}
          q-card(flat)
            q-list(dense)
              q-item.no-padding(v-for="(comment,index) in feed.comments" :key="index")
                q-item-main
                  small
                    span.text-primary
                      | {{comment.user.name}}: 
                    | {{ comment.text }}
        div.text-center(slot="message")
          q-spinner-dots( :size="40")
    q-modal(ref="feedModal" maximized)
      q-modal-layout
        q-toolbar(slot="header" color="primary")
          q-btn(color="white" flat @click="$refs.feedModal.close()")
            q-icon(name="close")
          q-toolbar-title
              | 详情
        q-card(flat style="margin:1rem 0 0 0")
          q-card-title.no-padding 
          q-item(dense)
            q-item-side
              q-item-tile(avatar)
                img(:src="`https://static.shuhelper.cn/${feed.user.avatar}`")
            q-item-main
              q-item-tile(label) {{feed.user.name}}
              q-item-tile(sublabel)  {{[feed.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
          q-card-separator
          q-card-main 
            p(v-for="paragraph in feed.text.split('\\n')")
              | {{ paragraph }}
          div.row.flex.xs-gutter(v-if="feed.img.length !== 0" style="padding:0.5rem;")
            div.col-4(v-for="(img,index) in feed.img" :key="index" @click.stop="")
              img(:src="`${img}-slim75`" @click="showImg(img)"
              style="object-fit: cover;width:100%;height:100%;" 
              alt="lorem")
          q-card-separator
          q-card-actions
            div.full-width
              q-btn.pull-right(flat)
                q-icon(name="comment")
                span(style="color:grey;font-size:1rem;")
                  | {{feed.comments.length}}
              q-btn.pull-right( :class="{'text-pink':feed.liked}" flat @click.stop="onLikeClick(currentIndex)")
                q-icon(name="favorite")
                span(style="color:grey;font-size:1rem;")
                  | {{feed.likecount}}
        q-list
          q-list-header(v-if="feed.comments.length > 0") 共有{{feed.comments.length}}条评论
          q-item-separator
          q-card(flat v-for="(comment,index) in feed.comments" :key="index" style="margin:1rem 0 0 0")
            q-card-title.no-padding 
            q-item(dense)
              q-item-side
                q-item-tile(avatar)
                  img(:src="`https://static.shuhelper.cn/${comment.user.avatar}`")
              q-item-main
                q-item-tile(label) {{comment.user.name}}
                q-item-tile(sublabel)  {{[comment.created.slice(0,19),'YYYY-MM-DD HH:mm:ss']|moment("from")}}
              q-item-side(:stamp="`\#${index+1}`")
            q-card-separator
            q-card-main 
              | {{comment.text}}
          q-list-header 没有更多评论
        q-toolbar(slot="footer" color="white")
          q-toolbar-title
            mt-field(placeholder="请输入评论" v-model="comment")
          q-btn(flat color="primary" @click="publishComment(feed.id)")
            q-icon(name="send")
    q-modal.flex(ref="imgModal" minimized @click.native="$refs.imgModal.close()")
      q-card.no-margin(flat v-if="imgLoading" style="min-height:100px;min-width:100px;")
        q-inner-loading(:visible="imgLoading")
          q-spinner-gears(size="50px" color="primary")
      img.responsive(:src="img" v-show="!imgLoading" @load="imgLoad")
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
import { Toast, QScrollArea, QInnerLoading, QSpinnerGears } from 'quasar'
export default {
  components: {
    QScrollArea,
    QInnerLoading,
    QSpinnerGears
  },
  created() {
    // this.resetFeeds()
    // this.getFeeds()
  },
  beforeRouteUpdate(to, from, next) {
    if (to.name === 'Square' && from.name !== 'feedDetail') {
      this.resetFeeds()
    }
    next()
  },
  computed: {
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
            avatar: '',
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
      feeds: [],
      uploadImgs: [],
      text: '',
      token: '',
      key: '',
      img: '',
      imgLoading: false,
      currentIndex: -1
    }
  },
  methods: {
    imgLoad() {
      console.log('img loaded')
      this.imgLoading = false
    },
    showImg(img) {
      this.img = img
      this.imgLoading = true
      this.$refs.imgModal.open()
    },
    onLikeClick(index) {
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
    publishComment(feedID) {
      if (this.comment === '') return
      this.$http
        .put(`/api/feeds/${this.feed.id}`, {
          text: this.comment
        })
        .then(response => {
          this.comment = ''
          this.getFeed(feedID)
        })
    },
    getFeed(feedID) {
      this.$http.get(`/api/feeds/${this.feed.id}`).then(response => {
        let feed = response.data
        this.$set(this.feeds, this.currentIndex, feed)
        this.feeds[this.currentIndex].likecount = feed.like.length
        this.feeds[this.currentIndex].img = feed.img.map(x => {
          return 'https://static.shuhelper.cn/' + x
        })
      })
    },
    onCommentClick(index) {
      this.currentIndex = index
      // this.$refs.commentModal.open()
    },
    refresher(done) {
      this.currentIndex = -1
      this.feeds = []
      this.$refs.infiniteScroll.reset()
      this.$refs.infiniteScroll.resume()
      done()
    },
    onFeedClick(index) {
      this.currentIndex = index
      this.$refs.feedModal.open()
      // this.$router.push(`/feed-detail/${this.feed.id}`)
    },
    onFeedDelete(index) {
      this.feeds.splice(index, 1)
    },
    publish() {
      if (this.text === '') {
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
            feed.img = feed.img.map(x => {
              return 'https://static.shuhelper.cn/' + x
            })
            this.feeds.push(feed)
          }
          console.log('loaded')
          done()
        })
        .catch(error => {
          console.log(error)
          this.$refs.infiniteScroll.stop()
          done()
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
          this.$http.get(`/api/upload/token?key=${this.key}`).then(response => {
            this.token = response.data.uptoken
            this.$nextTick(() => {
              // var f = new FormData(this.$refs.testform)
              // f
              let index = base64.indexOf(',') + 1
              this.key = btoa(this.key)
              this.key.replace('+', '-')
              this.key.replace('/', '_')
              this.key.replace('=', '')
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
