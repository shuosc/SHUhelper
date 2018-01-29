<template lang="pug">
  div
    q-card.namecard
      q-card-title(style="margin: 0;padding: 0")
        q-spinner(slot="right" v-if="loading" style="color: #e2aa6f")
        q-icon(slot="right" v-else name="refresh" @click="renewData")
        q-icon(slot="right" name="info" @click="dialog.handler()")
      q-card-main
        q-list(class="no-border")
          q-item
            q-item-side
              q-icon(color='primary', name='fa-tiyujiankang', style='font-size:2rem;')
            q-item-main
              q-item-tile(label='') 晨跑:{{this.data.sport}}/5 &nbsp 课外活动:{{this.data.act}}/5 
              q-item-tile(label='') 免晨跑:{{this.data.sport_reduce}} &nbsp 免课外:{{this.data.act_reduce}}
              q-item-tile(sublabel='' v-if="success") 晨跑辛苦啦(´▽｀)
              q-item-tile(sublabel='' v-else) 体育学院服务器又挂啦，明天来试试吧
          q-item(v-if="this.data.sport<=5")
            q-item-main
               q-progress(:percentage='(this.data.sport + this.data.act + this.data.sport_reduce + this.data.act_reduce)/10*100',color='teal-4')
      q-card-separator
      q-card-actions
        q-btn.full-width(flat @click="open()")
          | 查看本学期课外活动表
    q-modal(ref="activitiesTable" :content-css="{minWidth: '80vw', minHeight: '80vh'}")
      q-modal-layout
        q-toolbar(slot="header" color="primary")
          q-btn(color="white" flat @click="close")
            q-icon(name="close")
            q-toolbar-title
              | 课外活动表
        div(v-if="activitiesTableOpen")
          <q-card>
            <q-card-title>
              |  筛选
            </q-card-title>
            q-card-main
              div(class="rlayout-padding row justify-center")
              div(class="row" style="width: 500px; max-width: 90vw;")
                q-checkbox(class="col-6" v-for="sport in sports" v-model="sportFilter" :label='sport.name' :val='sport.val' :key="sport.val")
          </q-card>
          <q-card v-for="sport in sportsFiltered" :key="sport.val" >
            <q-card-title>
              |  {{sport.name}}  @{{sport.place}}
            </q-card-title>
            <q-card-separator />
            <q-list>
              <q-item v-for="item in sport.items" :key="item.day">
                <q-item-main>
                  <q-item-tile label>{{item.teacher}}</q-item-tile>
                  <q-item-tile sublabel>{{item.day}}  {{item.time}} </q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </q-card>
</template>

<script>
// const sports =
import { decrypt } from 'src/libs/utils.js'
import { Dialog, Toast, QProgress, QSpinner, QCheckbox } from 'quasar'
export default {
  name: 'sportCard',
  components: { QProgress, QSpinner, QCheckbox },
  data() {
    return {
      dialog: {
        label: '数据异常',
        icon: 'warning',
        handler() {
          Dialog.create({
            title: '数据异常',
            message: `
            在很多情况下次数会延迟很久很久更新
            <br/>
            如果不放心可以到上海大学微信公众号查看完整记录
            <br/>
            另外，提示查询失败一般是体育学院服务器挂掉啦，请明天再来。`
          })
        }
      },
      time: {
        year: '喵喵喵',
        term: '喵喵喵',
        week: '喵喵喵',
        day: '喵喵喵',
        course: '喵喵喵'
      },
      passwordVisiable: false,
      data: {
        run: 0,
        act: 0
      },
      loading: false,
      popup: false,
      detail: null,
      phypassword: '',
      status: {
        lastModified: null,
        status: 'loading',
        remark: '信息来自上海大学体育学院'
      },
      success: false,
      activitiesTableOpen: false,
      sportFilter: [],
      sports: []
    }
  },
  created() {
    // this.renewData()
    this.getTime()
    this.getData()
  },
  computed: {
    sportsFiltered: function() {
      let filtered = this.sports
      if (this.sportFilter.length !== 0) {
        filtered = []
        this.sportFilter.forEach(item => {
          this.sports.forEach(s => {
            if (s.val === item) {
              filtered.push(s)
            }
          })
        })
      }
      return filtered
    }
  },
  methods: {
    getSportSchedule() {
      if (this.sports.length !== 0) {
        return
      }
      this.$http.get('/statics/sports_17_winter.json').then(response => {
        this.sports.push(...response.data)
      })
    },
    getTime() {
      this.$http.get('/api/time/').then(response => {
        this.time.year = response.data.year
        this.time.term = response.data.term
        this.time.week = response.data.week
        this.time.day = response.data.day
        this.time.course = response.data.course
      })
    },
    open() {
      this.activitiesTableOpen = true
      this.getSportSchedule()
      this.$refs.activitiesTable.open()
    },
    close() {
      this.activitiesTableOpen = false
      this.$refs.activitiesTable.close()
    },
    getData() {
      this.loading = true
      this.$http
        .get(`/api/users/query/tiyu/`)
        .then(response => {
          this.status.status = response.data.status
          this.status.time = response.data.last_modified.$date
          let now = new Date()
          now.setSeconds(0)
          now.setMinutes(0)
          now.setMilliseconds(0)
          now.setHours(0)
          // console.log()
          // console.log(this.status.time - 8 * 3600 * 1000)
          if (this.status.time - 8 * 3600 * 1000 < now.valueOf()) {
            this.renewData()
          }
          this.success = response.data.status === 'success'
          this.data = decrypt(
            response.data.data,
            this.$store.state.user.password
          )
          // console.log(this.data)
          this.data.sport = parseInt(this.data.sport)
          this.data.act = parseInt(this.data.act)
          this.data.sport_reduce = parseInt(this.data.sport_reduce)
          this.data.act_reduce = parseInt(this.data.act_reduce)
          // console.log(this.data)
          this.loading = false
        })
        .catch(err => {
          console.log(err)
          this.loading = false
          if (err.response.status === 404) {
            this.renewData()
          } else {
            Toast.create('体育查询失败，可能是体育学院服务器挂掉啦')
          }
        })
    },
    renewData() {
      Toast.create('更新体育数据中')
      this.loading = true
      this.status.status = 'loading'
      this.$http
        .post(`/api/users/query/tiyu/`, {
          card_id: this.$store.state.user.cardID,
          password: this.$store.state.user.password
        })
        .then(response => {
          if (response.data.success === 'ok') {
            this.getData()
            Toast.create('更新成功')
            this.success = true
          }
          this.loading = false
        })
        .catch(err => {
          console.log(err)
          this.loading = false
          Toast.create('更新体育数据失败')
          this.success = false
        })
    }
  }
}
</script>

<style lang="stylus">
</style>
