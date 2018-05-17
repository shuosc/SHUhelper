<template lang="pug">
  div
    div.row.justify-center(style="margin-top: 5px;")
      div.card.col-10
        div.row.main-info
          div.col-2.avatar-wrapper
            img.avatar(:src="'https://static.shuhelper.cn/' + post.authorAvatar")
          div.col-9.info-wrapper
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
          span.tag-name 位置：
          span.tag {{post.address}}
          button(@click="mapVisiable=!mapVisiable" style="margin-top:10px;") {{mapVisiable?'折叠':'展开'}}地图
        map(v-show="mapVisiable" id="map" :longitude="post.longitude" :latitude="post.latitude" :markers="markers" scale="19" show-location style="width: 100%; height: 300px;")        
        div.image-wrapper(v-for="img in post.imgURLs")
          img.imageItem(mode="widthFix",:src="img")
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
    div.bottom-bar
      //- div.bottom-button-wrapper
      //- div.bottom-button(@click="onHomeClick") 首页
      //- div.bottom-button 收藏
      //- div.bottom-button 分享
      div.bottom-button(@click="onContactClick") 一键联系： {{post.contact}}
</template>
<script>
export default {
  data() {
    return {
      id: '',
      mapVisiable: false,
      post: {}
    }
  },
  computed: {
    markers: function() {
      return [
        {
          iconPath: '/static/marker.png',
          id: 0,
          latitude: this.post.latitude,
          longitude: this.post.longitude,
          width: 50,
          height: 50
        }
      ]
    }
  },
  mounted() {
    // let now = new Date()
    // this.date = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    this.post = {}
    this.id = this.$root.$mp.query.id
    // this.date = this.$moment(this.$root.$mp.query.date, 'YYYY-MM-DD')
    this.getPost(this.id)
  },
  methods: {
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
        this.post = resp.post
        this.post.occurTime = this.$moment(this.post.occurTime).format('YYYY-MM-DD')
        console.log(resp)
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
