<template>
  <div>
    <v-layout class="mx-0 mb-2">
      <v-flex xs12>
        <v-card flat>
          <v-card-title>
            <div>你好 {{$store.state.user.name}}</div>
            <v-spacer></v-spacer>
            <div>晴 32C D楼附近</div>
          </v-card-title>
          <!-- <v-card-text>
               <v-text-field name="input-1-3" label="搜索功能 活动 人 课程 ..." single-line prepend-icon="search" hide-details></v-text-field> 
            </v-card-text> -->
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout class="mx-0 mb-2">
      <v-flex xs12 class="pa-0">
        <v-card>
          <v-layout row wrap class="ma-0">
            <v-flex xs3 v-for="(link,index) in navs" :key="index">
              <div style="width:100%;height:100%;cursor:pointer;" @click="$router.push(link.url)">
                <v-icon v-html="link.icon" style="display:flex;">
                </v-icon>
                <p style="text-align:center;" class="mb-1">{{link.name}}</p>
              </div>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row class="ma-2">
      <span>动态推荐</span>
      <v-spacer></v-spacer>
      <span style="font-size:0.5rem;color:grey;">管理卡片出现规则
        <v-icon>favorite</v-icon>
      </span>
    </v-layout>
    <v-card class="mb-2">
      <v-card-title primary-title class="pa-2">通知公告</v-card-title>
      <v-divider></v-divider>
      <v-card-text>喵喵喵</v-card-text>
      <v-card-actions class="pa-0">
        <v-btn block class="orange--text ma-0">查看详情</v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="mb-2">
      <v-card-title primary-title class="pa-2">附近的空教室</v-card-title>
      <v-divider></v-divider>
      <v-card-text>喵喵喵</v-card-text>
      <v-card-actions class="pa-0">
        <v-btn block class="orange--text ma-0">查看详情</v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="mb-2">
      <v-card-title primary-title class="pa-2">附近的课程</v-card-title>
      <v-divider></v-divider>
      <v-card-text>喵喵喵</v-card-text>
      <v-card-actions class="pa-0">
        <v-btn block class="orange--text ma-0">查看详情</v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="mb-2">
      <v-card-title primary-title class="pa-2">最近的活动</v-card-title>
      <v-divider></v-divider>
      <v-card-text>喵喵喵</v-card-text>
      <v-card-actions class="pa-0">
        <v-btn block class="orange--text ma-0">查看详情</v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="mb-2">
      <v-card-title primary-title class="pa-2">最近的活动</v-card-title>
      <v-divider></v-divider>
      <v-card-text>喵喵喵</v-card-text>
      <v-card-actions class="pa-0">
        <v-btn block class="orange--text ma-0">查看详情</v-btn>
      </v-card-actions>
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
        { name: '一卡通', icon: 'bubble_chart', url: '/info' },
        { name: '体育活动', icon: 'bubble_chart', url: '/info' },
        { name: '尔美订餐', icon: 'bubble_chart', url: '/http://ermei.shuhelper.cn?code=ermeishu' },
        { name: '校园地图', icon: 'bubble_chart', url: '/map' },
        { name: '安全地图', icon: 'bubble_chart', url: '/security-map' },
        { name: '快速链接', icon: 'bubble_chart', url: '/info' },
        { name: '全部功能', icon: 'bubble_chart', url: '/apps' }
      ]
    }
  },
  created () {
    this.$router.push('/')
  }
}
</script>
<style lang="stylus">

</style>
