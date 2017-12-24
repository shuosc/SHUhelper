<template lang="pug">
  div
    q-card.namecard
      q-card-title(style="margin: 0;padding: 0")
        q-icon(slot="right" name="refresh" @click="this.renewData")
        q-icon(slot="right" name="info" @click="dialog.handler()")
      q-card-main
        q-list(class="no-border")
          q-item
            q-item-side
              q-icon(color='primary', name='fa-tiyujiankang', style='font-size:2rem;')
            q-item-main
              q-item-tile(label='') 晨跑:{{this.data.sport}}/5 &nbsp 课外活动:{{this.data.act}}/5 
              q-item-tile(label='') 免晨跑:{{this.data.sport_reduce}} &nbsp 免课外:{{this.data.act_reduce}}
              q-item-tile(sublabel='' ) 晨跑辛苦啦(´▽｀)
          q-item(v-if="this.data.sport<=5")
            q-item-main
               q-progress(:percentage='(this.data.sport + this.data.act + this.data.sport_reduce + this.data.act_reduce)/10',color='teal-4')
      q-card-separator
      q-card-actions
        q-btn.full-width(flat @click="open()")
          | 查看本学期课外活动表<del>（图片）</del>
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
              Card  筛选
            </q-card-title>
            <div class="rlayout-padding row justify-center">
            <div class="row" style="width: 500px; max-width: 90vw;">
              <q-checkbox class="col-6" v-for="sport in sports" v-model="sportFilter" :label='sport.name' :val='sport.val' :key="sport.val" />
            </div>
          </div>
          </q-card>
          <q-card v-for="sport in sportsFiltered" :key="sport.val" >
            <q-card-title>
              Card  {{sport.name}}  @{{sport.place}}
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
import { decrypt } from 'src/libs/utils.js'
import { Dialog } from 'quasar'
export default {
  name: 'sportCard',
  data() {
    return {
<<<<<<< HEAD
      dialog: {
        label: '数据异常',
        icon: 'warning',
        handler() {
          Dialog.create({
            title: '数据异常',
            message: '如果数据异常是体育学院的锅，我们也不造为啥(￣∇￣)'
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
        run: 2,
        act: 3
      },
      popup: false,
      detail: null,
      phypassword: '',
      status: {
        lastModified: null,
        status: 'loading',
        remark: '信息来自上海大学体育学院'},
      activitiesTableOpen: false
    }
  },
  created() {
    // this.renewData()
    this.getTime()
    this.getData()
=======
      activitiesTableOpen: false,
      sportFilter: [],
      sportsFiltered: [],
      sports: [
        {
          name: '篮球/荷式篮球',
          val: 'basketball',
          place: 'C区风雨操场',
          items: [
            {
              day: '周一',
              teacher: '胡吉/刘娜',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '孙岩/张秀萍/许汸',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '魏磊',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '秦文宏/吕彪',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '沈何为',
              time: '15:00 - 16:30'
            }
          ]
        },
        {
          name: '排球',
          val: 'baseball',
          place: 'C区风雨操场',
          items: [
            {
              day: '周一',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '居蔚青',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '朱宝祥',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '魏轶林',
              time: '15:00 - 16:30'
            }
          ]
        },
        {
          name: '男生足球',
          val: 'football',
          place: 'J区足球场',
          items: [
            {
              day: '周一',
              teacher: '沈强',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '王长琦',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '益广仁',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '王文胜',
              time: '15:00 - 16:30'
            }
          ]
        },
        {
          name: '羽毛球',
          val: 'badminton',
          place: '体育馆内场',
          items: [
            {
              day: '周一',
              teacher: '柏慧敏/王江宇',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '柴承军/柏慧敏',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '卢高峰/柴承军',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '曾朝恭/徐英姿',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '许凤/徐英姿',
              time: '13:30 - 15:00'
            }
          ]
        },
        {
          name: '乒乓球',
          val: 'pingpong',
          place: '训练馆乒乓房',
          items: [
            {
              day: '周一',
              teacher: '庄琰',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '贺晓明',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '王旨明',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '张轶',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '林威力',
              time: '15:00 - 16:30'
            }
          ]
        },
        {
          name: '女生操舞类',
          val: 'dancing',
          place: '训练馆X107',
          items: [
            {
              day: '周一',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '俞华',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '时静',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '孙婷婷',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            }
          ]
        },
        {
          name: '女生养生普拉提',
          val: 'yoga',
          place: '训练馆X106',
          items: [
            {
              day: '周一',
              teacher: '周艳',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '张靖',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            }
          ]
        },
        {
          name: '游泳达标测试',
          val: 'swimmingTest',
          place: '游泳馆',
          items: [
            {
              day: '周一',
              teacher: '林仪煌/卢琳/陈爱鞠',
              time: '15:45 - 16:30'
            },
            {
              day: '周二',
              teacher: '尹默林/刘超云',
              time: '15:45 - 16:30'
            },
            {
              day: '周三',
              teacher: '王永/陈婷/林仪煌',
              time: '15:45 - 16:30'
            },
            {
              day: '周四',
              teacher: '陈婷/刘超云/王永/尹默林',
              time: '15:45 - 16:30'
            },
            {
              day: '周五',
              teacher: '卢琳/陈爱鞠',
              time: '13:30 - 14:15'
            }
          ]
        },
        {
          name: '游泳',
          val: 'swimming',
          place: '游泳馆',
          items: [
            {
              day: '周一',
              teacher: '林仪煌/卢琳/陈爱鞠',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '尹默林/刘超云',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '王永/陈婷/林仪煌',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '陈婷/刘超云/王永/尹默林',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '卢琳/陈爱鞠',
              time: '13:30 - 15:00'
            }
          ]
        },
        {
          name: '武术',
          val: 'gongfu',
          place: '训练馆2楼',
          items: [
            {
              day: '周一',
              teacher: '申亮/梁志雄',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '王光/李效凯',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '孙敏',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '徐春毅',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            }
          ]
        },
        {
          name: '旱地冰球',
          val: 'iceball',
          place: '训练馆2楼',
          items: [
            {
              day: '周一',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '唐冬菊',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            }
          ]
        },
        {
          name: '跆拳道',
          val: 'taewondo',
          place: '体育馆2楼南侧',
          items: [
            {
              day: '周一',
              teacher: '林大参',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '陈琳',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            }
          ]
        },
        {
          name: '击剑',
          val: 'sword',
          place: '体育馆2楼北侧',
          items: [
            {
              day: '周一',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '徐漫云',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '周珏',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            }
          ]
        },
        {
          name: '攀岩',
          val: 'climb',
          place: 'C区攀岩墙',
          items: [
            {
              day: '周一',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '何颖强',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '陈利荣',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            }
          ]
        },
        {
          name: '高尔夫球',
          val: 'golf',
          place: 'J区南侧',
          items: [
            {
              day: '周一',
              teacher: '邵斌',
              time: '15:45 - 17:15'
            },
            {
              day: '周二',
              teacher: '黄军海',
              time: '15:45 - 17:15'
            },
            {
              day: '周三',
              teacher: '沙俊波',
              time: '15:45 - 17:15'
            },
            {
              day: '周四',
              teacher: '郭平',
              time: '15:45 - 17:15'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 17:15'
            }
          ]
        },
        {
          name: '跑步（嘉定）',
          val: 'runningJiaDing',
          place: '田径场南侧',
          items: [
            {
              day: '周一',
              teacher: '王伟忠/张耘/许凤',
              time: '15:45 - 16:45'
            },
            {
              day: '周二',
              teacher: '陆英浩/张玲芳',
              time: '15:45 - 16:45'
            },
            {
              day: '周三',
              teacher: '刘春辉/陆志超',
              time: '15:45 - 16:45'
            },
            {
              day: '周四',
              teacher: '闵伟',
              time: '15:45 - 16:45'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 16:45'
            }
          ]
        },
        {
          name: '跑步（延长）',
          val: 'runningYanChang',
          place: '田径场北侧',
          items: [
            {
              day: '周一',
              teacher: '林建华',
              time: '15:45 - 16:45'
            },
            {
              day: '周二',
              teacher: '陶涛',
              time: '15:45 - 16:45'
            },
            {
              day: '周三',
              teacher: '自己玩',
              time: '15:45 - 16:45'
            },
            {
              day: '周四',
              teacher: '谢秀雯',
              time: '15:45 - 16:45'
            },
            {
              day: '周五',
              teacher: '自己玩',
              time: '15:45 - 16:45'
            }
          ]
        }
      ]
    }
  },
  computed: {
  },
  watch: {
    sportFilter: function(val) {
      if (val.length === 0) {
        this.sportsFiltered = this.sports
        return
      }
      this.sportsFiltered = []
      this.sportFilter.forEach((item) => {
        this.sports.forEach((s) => {
          if (s.val === item) {
            this.sportsFiltered.push(s)
          }
        })
      })
    }
  },
  created() {
    this.sportsFiltered = this.sports
>>>>>>> ee981f1fb140f816276294344a9231b031b5c2d3
  },
  methods: {
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
      this.$refs.activitiesTable.open()
    },
    close() {
      this.activitiesTableOpen = false
      this.$refs.activitiesTable.close()
    },
    getData() {
      this.$http.get(`/api/users/query/tiyu/`)
        .then((response) => {
          this.status.status = response.data.status
          this.status.time = response.data.last_modified.$date
          this.data = decrypt(response.data.data, this.$store.state.user.password)
          console.log(this.data)
        })
        .catch((err) => {
          console.log(err)
          if (err.response.status === 404) {
            this.renewData()
          }
        })
    },
    renewData() {
      this.status.status = 'loading'
      this.$http.post(`/api/users/query/tiyu/`, {
        card_id: this.$store.state.user.cardID,
        password: this.$store.state.user.password
      })
        .then((response) => {
          if (response.data.success === 'ok') {
            this.getData()
            this.$store.commit('showSnackbar', { text: '更新成功' })
          }
        })
        .catch((err) => {
          console.log(err)
          this.getData()
        })
    }
  }
}
</script>

<style lang="stylus">

</style>
