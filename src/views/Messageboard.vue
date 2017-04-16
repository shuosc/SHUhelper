<template>
  <scroller lock-x
            scrollbar-y
            height="-100"
            ref="scroller">
    <div>
      <group title="账号">
        <box gap="10px 10px">
          <x-input title="姓名"
                   placeholder=""
                   v-model="name"></x-input>
          <x-textarea title="留言"
                      v-model="content"
                      placeholder="可以在这里写下您的使用反馈，期望建议等等"></x-textarea>
        </box>
      </group>
      <x-button @click.native=" $vux.confirm.show({
                    title:'确认提交？',
              onCancel () {},
              onConfirm () {submit()}
            })"
                type="primary">提交</x-button>
      <divider>网站留言</divider>
      <div v-for="message in messages">
        <div style="color:#00868B;font-size:1.2rem;margin-right:10px;margin-left:10px;border-bottom:1px solid #eee;">{{message.name}}:</div>
        <div style="padding:10px;margin-right:10px;margin-left:10px;border-bottom:1px solid #eee;">{{message.content}}</div>
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
      this.$http.get('/api/messageboard')
        .then((response) => {
          this.messages = response.data
          this.resetScroller()
        })
    },
    submit() {
      if (this.name === '' || this.content === '') {
        return
      }
      this.$http.post('/api/messageboard', {
        'name': this.name,
        'content': this.content
      }).then((response) => {
        if (response.data.success) {
          this.$vux.toast.show({
            position: 'bottom',
            type: 'text',
            text: '发送成功'
          })
          this.getMessages()
        }
      })
    }
  }
}
</script>

<style>

</style>
