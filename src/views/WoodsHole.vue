<template>
  <scroller lock-x
            scrollbar-y
            height="-96"
            ref="scroller">
    <div>
      <div>
        <group gutter="0"
               title="账号">
          <x-textarea title="树洞"
                      v-model="content"
                      placeholder="把心里想的事情说出来没关系的:-)"></x-textarea>
          <x-button plain  @click.native=" $vux.confirm.show({
                              title:'确认提交？',
                        onCancel () {},
                        onConfirm () {submit()}
                      })"
                    type="primary">提交</x-button>
        </group>
        <divider>树洞</divider>
      </div>
      <div v-for="message in messages">
        <div style="background-color:#5f5f5f;color:#ffffff;padding:20px;margin-bottom:15px;margin:10px;border:1px solid #eee;text-align:center;border-radius:15px;text-shadow:0px 0px 0px #9e9e9e;">
        <p v-for="paragraph in message.content.split('\n')">
        {{ paragraph }}</p></div>
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
      activateShow: false
    }
  },
  created: function () {
    this.getMessages()
  },
  computed: {
  },
  methods: {
    resetScroller() {
      this.$nextTick(() => {
        this.$refs.scroller.reset({
        })
      })
    },
    getMessages() {
      this.$http.get('/api/woods-hole')
        .then((response) => {
          this.messages = response.data
          this.resetScroller()
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
</style>
