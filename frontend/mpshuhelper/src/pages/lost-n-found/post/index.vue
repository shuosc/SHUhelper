<template lang="pug">
  div
    div.row.justify-center(style="margin-top: 5px;" v-show="loaded")
      div.card.col-10
        div.row.main-info
          div.col-2.avatar-wrapper
            img.avatar(:src="'https://static.shuhelper.cn/' + post.authorAvatar")
          div.col-6.info-wrapper
            div.name {{post.authorName}}
            div.date {{post.occurTime}}
      div.card.col-10
        div.title {{post.title}}
        //- div.tags
        div.tag-wrapper
          span.tag-name 类别：
          span.tag {{post.category}}
        div.tag-wrapper
          div.content
            span.tag-name 详情：
            | {{post.content}}
        div.tag-wrapper
          span.tag-name 失物招领点：
          span.tag(v-if="post.site") {{sitesMap[post.site]}}
          span.tag(v-else) 无
        div.tag-wrapper
          span.tag-name 位置：
          span.tag {{post.address}}
          button(@click="onMapClick" style="margin-top:10px;") 在地图中查看
        div.image-wrapper(v-for="img in post.imgURLs")
          img.imageItem(mode="widthFix",:src="img")
      div.card.col-10(v-if="post.authorID===user.userID")
        div.row
          div.col-12
            div(class="weui-cell weui-cell_switch")
              div(class="weui-cell__bd") 已找到
              div(class="weui-cell__ft")
                switch(:checked="post.isFound" @change="onSwitchChange")
          div.col-12(style="margin-top:5px;box-sizing:border-box;")
            button(@click="onLightenClick" type="primary") 点亮
          div.col-12(style="margin-top:5px;")
            button(@click="onDeleteClick" type="warn") 删除

      //- div.card.col-10
        map(id="map" :longitude="post.longitude" :latitude="post.latitude" :markers="markers" scale="19" show-location style="width: 100%; height: 300px;")


      div.card.col-10(style="margin-bottom: 50px;")
        p.title 联系方式
        div.contact-wrapper
          p.date 电话
          p.name {{post.contact}}
        //- div.contact-wrapper
          p.date 微信
          p.name kastnerorz
          div.card.col-10

    div.bottom-bar
      //- div.bottom-button-wrapper
      //- div.bottom-button(@click="onHomeClick") 首页
      //- div.bottom-button 收藏
      //- div.bottom-button 分享
      div.bottom-button(@click="onContactClick") 一键联系： {{post.contact}}
</template>
<script>
import { sitesMap } from '@/utils'
import { mapState } from 'vuex'
export default {
  data() {
    return {
      id: '',
      mapVisiable: false,
      post: {},
      sitesMap: sitesMap,
      loaded: false
    }
  },
  computed: mapState(['user', 'time']),
  mounted() {
    // let now = new Date()
    // this.date = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    this.loaded = false
    this.post = {}
    this.id = this.$root.$mp.query.id
    // this.date = this.$moment(this.$root.$mp.query.date, 'YYYY-MM-DD')
    this.getPost(this.id)
  },
  onShow() {
    wx.showNavigationBarLoading()
  },
  methods: {
    onSwitchChange(e) {
      wx.showModal({
        title: '提示',
        content: '确认修改目前状态吗',
        success: res => {
          if (res.confirm) {
            this.switchStatus(e.target.value)
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    },
    onLightenClick() {
      wx.showModal({
        title: '提示',
        content: '点亮后，您的帖子将会显示在搜索结果的最前方，确认操作吗',
        success: res => {
          if (res.confirm) {
            this.lightenPost()
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    },
    onDeleteClick() {
      wx.showModal({
        title: '提示',
        content: '确定要删除吗',
        success: res => {
          if (res.confirm) {
            this.deletePost()
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    },
    switchStatus(value) {
      this.$http.put(`/lost-n-found/${this.post.id}`, { isFound: value }).then(resp => {
        this.post = resp.post
        wx.showToast({
          title: '修改状态成功',
          icon: 'success',
          duration: 2000
        })
      })
    },
    lightenPost() {
      this.$http.get(`/lost-n-found/${this.post.id}/lighten`).then(resp => {
        this.post = resp.post
        wx.showToast({
          title: '点亮成功',
          icon: 'success',
          duration: 2000
        })
      })
    },
    deletePost() {
      this.$http.delete(`/lost-n-found/${this.post.id}`).then(resp => {
        // this.post = resp.post
        wx.redirectTo({ url: '../success/main' })
      })
    },
    onMapClick() {
      wx.navigateTo({ url: `../map/main?longitude=${this.post.longitude}&latitude=${this.post.latitude}` })
    },
    onContactClick() {
      wx.makePhoneCall({
        phoneNumber: this.post.contact
      })
    },
    onHomeClick() {
      wx.reLaunch({ url: '/pages/index/main' })
    },
    getPost(id) {
      this.$http.get(`/lost-n-found/${id}`).then(resp => {
        this.loaded = true
        this.post = resp.post
        this.post.occurTime = this.$moment(this.post.occurTime).format('YYYY-MM-DD')
        console.log(resp)
        wx.hideNavigationBarLoading()
      })
    }
  }
}
</script>
<style scoped>
.hr {
  border: 0.5px solid rgba(32, 33, 36, 0.28);
}

.card {
  background-color: white;
  padding: 11px 16px 11px 16px;
  box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
  border-radius: 8px;
  margin: 0 0 10px 0;
}
.avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
}

/* .main-info {
  padding: 11px 16px 0 16px;
}

.contact-info {
  padding: 11px 0 11px 16px;
} */
.info-wrapper {
  padding: 0 0 0 10px;
}

.name {
  font-weight: bold;
  padding-top: 3px;
  font-size: 16px;
}

.date {
  padding-top: 3px;
  color: #888;
  font-size: 14px;
}

.title {
  font-size: 17pt;
}

.tags {
  margin-top: 3px;
  flex-direction: row;
  flex-wrap: wrap;
}

.tag-wrapper {
  margin-bottom: 6px;
}

.tag-name {
  font-size: 13px;
  color: #888;
  margin-right: 4px;
}

.tag {
  border-radius: 4px;
  background-color: #7eb3ec;
  color: #fff;
  font-size: 13px;
  height: 16px;
  padding: 3px;
  margin: 0 3px 0 0;
}

.content {
  font-size: 14px;
}

.image-wrapper {
  justify-content: center;
  display: flex;
  margin: 10px 0 10px 0;
}

.imageItem {
  width: 100%;
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  width: 100vw;
  background-color: #7eb3ec;
  height: 40px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 1rem;
  box-sizing: border-box;
}

/* .bottom-button-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
} */

.bottom-button {
  color: #fff;
  font-size: 14px;
}
</style>
