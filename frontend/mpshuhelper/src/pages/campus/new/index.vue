<template lang="pug">
  div(class="container" @click="clickHandle('test click', $event)")
    div.row.justify-center.act-card-wrapper
      div.fab(@click="onAddClick")
        div.iconfont.icon-add
      div.col-10.card.act-card(v-for="(card, cardIdx) in actCards" :key="cardIdx")
        div.row.flex-row
          div.col-2
            img.avatar(:src="card.user.avatar")
          div.col-10.flex-column.justify-between
            div.act-card-username {{ card.user.username }}
            div.act-card-time {{ card.creatTime }}
        div.row.flex-row
          div.col-10.offset-2
            div.act-card-content {{ card.content }}
            div.row.flex-row.wrap.act-img-group
              img.col-4.act-img(v-for="(img, imgIdx) in actImgs" :key="imgIdx" :src="img.src")
        div.card-comment(v-if="card.comments.length")
          div.card-comment-wrapper.flex-column
            div(v-for="(comment, cmtIdx) in card.comments" :key="cmtIdx")
              span.card-comment-username {{ comment.user.username }}：
              span.card-comment-content {{ comment.content }}
        div.row.card-option-wrapper
          div.col-2
            span.iconfont.icon-like.card-option(@click="like(cardIdx)")
            span.card-option-count {{ card.likes }}
          div.col-2
            span.iconfont.icon-comment.card-option
            span.card-option-count {{ card.comments.length }}
    
    
</template>

<script>
import Fly from 'flyio/dist/npm/wx'
export default {
  data() {
    return {
      actCards: [
        {
          user: {
            username: 'YS199971',
            avatar: '/static/avatar_default.jpg'
          },
          creatTime: '10小时前',
          content: '大一什么时候开始军训？',
          views: 45,
          likes: 0,
          comments: [
            {
              user: {
                username: 'TamakiAko'
              },
              content: '7月11还是10号的样子'
            }
          ]
        },
        {
          user: {
            username: 'zts201709',
            avatar: '/static/avatar_default.jpg'
          },
          creatTime: '2天前',
          content: '夏季行政课的绩点给的高吗？',
          views: 188,
          likes: 1,
          comments: []
        },
        {
          user: {
            username: 'YS199971',
            avatar: '/static/avatar_default.jpg'
          },
          creatTime: '6天前',
          content: '什么时候放暑假呀？',
          views: 324,
          likes: 2,
          comments: []
        },
        {
          user: {
            username: 'xuehuai',
            avatar: '/static/avatar_default.jpg'
          },
          creatTime: '6天前',
          content: '有去学汉语言文学的同学吗？',
          views: 248,
          likes: 0,
          comments: [
            {
              user: {
                username: 'xuehuai'
              },
              content: '！！！！！急'
            },
            {
              user: {
                username: 'Joning'
              },
              content: '嘎？'
            }
          ]
        },
        {
          user: {
            username: 'wswphnh123',
            avatar: '/static/avatar_default.jpg'
          },
          creatTime: '14天前',
          content: '计算机专业大二秋季学期专业必修课要学哪些书？',
          views: 45,
          likes: 0,
          comments: []
        },
        {
          user: {
            username: 'xuehai',
            avatar: '/static/avatar_default.jpg'
          },
          creatTime: '25天前',
          content: '学校的游泳馆一次多久呀',
          views: 45,
          likes: 0,
          comments: [
            {
              user: {
                username: 'moonin1q'
              },
              content: '校内人员15/h'
            },
            {
              user: {
                username: 'AlfredLin'
              },
              content: '15/90min'
            }
          ]
        }
      ]
    }
  },
  computed: {},
  methods: {
    reAuth() {
      wx.login({
        success: res => {
          this.$http
            .get(`/auth/mp/app?code=${res.code}&source=shuhelper_mp_app`)
            .then(response => {
              console.log(response)
              wx.redirectTo({
                url: '/pages/login/main'
              })
              // this.redirectToLogin(response.authID)
            })
            .catch(err => {
              console.log(err)
              this.redirectToLogin(err.response.authID)
            })
        }
      })
    },
    bindViewTap() {
      const url = '../logs/main'
      wx.navigateTo({ url })
    },
    clickHandle(msg, ev) {
      console.log('clickHandle:', msg, ev)
    },
    getActs(index) {
      let fly = new Fly()
      fly.get(`/api/feeds/?page=${index}`, {}, {
        baseURL: 'https://www.shuhelper.cn/'
      })
        .then(res => {
          let feeds = res.data.feeds
          for (let i in feeds) {
            let feed = feeds[i]
            feed.likecount = feed.like.length
            this.$store.commit('addFeed', feed)
            // this.feeds.push(feed)
          }
          console.log('loaded')
        })
        .catch(error => {
          console.log(error)
        })
    },
    like(index) {
      if (this.actCards[index].isLike) {
        this.actCards[index].likes--
        this.actCards[index].isLike = false
      } else {
        this.actCards[index].likes++
        this.actCards[index].isLike = true
      }
    }
  },
  onPullDownRefresh() {
    console.log('pull down')
  },
  created() {
    console.log(this.user)
    this.getActs(this.index++)
  }
}
</script>

<style scoped>

.act-card-wrapper {
  padding: 10px 0 0 0;
}

.card {
  background-color: white;
  padding: 11px 16px 11px 16px;
  box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
  border-radius: 8px;
  margin: 0 0 10px 0;
}

.card .hr {
  border: #aaa 1px solid;
}

.card-comment {
  margin-top: 10px;
  background: rgb(245, 245, 245);
  padding: 11px 16px 11px 16px;
  border-radius: 4px;
}

.avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
}

.act-card-username {
  font-size: 14px;
}

.act-card-time {
  font-size: 12px;
  color: #aaa;
}

.act-card-content {
  font-size: 14px;
}

.card-comment-username {
  color: rebeccapurple;
  font-size: 14px;
}

.card-comment-content {
  font-size: 14px;
}

.card-option-wrapper {
  margin-top: 5px;
}

.card-option {
  font-size: 16px;
}

.card-option-count {
  font-size: 16px;
  margin-left: 5px;
}

.fab {
  border-radius: 50%;
  height: 5rem;
  width: 5rem;
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background-color: #7eb3ec;
  color: white;
  z-index: 1000;
  box-shadow: 0 5px 5px #ccd8e2;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
