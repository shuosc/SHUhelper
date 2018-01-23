 <template lang="pug">
  div.window-height
    div.love-board(style="height:100vh;z-index: -200;" )
      .container
        .heart.anim1 &hearts;
      .container
        .heart.anim2 &hearts;
      .container
        .heart.anim3 &hearts;
      .container
        .heart.anim4 &hearts;
    div
      //- q-pull-to-refresh(:handler="refresher" style="z-index: 0;")
      q-card.no-margin.full-width(style="z-index: 2;")
        q-btn.full-width(flat color="white" @click="$router.push('/square')")
          q-icon(name="card_giftcard")
          | 回到广场
        q-card-main
          blockquote.no-margin.text-white(style='font-weight:400;font-size:0.8rem;')
            span(style="color:white;text-shadow:pink 0 1px 0;")
              | 倾诉你的心意
              br
            small
              span(style='color:red;') ♥ 
      q-infinite-scroll(:handler="loadMore" style="z-index: 2;"  ref="infiniteScroll")
        div.flex.row
          div.col-6(style="z-index: 1;")
            q-card.wish-card(v-for="(item, index) in feeds" v-if="index%2===0" :key="index")
              q-item()
                q-item-main.text-grey-3()
                  q-item-tile {{item.displayName}}
                q-item-side(:stamp="'#'+(total-index)")
              q-card-separator 
              q-card-main.text-red(style="font-size:1.1rem;")
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
                q-item-main.text-grey-3
                  q-item-tile {{item.displayName}}
                q-item-side(:stamp="'#'+(total-index)")
              q-card-separator 
              q-card-main.text-red(style="font-size:1.1rem;")
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
          namespace: 'loveboard',
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
          _this.$store.commit('showSnackbar', { text: '登陆失败' + error })
        })
    },
    loadMore(index, done) {
      this.loading = true
      var now = new Date()
      this.$http
        .get(`/api/feeds/anonymous/?page=${index}&namespace=loveboard`)
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

<style scoped>
.new-year-text {
  color: antiquewhite;
  text-shadow: #6b92b9;
  font-weight: bold;
}
.wish-card {
  background-color: rgba(219, 168, 216, 0.3);
  word-break: break-all;
}

.love-board {
  width:100vw;
  height:100vh;
  position: fixed;
  background-color: pink;
}
.center {
  width: 230px;
  margin: 0 auto;
}
.container{
  /* margin-top: 20px;
  width: 50px;
  height: 170px; */
  height:50%;
  width:50%;
  text-align: center;
  position: relative;
  display: inline-block;
}

.valentines {
  font-family: Podkova, san-serif;
  color: oldlace;
  font-weight: 300;
  font-size:32px;
  margin-top: 10px;
  border-bottom: 1px dotted oldlace;
  
}
.heart {
  color:oldlace;
  font-size: 25px;
  position: absolute;
  bottom: 0;
  right: 50px;
  animation-name: movement;
  animation-duration: 2s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.anim1 {
  animation-delay: 1s;
}
.anim2 {
  animation-delay: 1.5s;
}
.anim3 {
  animation-delay: 0.5s;
}
.anim4 {
  animation-delay: 1.9s;
}

@keyframes movement {
  0%{
   
    bottom: 0;
    right: 50px;
  }
  20%{
    color: hotpink;
    right: 40px;
  }
  40%{
    right: 60px;
  }
  
  50%{ 
    right: 50px;
  }
  60%{
    right: 40px;
  }
  70%{
    right: 50px;
  }
  80%{
    right: 45px;
  }
  90%{
    right: 50px;
  }
  100%{
    bottom: 150px;
    -webkit-opacity: 0;
    -moz-opacity: 0;
    opacity: 0;
  }
}
</style>
