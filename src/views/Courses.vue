<template>
  <scroller lock-x
            scrollbar-y
            height="-96"
            ref="scroller"
            use-pullup
            @on-pullup-loading="getCourses()">
    <div>
      <group gutter="0">
        <x-input title="课程名"
                 v-model="coursename"></x-input>
        <x-input title="教师名"
                 v-model="teachname"></x-input>
        <selector title="校区"
                  :options="['本部','嘉定','延长']"
                  v-model="campus"></selector>
      </group>
      <x-button type="primary"
                @click.native="(page=1)&&getCourses()">查询</x-button>
      <divider>查询结果</divider>
      <table style="text-align:center;width:100%;">
        <thead>
          <tr style="font-size:0.4rem;background-color: rgba(100, 109, 237, 0.70);">
            <th style="width:50px;">课程号</th>
            <th>课程名</th>
            <th>教师名</th>
            <th>课程地点</th>
            <th>课程时间</th>
            <th>答疑地点</th>
            <th>答疑时间</th>
          </tr>
        </thead>
        <tbody style="font-size:0.6rem;background-color: rgba(100, 109, 237, 0.10);">
          <tr v-for="course in list">
            <td>{{course.courseno}}</td>
            <td>{{course.coursename}}</td>
            <td>{{course.teachname}}</td>
            <td>{{course.courseplace}}</td>
            <td>{{course.coursetime}}</td>
            <td>{{course.qplace}}</td>
            <td>{{course.qtime}}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </scroller>
</template>

<script>
import { Group, Cell, Tabbar, TabbarItem, XHeader, Divider, Card, XNumber, Flexbox, FlexboxItem, XImg, Scroller, ViewBox, XButton, Popup, Radio, XInput, Checker, CheckerItem, Grid, GridItem, GroupTitle, Marquee, MarqueeItem, XTable, Selector } from 'vux'

export default {
  components: {
    Grid,
    Marquee,
    MarqueeItem,
    XTable,
    GroupTitle,
    GridItem,
    Group,
    Cell,
    Tabbar,
    TabbarItem,
    XHeader,
    Divider,
    Card,
    XNumber,
    FlexboxItem,
    Flexbox,
    XImg,
    Scroller,
    Selector,
    ViewBox,
    XButton,
    Popup,
    Radio,
    XInput,
    Checker,
    CheckerItem
  },
  data() {
    return {
      coursename: '',
      teachname: '',
      campus: '',
      time: '',
      rooms: [],
      page: 1,
      list: [],
      total: 0
    }
  },
  computed: {
  },
  created: function () {
    this.getCourses()
  },
  methods: {
    resetScroller() {
      this.$nextTick(() => {
        this.$refs.scroller.reset()
      })
    },
    getCourses() {
      this.$http.get('/xk/getcourse', {
        params: {
          courseno: '',
          coursename: this.coursename,
          teachname: this.teachname,
          coursetime: '',
          credit: '',
          campus: this.campus,
          page: this.page
        }
      }).then((response) => {
        if (this.page !== 1) {
          this.list = this.list.concat(response.data.list)
          if (response.data.list.length === 0) {
            this.$vux.toast.show({
              position: 'bottom',
              type: 'text',
              text: '无更多数据'
            })
          } else {
            this.$vux.toast.show({
              position: 'bottom',
              type: 'text',
              text: '查询成功'
            })
          }
        } else {
          this.list = response.data.list
          this.$vux.toast.show({
            position: 'bottom',
            type: 'text',
            text: '查询成功'
          })
        }
        this.total = response.data.total
        this.page++
        this.resetScroller()
        this.$refs.scroller.donePullup()
      })
    }
  }
}
</script>

<style>
#info {
  color: #fff;
  border-radius: 15px;
  margin: 10px;
  padding: 5px;
  font-size: 1rem;
  background-color: rgba(83, 134, 139, 0.90);
  text-shadow: 0px 0px 0px #000;
  text-align: center;
}

#rooms {
  color: #fff;
  border-radius: 15px;
  margin: 10px;
  padding: 5px;
  font-size: 0.8rem;
  background-color: rgba(100, 109, 237, 0.70);
  text-shadow: 0px 0px 0px #000;
  text-align: center;
}
</style>
