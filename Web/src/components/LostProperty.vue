<template lang="pug">
  div
    q-card(v-for="item in items" @click="AddPropertyDetail")
      q-card-media
        q-parallax(:src="'/statics/course-back.jpg'" :height="150")
        q-card-title {{item.name}}
          span(slot="subtitle") {{item.place}}&nbsp{{item.detail}}
    //q-modal(v-model="PropertyDetail" minimized  :content-css="{minWidth: '80vw'}")
      q-card.no-margin
        q-card-title {{item.name}}


    //div(slot="footer")
      q-tabs(align="justify")
        q-route-tab(icon="fa-xuexiao" to="/" exact @click="onClick('index')" slot="title")
        q-route-tab(icon="explore" to="/apps" exact  @click="onClick" slot="title")
        q-route-tab(icon="fa-filtervintage" to="/square" exact @click="onClick('square')" slot="title")
        q-route-tab(icon="fa-calendar1" to="/schedule" exact @click="onClick" slot="title")
</template>

<script>
import LostPropertyCard from '@/LostPropertyCard'
import { QTabs, QRouteTab, Events, QParallax } from 'quasar'
export default {
  components: {
    QParallax,
    LostPropertyCard,
    QTabs,
    QRouteTab
    },
  data(){
    return{
        PropertyDetail: 'false',
        items: [{
          "name": "学生卡",
          "place": "新世纪",
          "detail": "新世纪保安亭领取",
          "img": "/statics/course-back.jpg"
        },
        {
          "name": "8G内存条",
          "place": "东区计算机大楼",
          "detail": "被私吞了",
          "img": "/statics/course-back.jpg"
        }]
    }
  },
  methods: {
    AddPropertyDetail() {
      this.PropertyDetail= true
    }
  }
}
</script>    