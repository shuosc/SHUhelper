<template>
  <div>
    <v-layout class="mx-0 mb-2">
      <v-flex xs12>
        <v-card flat>
          <v-card-title>
            <div>你好 {{$store.state.user.name}}</div>
            <v-spacer></v-spacer>
            <!-- <div>晴 32C D楼附近</div> -->
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
                <v-icon v-html="link.icon" class="blue--text" style="display:flex;">
                </v-icon>
                <p style="text-align:center;" class="mb-1">{{link.name}}</p>
              </div>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row class="ma-2">
      <!-- <span>动态推荐</span> -->
      <v-spacer></v-spacer>
      <!-- <span style="font-size:0.5rem;color:grey;">管理卡片出现规则
                            <v-icon>favorite</v-icon> -->
      </span>
    </v-layout>

    <v-card class="mb-2">
      <v-card-title primary-title class="pa-2">通知公告</v-card-title>
      <v-divider></v-divider>
      <v-card-text class="">
        <ul>
          <li v-for="publication in publications" :key="publication.title" @click.stop="showPublication(publication)">{{publication.title}}
          </li>
        </ul>
        <!-- 
              <!-- <v-divider></v-divider>
                      * iOS用户可以在safari中点击右上角，将网站发送至桌面，获得和APP一样的浏览效果
                       <br/>
                      <v-divider></v-divider>
                      * iOS用户可以在safari中点击右上角，将网站发送至桌面，获得和APP一样的浏览效果 -->
      </v-card-text>
      <!-- <v-card-actions class="pa-0">
                            <v-btn block class="orange--text ma-0">查看详情</v-btn>
                          </v-card-actions> -->
    </v-card>
    <!-- <v-card class="mb-2">
                          <v-card-title primary-title class="pa-2">迎新频道</v-card-title>
                          <v-divider></v-divider>
                          <v-card-text>SHUhelper3.0已经开始公测 </v-card-text> -->
    <!-- <v-card-actions class="pa-0">
                            <v-btn block class="orange--text ma-0">查看详情</v-btn>
                          </v-card-actions> -->
    </v-card>
    <!-- <v-card class="mb-2">
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
                        </v-card> -->
    <v-dialog v-model="dialog">
      <v-card>
        <v-card-title class="headline">{{publication.title}}</v-card-title>
        <v-card-text v-html="publication.content"></v-card-text>
        <!-- <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="green--text darken-1" flat="flat" @click.native="dialog = false">Disagree</v-btn>
            <v-btn class="green--text darken-1" flat="flat" @click.native="dialog = false">Agree</v-btn>
          </v-card-actions> -->
      </v-card>
    </v-dialog>
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
        // { name: '我的宿舍', icon: 'bubble_chart', url: '/info' },
        // { name: '一卡通余额', icon: 'bubble_chart', url: '/info' },
        // { name: '空教室', icon: 'iconfont-xiangtongfangjianrenwu', url: '/empty-room' },
        // { name: '体育活动', icon: 'bubble_chart', url: '/info' },
        { name: '校园地图', icon: 'iconfont-map-o', url: '/map' },
        // { name: '快速链接', icon: 'bubble_chart', url: '/info' },
        { name: '课程查询', icon: 'iconfont-book', url: '/courses-query' },
        { name: '学生财务', icon: 'iconfont-money', url: '/fin' },
        { name: '校车运行', icon: 'iconfont-bus', url: '/bus' },
        { name: '校历', icon: 'iconfont-rili', url: '/school-cal' },
        { name: '就医指导', icon: 'iconfont-yiyuan', url: '/med' }
        // { name: '尔美订餐', icon: 'bubble_chart', url: 'http://ermei.shuhelper.cn?code=ermeishu' }
      ],
      publications: [
        {
          title: 'SHUhelper3上线啦~',
          content: '* SHUhelper3.0匆忙上线( <br/>* 好多功能还未完善，暂时屏蔽掉了 < br />* 开学愉快w < br />* Andoird APP现已上线< a href= "https://www.pgyer.com/apiv1/app/install?aId=e7c4929b91486d9f76a6b6790df36f76&_api_key=a6a7ba51429b6968af23b13eec01d815 " > 点击这里下载</a ><br />* iOS用户可以在safari中点击下方分享按钮，将网站发送至桌面，获得和APP一样的浏览效果< br />* 遇到问题可以直接在广场里发表哦< br /><span>* Powered By 上海大学开源社区 加入我们！<br />* QQ群：146685225</span><br />'
        }
      ],
      dialog: false,
      publication: {}
    }
  },
  created () {
    this.getPublications()
    // this.$router.push('/')
  },
  methods: {
    getPublications () {
      this.$http.get('/api/v1/publications/')
        .then((response) => {
          this.publications = response.data
        })
    },
    showPublication (publication) {
      this.publication = publication
      this.dialog = true
    }
  }
}
</script>
<style lang="stylus">

</style>
