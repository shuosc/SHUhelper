<template>
  <div>
    <v-card>我的应用</v-card>
    <v-card>
      <v-container fluid grid-list-xs>
        <v-layout row wrap>
          <v-flex xs3 v-for="(link,index) in navs" :key="index">
            <div style="width:100%;height:100%;cursor:pointer;" @click="$router.push(link.url)">
              <v-icon v-html="link.icon" style="display:flex;">
              </v-icon>
              <p style="text-align:center;" class="my-1">{{link.name}}</p>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
      <v-divider class="mt-2"></v-divider>
      <span style="border-left-style:solid;border-color:teal;border-width:5px;margin:1rem;margin-top:1rem;padding-left:0.5rem;display:block;">2312</span>
       <v-container fluid grid-list-xs>
        <v-layout row wrap>
          <v-flex xs3 v-for="(link,index) in navs" :key="index">
            <div style="width:100%;height:100%;cursor:pointer;" @click="$router.push(link.url)">
              <v-icon v-html="link.icon" style="display:flex;">
              </v-icon>
              <p style="text-align:center;" class="my-1">{{link.name}}</p>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </div>
</template>
<script>
export default {
  data () {
    return {
      items: ['1', '2', '3'],
      e1: '',
      fab: false,
      navs: [
        { name: '图书馆', icon: 'bubble_chart', url: '/info' },
        { name: '自习室', icon: 'bubble_chart', url: '/info' },
        { name: '一卡通', icon: 'bubble_chart', url: '/info' },
        { name: '体育活动', icon: 'bubble_chart', url: '/info' },
        { name: '寻人', icon: 'bubble_chart', url: '/info' },
        { name: '课程总览', icon: 'bubble_chart', url: '/info' },
        { name: '校园助手', icon: 'bubble_chart', url: '/info' },
        { name: '场馆开放', icon: 'bubble_chart', url: '/info' },
        { name: '校园地图', icon: 'bubble_chart', url: '/info' },
        { name: '美食推荐', icon: 'bubble_chart', url: '/info' },
        { name: '快速链接', icon: 'bubble_chart', url: '/info' },
        { name: '全部功能', icon: 'bubble_chart', url: '/apps' }
      ]
    }
  }
}
</script>
<style lang="stylus">

</style>
