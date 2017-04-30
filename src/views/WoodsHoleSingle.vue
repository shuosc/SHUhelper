<template>
  <div>
    <divider> 详情 </divider>
    <div id="message">
      <div id="content">
        <p v-for="paragraph in message.content.split('\n')">
          {{ paragraph }}</p>
      </div>
      <div id="footer">
        <div>
          <div style="display:inline;text-align:left;">点赞 : {{ message.like }} 评论数 : {{ message.comments.length }}</div>
          <div style="display:inline;float:right;text-align:right;"> 发表于 : {{ message.time|formateDate }} </div>
        </div>
        <div @click="like()"
             style="color:orange;text-align:right;font-size:1rem;margin-right:10px;"><i class="iconfont"
             :class="{ 
               'icon-heart-o': !isLiked, 'icon-heart': isLiked }"> </i></div>
      </div>
    </div>
    <div v-for="comment in message.comments">
      <div style="color:#00868B;font-size:1.2rem;margin-right:10px;margin-left:10px;border-bottom:1px solid #eee;">{{comment.name==''?'匿名用户':comment.name}}:</div>
      <div style="padding:10px;margin-right:10px;margin-left:10px;border-bottom:1px solid #eee;">{{comment.content}}</div>
    </div>
    <group gutter="0"
           title="评论">
      <x-input title="昵称"
               placeholder=""
               v-model="name"></x-input>
      <x-textarea title="评论"
                  v-model="content"
                  placeholder=""></x-textarea>
      <x-button @click.native=" $vux.confirm.show({
                                    title:'确认提交？',
                              onCancel () {},
                              onConfirm () {submit()}
                            })"
                type="primary">提交</x-button>
    </group>
  </div>
</template>

<script>
import { Group, Divider, Scroller, XTextarea, XButton, XInput } from 'vux'

export default {
  components: {
    Group,
    Divider,
    Scroller,
    XTextarea,
    XButton,
    XInput
  },
  data() {
    return {
      name: '',
      message: {},
      content: '',
      activateShow: false,
      isLiked: false
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
    this.getMessage()
  },
  computed: {
  },
  methods: {
    getMessage() {
      console.log(this.$route.params.id)
      this.$http.get('/api/woods-hole/' + this.$route.params.id)
        .then((response) => {
          this.message = response.data
        })
    },
    like() {
      this.isLiked = true
      this.$http.get('/api/woods-hole/' + this.$route.params.id + '/like')
        .then((response) => {
          if (response.data.success) {
            this.$vux.toast.show({
              position: 'bottom',
              type: 'text',
              text: '点赞成功'
            })
            this.getMessage()
          }
        })
    },
    submit() {
      if (this.name === '' && this.content === '') {
        return
      }
      this.$http.post('/api/woods-hole/' + this.$route.params.id, {
        'name': this.name,
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
          this.getMessage()
        }
      })
    }
  }
}
</script>

<style scoped>
#message {
  margin: 10px 10px 15px 10px;
  border: 1px solid #eee;
}

#content {
  color: #ffffff;
  text-align: center;
  padding: 40px 20px 40px 20px;
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
