<template lang="pug">
  div(class="container" @click="clickHandle('test click', $event)")
    //- img(@click="onAvatarClick",style="height:1.5rem;width:1.5rem;margin:auto;display:block;" class="userinfo-avatar" v-if="user.avatarURL" :src="user.avatarURL" background-size="cover")
    div.form(style="padding:10px;display:flex;flex-direction:column;")
      div
        input.title-form(placeholder="请输入标题" v-model="form.title")
      div
        textarea.description-form(v-model="form.description" placeholder="物品型号，在哪里捡到..")
      div.img-form(style="display:flex;")
        div(style="height:80px;width:80px;background-color:#ccc;" @click="onAddImageClick")
      div.assets-form
        div(style="display:flex;")
          div(style="flex:1;") 物品分类
          div(style="flex:4;")
            radio-group(class="radio-group" @change="radioChange")
                <label class="radio">
                  <radio value="lost"/> 寻找失物
                </label>
                <label class="radio">
                  <radio value="found"/> 寻找失主
                </label>
            //- input(type="radio" id="one" value="One" v-model="picked")
            //- span 寻找失物
            //- input(type="radio" id="two" value="One" v-model="picked")
            //- span 寻找失主
        div(style="display:flex;")
          div(style="flex:1") 物品分类
          input(style="flex:4" v-model="form.category" placeholder="请选择物品分类")
        div(style="display:flex;" @click="onLocationClick")
          div(style="flex:1") 地址定位
          div(style="flex:4;" ) 请选择位置 > 
        div(style="display:flex;")
          div(style="flex:1") 详细地址
          input(style="flex:4;"  v-model="form.address" placeholder="详细的地点名称")
        div(style="display:flex;")
          div(style="flex:1") 联系方式
          input(style="flex:4" v-model="form.contact" placeholder="请输入您的电话")
      div()
        button(style="height:3rem;vertical-align: middle;" type="primary") 发布
</template>

<script>
import card from '@/components/card'
import TimeTable from '@/components/TimeTable'
import { mapState } from 'vuex'
export default {
  data() {
    return {
      motto: 'Hello World',
      userInfo: {},
      courses: [],
      isLogin: false,
      tabIndex: 0,
      form: {
        title: '',
        description: '',
        category: '',
        contact: '',
        address: '',
        type: 'lost',
        imgsURL: []
      },
      items: [
        {
          name: 'lost',
          checked: null,
          value: '我丢了物品'
        },
        {
          name: 'found',
          checked: null,
          value: '我拾获物品'
        }
      ]
    }
  },
  computed: mapState(['user']),
  components: {
    card,
    TimeTable
  },
  methods: {
    radioChange(e) {
      this.form.type = e.target.value
    },
    onAddImageClick() {
      wx.chooseImage({
        success: function(res) {
          var tempFilePaths = res.tempFilePaths
          wx.uploadFile({
            url: 'https://example.weixin.qq.com/upload',
            filePath: tempFilePaths[0],
            name: 'file',
            formData: {
              user: 'test'
            },
            success: function(res) {
              // var data = res.data
              console.log(res)
            }
          })
        }
      })
    },
    onAddClick() {
      // todo
    },
    onLocationClick() {
      wx.chooseLocation({
        success: detail => {
          console.log('success')
          console.log(detail)
        }
      })
    },
    onPublishClick() {},
    postForm() {}
  },
  created() {}
}
</script>

<style scoped>
.form > div {
  /* padding-top: 10px; */
  margin-bottom: 5px;
}
.avatar {
  border-radius: 50%;
  height: 2rem;
  width: 2rem;
  margin: auto;
  display: block;
}
.assets-form {
  padding-top: 10px;
  font-size: 1.3rem;
  align-items: center;
  /* padding-bottom: 10px; */
  background-color: #fff;
  box-shadow: 0 5px 5px #ccd8e2;
  border-radius: 10px;
}
.assets-form > div :last-child {
  text-align: right;
  /* padding-right:10px; */
}
.assets-form > div {
  align-items: center;
  padding-left: 10px;
  padding-right: 10px;
  height: 4rem;
  border-bottom: 1px solid #ddd;
}
.assets-form div div:first-of-type {
  color: #aaa;
}
.img-form {
  /* height: 80px; */
  font-size: 1.3rem;
  padding-top: 10px;
  padding-left: 10px;
  padding-bottom: 10px;
  background-color: #fff;
  box-shadow: 0 5px 5px #ccd8e2;
  border-radius: 10px;
}
.title-form {
  height: 3rem;
  font-size: 1.3rem;
  padding-left: 10px;
  background-color: #fff;
  box-shadow: 0 5px 5px #ccd8e2;
  border-radius: 10px;
}
.description-form {
  height: 8rem;
  width: 100%;
  font-size: 1.3rem;
  padding-top: 10px;
  padding-left: 10px;
  background-color: #fff;
  box-shadow: 0 5px 5px #ccd8e2;
  border-radius: 10px;
  box-sizing: border-box;
}
.container {
  /* padding: 10px; */
  /* padding-right: 10px; */
  min-height: 100vh;
  padding-bottom: 10px;
  /* padding-top: 10px; */
  box-sizing: border-box;
  background: #eee;
}
.userinfo {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
