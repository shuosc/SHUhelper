<template>
  <scroller lock-x
            scrollbar-y
            height="-96"
            ref="scroller">
    <div>
      <div>
        <group gutter="0"
               title="账号">
          <x-input title="姓名"
                   placeholder=""
                   v-model="name"></x-input>
          <x-textarea title="留言"
                      v-model="content"
                      placeholder="可以在这里写下您的使用反馈，期望建议等等"></x-textarea>
          <x-button @click.native=" $vux.confirm.show({
                              title:'确认提交？',
                        onCancel () {},
                        onConfirm () {submit()}
                      })"
                    type="primary">提交</x-button>
        </group>
        <divider>网站留言</divider>
      </div>
      <div v-for="message in messages">
        <div style="color:#00868B;font-size:1.2rem;margin-right:10px;margin-left:10px;border-bottom:1px solid #eee;">{{message.name}}:</div>
        <div style="padding:10px;margin-right:10px;margin-left:10px;border-bottom:1px solid #eee;">{{message.content}}</div>
      </div>
    </div>
  </scroller>
</template>

<script>
import { Group, Divider, Scroller, XButton, XInput, XTextarea } from 'vux'

export default {
  components: {
    Group,
    Divider,
    Scroller,
    XButton,
    XInput,
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
