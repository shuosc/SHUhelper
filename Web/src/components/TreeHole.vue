 <template lang="pug">
  div
    div.sky(style="height:100vh;z-index: -200;" )
      div.stars
        .container(v-for="i in 100")
          .star
    div
      //- q-pull-to-refresh(:handler="refresher" style="z-index: 0;")
      q-card.no-margin.full-width(style="z-index: 2;")
        //- q-btn.full-width(flat color="white" @click="$router.push('/square')")
          q-icon(name="card_giftcard")
          | 回到广场
        q-card-main
          blockquote.no-margin.text-white(style='font-weight:400;font-size:0.8rem;')
            span(style="color:white;text-shadow:pink 0 1px 0;")
              | 把心里想的东西说出来没关系的
              br
            small
              span(style='color:red;') ♥
              span.text-white
              | SHUhelper
      q-infinite-scroll(:handler="loadMore" style="z-index: 2;"  ref="infiniteScroll")
        div.flex.row
          div.col-6(style="z-index: 1;")
            q-card.wish-card(v-for="(item, index) in feeds" v-if="index%2===0" :key="index")
              q-item()
                q-item-main.text-grey-3(style="text-shadow:grey 0 1px 0;")
                  q-item-tile {{item.displayName}}
                q-item-side(:stamp="'#'+(total-index)")
              q-card-separator
              q-card-main.text-blue-grey-1
                | {{item.text}}
              q-card-separator
              q-card-actions.text-pink
                q-btn.float-right(flat small @click="onLikeClick(index)")
                  q-icon(name="favorite")
                  span(style="color:white;font-size:1rem;")
                    | {{item.likecount}}
          div.col-6(style="z-index: 2;")
            q-card.wish-card( v-for="(item, index) in feeds" v-if="index%2===1" :key="index")
              q-item()
                q-item-main.text-grey-3(style="text-shadow:grey 0 1px 0;")
                  q-item-tile {{item.displayName}}
                q-item-side(:stamp="'#'+(total-index)")
              q-card-separator
              q-card-main.text-blue-grey-1
                | {{item.text}}
              q-card-separator
              q-card-actions.text-pink
                q-btn.float-right(flat small @click="onLikeClick(index)")
                  q-icon(name="favorite")
                  span(style="color:white;font-size:1rem;")
                    | {{item.likecount}}
        div.col-12.text-center(slot="message" style="z-index: 2;")
          q-spinner-dots( :size="40")
    q-modal(v-model="addMsgModal" minimized :content-css="{minWidth: '80vw'}")
      q-card-main
        q-field(:count="10" )
          mt-field(placeholder="你的名字" v-model="msg.name")
          //- q-input(stack-label="你的名字"  v-model="msg.name")
        q-field( :count="450")
          mt-field(placeholder="想说的话" type="textarea" rows="4" v-model="msg.content")
          //- q-input( stack-label="想说的话" type="textarea" :min-rows="5" v-model="msg.content")
        q-btn.full-width(@click="sendMsg")
          | 添加
    q-fixed-position(corner="bottom-right" :offset="[18, 18]" style="z-index: 2;")
      q-btn(round color="primary" @click="add" icon="add")
</template>

<script>

import { AppFullscreen } from 'quasar'
export default {
  data() {
    return {
      addMsgModal: false,
      page: 1,
      msg: {
        name: '匿名',
        content: ''
      },
      feeds: [],
      total: 0
    }
  },
  mounted() {
    AppFullscreen.request()
  },
  methods: {
    refresher(done) {
      this.feeds = []
      this.$refs.infiniteScroll.reset()
      this.$refs.infiniteScroll.resume()
      done()
    },
    add() {
      this.addMsgModal = true
    },
    onLikeClick(index) {
      let id = this.feeds[index].id
      this.$http.get(`/api/feeds/${id}/like`)
      this.feeds[index].likecount += 1
      this.feeds[index].liked = true
    },
    sendMsg() {
      var _this = this
      _this.publishLoading = true
      this.$http
        .post('/api/feeds/anonymous/', {
          namespace: 'treehole',
          name: this.msg.name,
          text: this.msg.content
        })
        .then(response => {
          this.text = ''
          this.$router.go(-1)
          this.feeds = []
          this.$refs.infiniteScroll.reset()
          this.$refs.infiniteScroll.resume()
          this.msg.content = ''
        })
        .catch(error => {
          _this.$store.commit('showSnackbar', { text: '登录失败' + error })
        })
    },
    loadMore(index, done) {
      this.loading = true
      var now = new Date()
      this.$http
        .get(`/api/feeds/anonymous/?page=${index}&namespace=treehole`)
        .then(response => {
          console.log('request complete', new Date() - now)
          // var cardID = this.$store.state.user.cardID
          this.total = response.data.total
          for (let i in response.data.feeds) {
            let feed = response.data.feeds[i]
            feed.likecount = feed.like.length
            this.feeds.push(feed)
          }
          if (response.data.feeds.length === 0) {
            this.$refs.infiniteScroll.stop()
          }
          done()
        })
        .catch(error => {
          done()
          this.$refs.infiniteScroll.stop()
          console.log(error)
        })
    }
  }
}
</script>

<style lang="stylus" scoped>
.new-year-text {
  color: antiquewhite;
  text-shadow: #6b92b9;
  font-weight: bold;
}
.wish-card {
  background-color: rgba(168, 168, 219, 0.3);
  word-break: break-all;
}
random(min, max)
  return floor(math(0, 'random')*(max - min + 1) + min)

.sky
  width 100vw
  height 100vh
  margin 0
  top 0
  overflow hidden
  position fixed
  background-image radial-gradient(center, ellipse cover, rgba(39,54,79,1) 0%,rgba(17,17,34,1) 50%,rgba(17,17,34,1) 100%)
  background -moz-radial-gradient(center, ellipse cover, rgba(39,54,79,1) 0%, rgba(17,17,34,1) 50%, rgba(17,17,34,1) 100%)
  background -webkit-gradient(radial, center center, 0px, center center, 100%, color-stop(0%,rgba(39,54,79,1)), color-stop(50%,rgba(17,17,34,1)), color-stop(100%,rgba(17,17,34,1)))
  background -webkit-radial-gradient(center, ellipse cover, rgba(39,54,79,1) 0%,rgba(17,17,34,1) 50%,rgba(17,17,34,1) 100%)
  background -o-radial-gradient(center, ellipse cover, rgba(39,54,79,1) 0%,rgba(17,17,34,1) 50%,rgba(17,17,34,1) 100%)
  background -ms-radial-gradient(center, ellipse cover, rgba(39,54,79,1) 0%,rgba(17,17,34,1) 50%,rgba(17,17,34,1) 100%)
  filter 'progid:DXImageTransform.Microsoft.gradient( startColorstr='#27364f', endColorstr='#111122',GradientType=1 )'
  background-position 50% 0%
  background-size 150vmax 150vmax
  background-repeat no-repeat
  background-color #112

.stars
  .container
    position absolute
    animation stars linear infinite
    .star
      animation twinkle linear infinite
      border-radius 100%
      transform translateZ(0)
  for n in (0..100)
    .container:nth-child({n})
      width random(1, 3px)
      height @width
      left (random(0, 200) / 2vw)
      animation-delay (random(1, 100) / 5s / @width - 1000s)
      animation-duration (random(200, 2000) / 5s / @width)
      .star
        width inherit
        height inherit
        animation-delay (random(1, 100) / 10s - 50s)
        animation-duration (random(50, 500) / 10s)
        background rgba(random(200, 255), random(150, 255), random(100, 255), (random(7, 10) / 10))



@keyframes stars
  0%
    transform translateY(110vh) translateZ(0)
  100%
    transform translateY(-10vh) translateZ(0)

@keyframes twinkle
  0%, 80%, 100%
    opacity .7
    box-shadow 0 0 0 white, 0 0 0 white
  95%
    opacity 1
    box-shadow 0 0 2px white, 0 0 4px white
</style>
