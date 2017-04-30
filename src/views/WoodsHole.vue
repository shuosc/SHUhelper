<template>
  <scroller lock-x
            scrollbar-y
            height="-96"
            ref="scroller"
            use-pullup
            @on-pullup-loading="getMessages()"
            use-pulldown
            @on-pulldown-loading="getLatestMessages()">
    <div>
      <div>
        <group gutter="0"
               title="账号">
          <x-textarea title="树洞"
                      v-model="content"
                      placeholder="把心里想的事情说出来没关系的:-)"></x-textarea>
          <x-button plain
                    @click.native="$vux.confirm.show({
                                    title:'确认提交？',
                              onCancel () {},
                              onConfirm () {submit()}
                            })"
                    type="primary">提交</x-button>
        </group>
        <divider>树洞</divider>
      </div>
      <div v-for="message in messages">
        <div id="message"
             @click="viewDetail(message.id)">
          <div id="content">
            <p v-for="paragraph in message.content.split('\n')">
              {{ paragraph }}</p>
          </div>
          <div id="footer">
            <div style="display:inline;text-align:left;">点赞 : {{ message.like }} 评论数 : {{ message.comments }}</div>
            <div style="display:inline;float:right;text-align:right;"> 发表于 : {{ message.time|formateDate }} </div>
          </div>
        </div>
      </div>
    </div>
  </scroller>
</template>

<script>
import { Group, Cell, Tabbar, TabbarItem, XHeader, Divider, Card, XNumber, Flexbox, FlexboxItem, XImg, Scroller, ViewBox, XButton, Popup, Radio, XInput, Checker, CheckerItem, Grid, GridItem, GroupTitle, Marquee, MarqueeItem, XTextarea, Box } from 'vux'

export default {
  components: {
    Grid,
    Box,
    Marquee,
    MarqueeItem,
    GroupTitle,
    GridItem,
    Group,
    Cell,
    Tabbar,
    TabbarItem,
    XHeader,
    Divider,
    Card,
    XNumber,
    FlexboxItem,
    Flexbox,
    XImg,
    Scroller,
    ViewBox,
    XButton,
    Popup,
    Radio,
    XInput,
    Checker,
    CheckerItem,
    XTextarea
  },
  data() {
    return {
      name: '',
      messages: [],
      content: '',
      activateShow: false,
      page: 1
    }
  },
  filters: {
    formateDate: function (value) {
      var date = new Date(value)
      date.setMinutes(date.getMinutes() + date.getTimezoneOffset())
      return (date.getMonth() + 1) + '/' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes()
    }
  },
  created: function () {
    this.getMessages()
  },
  // beforeRouteLeave (to, from, next) {
  //   if (from.name === 'woodshole' && to.name !== 'woodsholesingle') {
  //     console.log(to, from, next)
  //     this.messages = []
  //   }
  // },
  computed: {
  },
  methods: {
    viewDetail(id) {
      this.$router.push('/woods-hole/' + id)
    },
    resetScroller() {
      this.$nextTick(() => {
        this.$refs.scroller.reset({
        })
      })
    },
    getLatestMessages() {
      this.page = 1
      this.getMessages()
    },
    getMessages() {
      this.$http.get('/api/woods-hole', { params: { page: this.page } })
        .then((response) => {
          if (this.page !== 1) {
            this.messages = this.messages.concat(response.data)
          } else {
            this.messages = response.data
            this.$refs.scroller.donePulldown()
          }
          if (response.data.length === 0) {
            this.$vux.toast.show({
              position: 'bottom',
              type: 'text',
              text: '无更多数据'
            })
          } else {
            this.$vux.toast.show({
              position: 'bottom',
              type: 'text',
              text: '加载成功'
            })
            this.page++
          }
          this.resetScroller()
          this.$refs.scroller.donePullup()
        })
    },
    submit() {
      if (this.content === '') {
        return
      }
      this.$http.post('/api/woods-hole', {
        'title': this.name,
        'content': this.content
      }).then((response) => {
        if (response.data.success) {
          this.$vux.toast.show({
            position: 'bottom',
            type: 'text',
            text: '发送成功'
          })
          this.name = ''
          this.content = ''
          this.getMessages()
        }
      })
    }
  }
}
</script>

<style scoped>
#message {
  margin: 0px 10px 15px 10px;
  border: 1px solid #eee;
}

#content {
  color: #ffffff;
  text-align: center;
  padding: 30px 20px 30px 20px;
  background-color: rgba(80, 114, 139, 0.70);
  border-radius: 5px 5px 0px 0px;
  text-shadow: 0px 0px 0px #9e9e9e;
}

#footer {
  text-align: left;
  padding: 5px 10px 5px 10px;
  font-size: 0.8rem;
  color: #b6b6b6;
  border-radius: 0px 0px 5px 5px;
  background-color: rgba(250, 250, 250, 1);
}
</style>
