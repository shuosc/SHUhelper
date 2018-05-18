<template lang="pug">
  div(class="container")
    //- img(@click="onAvatarClick",style="height:1.5rem;width:1.5rem;margin:auto;display:block;" class="userinfo-avatar" v-if="user.avatarURL" :src="user.avatarURL" background-size="cover")
    div.form(style="padding:10px;display:flex;flex-direction:column;")
      div
        input.title-form(placeholder="请输入标题" v-model="title")
      div
        textarea.description-form(v-model="content" placeholder="物品型号，在哪里捡到..")
      div.img-form
        div(style="background-color:#ccc;" v-for="img in imgURLs")
          img(:src="img+'-thumbnail'" style="object-fit: cover;width:100%;height:100%;" )
        div(style="background-color:#ccc;" @click="onAddImageClick")
      div.assets-form
        //- div(style="display:flex;")
          div(style="flex:1;") 发生时间
          div(style="flex:4;")
        div(style="display:flex;")
          div(style="flex:1") 失物招领点
          //- input(style="flex:4" v-model="category" placeholder="请选择物品分类")
          picker(@change="bindPickerChangeSite" :value="siteIndex" :range="sites")
            view {{sites[siteIndex]}} >
        div(style="display:flex;")
          div(style="flex:1;") 物品分类
          div(style="flex:4;")
            radio-group(class="radio-group" @change="radioChange")
              label.radio 寻找失物
                radio(value="lost" :checked="true")
              label.radio 寻找失主
                radio(value="found")
        div(style="display:flex;")
          div(style="flex:1") 物品分类
          //- input(style="flex:4" v-model="category" placeholder="请选择物品分类")
          picker(@change="bindPickerChange" :value="categoryIndex" :range="categories")
            view {{categories[categoryIndex]}} >
        div(style="display:flex;" @click="onLocationClick")
          div(style="flex:1") 地址定位
          div(style="flex:4;" v-if="!location.latitude" ) 请选择位置 >
          div(style="flex:4;" v-else) 重新选择 >
        div(style="display:flex;")
          div(style="flex:1") 详细地址
          input(style="flex:4;"  v-model="location.name" placeholder="详细的地点名称")
        //- div(style="display:flex;")
          div(style="flex:1") 详细地址
          input(style="flex:4;"  v-model="location.name" placeholder="详细的地点名称")
        div(style="display:flex;")
          div(style="flex:1") 联系方式
          input(style="flex:4" v-model="contact" placeholder="请输入您的电话")
      div()
        button( :loading="submitLoading",:disabled="disable" style="vertical-align: middle;" type="primary" @click="onPublishClick") 发布
</template>

<script>
import card from '@/components/card'
import TimeTable from '@/components/TimeTable'
import { mapState } from 'vuex'
import { lostNFoundSites } from '@/utils'
export default {
  data() {
    return {
      motto: 'Hello World',
      userInfo: {},
      courses: [],
      isLogin: false,
      tabIndex: 0,
      categoryIndex: 0,
      categories: ['证件', '数码', '书本', '箱包', '衣物', '其他'],
      location: {
        latitude: null,
        longitude: null,
        name: '',
        address: ''
      },
      title: '',
      content: '',
      category: '',
      contact: '',
      submitLoading: '',
      address: '',
      type: 'lost',
      siteIndex: 0,
      imgURLs: [],
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
  computed: {
    sites: function() {
      let names = []
      lostNFoundSites.forEach(e => {
        names.push(e.name)
      })
      return names
    },
    disable: function() {
      return !(this.title && this.content && this.location.longitude && this.contact)
    },
    form: function() {
      return {
        title: this.title,
        content: this.content,
        category: this.categories[this.categoryIndex],
        contact: this.contact,
        address: this.location.name,
        type: this.type,
        imgURLs: this.imgURLs,
        latitude: this.location.latitude,
        longitude: this.location.longitude,
        site: lostNFoundSites[this.siteIndex].value
        // occurredTime: this.occurredTime
      }
    },
    ...mapState(['user'])
  },
  components: {
    card,
    TimeTable
  },
  methods: {
    bindPickerChange(e) {
      this.categoryIndex = e.target.value
    },
    bindPickerChangeSite(e) {
      this.siteIndex = e.target.value
    },
    radioChange(e) {
      this.type = e.target.value
    },
    onAddImageClick() {
      wx.chooseImage({
        success: res => {
          // eslint-disable-next-line
          var tempFilePaths = res.tempFilePaths
          var ramdomName =
            Math.random()
              .toString(36)
              .substr(2) + tempFilePaths[0].match(/\.?[^./]+$/)
          let key = `post/lost-n-found/${this.user.userID}/${ramdomName}`
          this.$http.get(`/upload/token?key=${key}`).then(response => {
            let token = response.uptoken
            wx.uploadFile({
              url: 'https://upload.qiniup.com',
              filePath: `${tempFilePaths[0]}`,
              name: 'file',
              formData: {
                user: 'test',
                key: key,
                token: token
              },
              success: res => {
                console.log(res)
                this.imgURLs.push(`https://static.shuhelper.cn/${key}`)
              }
            })
          })
        }
      })
    },
    onAddClick() {
      // todo
    },
    onLocationClick() {
      wx.chooseLocation({
        success: res => {
          this.location = res
        }
      })
    },
    onPublishClick() {
      wx.showModal({
        title: '提示',
        content: '确定要发布吗',
        success: res => {
          if (res.confirm) {
            console.log('用户点击确定')
            this.postForm()
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    },
    postForm() {
      let form = this.form
      this.submitLoading = true
      this.$http
        .post('/lost-n-found/', form)
        .then(resp => {
          console.log(resp)
          this.submitLoading = false
          wx.redirectTo({
            url: '../success/main'
          })
        })
        .catch(err => {
          this.submitLoading = false
          console.log(err)
        })
    }
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
  padding: 10px;
  background-color: #fff;
  box-shadow: 0 5px 5px #ccd8e2;
  border-radius: 10px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}
.img-form > div {
  /* flex: 0 0 33%; */
  /* padding-top: 33%; */
  /* flex: 0 0 32%; */
  width: 50px;
  height: 50px;
  margin: 2px;
  /* box-sizing: border-box; */
}
.img-form > div > img {
  width: 100%;
  height: 100%;
  /* margin:2px; */
  /* box-sizing: border-box; */
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
