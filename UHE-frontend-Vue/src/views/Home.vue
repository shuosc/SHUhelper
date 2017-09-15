<template>
  <div>
    <v-layout class="mx-0 mb-2">
      <v-flex xs12>
        <v-card flat>
          <v-card-title>
            <div>你好 {{$store.state.user.name}}</div>
            <v-spacer></v-spacer>
            {{time.year+ '_'+time.term|term}},第{{time.week}}周,周{{time.day}}
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
      </v-card-text>
    </v-card>
    <v-card class="mb-2">
      <v-card-title primary-title class="pa-2">当前时间是 {{clock}}</v-card-title>
      <v-divider></v-divider>
      <v-card-text style="text-align:center;">
        还有{{timeLeft}}分钟进行第{{parseInt(point)+1%2===1?(parseInt(point)+2)/2+'节课':parseInt(point)/2+'节课间休息'}}
      </v-card-text>
    </v-card>
    <v-dialog v-model="dialog">
      <v-card>
        <v-card-title class="headline">{{publication.title}}</v-card-title>
        <v-card-text v-html="publication.content"></v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
const timeSChedule = [800, 845, 855, 940, 1000, 1045, 1055, 1140, 1210, 1255, 1305, 1350, 1410, 1455, 1505, 1550, 1600, 1645, 1655, 1740, 1800, 1845, 1855, 1940, 1950, 2035]
export default {
  filters: {
    term: function (value) {
      let map = {
        '1': '秋',
        '2': '冬',
        '3': '春',
        '4': '夏'
      }
      let year = parseInt(value.slice(2, 4))
      return `${year}-${year + 1}${map[value[5]]}`
    }
  },
  data () {
    return {
      items: ['1', '2', '3'],
      e1: '',
      fab: false,
      navs: [
        // { name: '我的宿舍', icon: 'bubble_chart', url: '/info' },
        // { name: '一卡通余额', icon: 'bubble_chart', url: '/info' },
        { name: '空教室', icon: 'iconfont-xiangtongfangjianrenwu', url: '/empty-room' },
        // { name: '体育活动', icon: 'bubble_chart', url: '/info' },
        { name: '校园地图', icon: 'iconfont-map-o', url: '/map' },
        // { name: '快速链接', icon: 'bubble_chart', url: '/info' },
        { name: '课程查询', icon: 'iconfont-book', url: '/courses-query' },
        { name: '学生财务', icon: 'iconfont-money', url: '/fin' },
        { name: '校车运行', icon: 'iconfont-bus', url: '/bus' },
        { name: '校历', icon: 'iconfont-rili', url: '/school-cal' },
        { name: '就医指导', icon: 'iconfont-yiyuan', url: '/med' },
        { name: '人生解答书', icon: 'iconfont-key', url: '/the-answer' },
        { name: '尔美订餐', icon: 'iconfont-dppj', url: '/external-service/ermei' },
        { name: '研习空间', icon: 'iconfont-fangjian', url: '/external-service/yanxi' },
        { name: '排课助手', icon: 'iconfont-paw', url: '/external-service/xk' },
        { name: '上大导航', icon: 'iconfont-iosnavigate', url: '/external-service/shuerlink' }
      ],
      publications: [
        {
          title: 'SHUhelper3上线啦~',
          content: '* SHUhelper3.0匆忙上线( <br/>* 好多功能还未完善，暂时屏蔽掉了 < br />* 开学愉快w < br />* Andoird APP现已上线< a href= "https://www.pgyer.com/apiv1/app/install?aId=e7c4929b91486d9f76a6b6790df36f76&_api_key=a6a7ba51429b6968af23b13eec01d815 " > 点击这里下载</a ><br />* iOS用户可以在safari中点击下方分享按钮，将网站发送至桌面，获得和APP一样的浏览效果< br />* 遇到问题可以直接在广场里发表哦< br /><span>* Powered By 上海大学开源社区 加入我们！<br />* QQ群：146685225</span><br />'
        }
      ],
      dialog: false,
      publication: {},
      time: {
        year: '',
        term: '',
        week: '',
        day: '',
        course: ''
      },
      timerID: '',
      clock: '',
      timeLeft: '',
      point: ''
    }
  },
  created () {
    this.getPublications()
    this.getTime()
    this.timerID = setInterval(this.updateTime, 1000)
  },
  beforeDestroy () {
    clearInterval(this.timerID)
  },
  methods: {
    zeroPadding (num, digit) {
      var zero = ''
      for (var i = 0; i < digit; i++) {
        zero += '0'
      }
      return (zero + num).slice(-digit)
    },
    updateTime () {
      var cd = new Date()
      var time = parseInt(this.zeroPadding(cd.getHours(), 2) + this.zeroPadding(cd.getMinutes(), 2))
      // console.log(time)
      for (let i in timeSChedule) {
        let scheduleMinutes = timeSChedule[i] % 100 + parseInt(timeSChedule[i] / 100) * 60
        let timeMinutes = time % 100 + parseInt(time / 100) * 60
        if (scheduleMinutes - timeMinutes >= 0) {
          this.timeLeft = scheduleMinutes - timeMinutes
          this.point = i
          break
        }
      }
      this.clock = this.zeroPadding(cd.getHours(), 2) + ':' + this.zeroPadding(cd.getMinutes(), 2) + ':' + this.zeroPadding(cd.getSeconds(), 2)
    },
    getTime () {
      this.$http.get('/api/v1/time/')
        .then((response) => {
          this.time.year = response.data.year
          this.time.term = response.data.term
          this.time.week = response.data.week
          this.time.day = response.data.day
          this.time.course = response.data.course
        })
    },
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
