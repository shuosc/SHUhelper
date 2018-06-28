<template lang='pug'>
  div(class='container')
    div.card
      div.card-title.line
        p 概览
      div.card-content(style='padding: 20px;margin-bottom: 20px;')
        // mpvue的checkbox的值有问题
        // div(class='row' style='width: 100%;font-size:14px;')
        //   div.col-6(v-for='sport in sports' v-model='sportFilter' :label='sport.name' :val='sport.val' :key='sport.val')
        //     input(type='checkbox' v-model='sportFilter' :value='sport.name')
        //     label {{ sport.name }}
        // 微信原生checkbox
        // checkbox-group(bindchange="sportFiter")
        //   label(class="checkbox" wx:for="{{sports}}")
        //     checkbox(value="{{sport.name}}" checked="{{sport.checked}}") {{ sport.name }}
        div.row(v-for='(sport,i) in sports'  :key='sport.val')
          span.name.col-6 {{ sport.name }} 
          span.place.col-6 
            <img src='/static/place.png' style="width:12px;height:12px"> {{ sport.place }}

          
    div.card(v-for='(sport,i) in sports'  :key='sport.val')
      div.card-title.line
        p {{ sport.name }}  @{{ sport.place }}
      div.card-content( v-for='(item,j) in sport.items' :key='item.day')
        div.list
          div.list-title {{ item.teacher }}
          div.list-content {{ item.day }}  {{ item.time }}
        
          

</template>
<script>

export default {
  name: 'sportCard',
  data() {
    return {
      sportFilter: [],
      sports: [
        {
          'name': '篮球/荷式篮球',
          'val': 'basketball',
          'place': 'C区风雨操场',
          'items': [
            {
              'day': '周一',
              'teacher': '胡吉/刘娜',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '孙岩/张秀萍/许汸',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '魏磊',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '秦文宏/吕彪',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '沈何为',
              'time': '15:00 - 16:30'
            }
          ]
        },
        {
          'name': '排球',
          'val': 'baseball',
          'place': 'C区风雨操场',
          'items': [
            {
              'day': '周一',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '居蔚青',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '朱宝祥',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '魏轶林',
              'time': '15:00 - 16:30'
            }
          ]
        },
        {
          'name': '男生足球',
          'val': 'football',
          'place': 'J区足球场',
          'items': [
            {
              'day': '周一',
              'teacher': '沈强',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '王长琦',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '益广仁',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '王文胜',
              'time': '15:00 - 16:30'
            }
          ]
        },
        {
          'name': '羽毛球',
          'val': 'badminton',
          'place': '体育馆内场',
          'items': [
            {
              'day': '周一',
              'teacher': '柏慧敏/王江宇',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '柴承军/柏慧敏',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '卢高峰/柴承军',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '曾朝恭/徐英姿',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '许凤/徐英姿',
              'time': '13:30 - 15:00'
            }
          ]
        },
        {
          'name': '乒乓球',
          'val': 'pingpong',
          'place': '训练馆乒乓房',
          'items': [
            {
              'day': '周一',
              'teacher': '庄琰',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '贺晓明',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '王旨明',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '张轶',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '林威力',
              'time': '15:00 - 16:30'
            }
          ]
        },
        {
          'name': '女生操舞类',
          'val': 'dancing',
          'place': '训练馆X107',
          'items': [
            {
              'day': '周一',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '俞华',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '时静',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '孙婷婷',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            }
          ]
        },
        {
          'name': '女生养生普拉提',
          'val': 'yoga',
          'place': '训练馆X106',
          'items': [
            {
              'day': '周一',
              'teacher': '周艳',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '张靖',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            }
          ]
        },
        {
          'name': '游泳达标测试',
          'val': 'swimmingTest',
          'place': '游泳馆',
          'items': [
            {
              'day': '周一',
              'teacher': '林仪煌/卢琳/陈爱鞠',
              'time': '15:45 - 16:30'
            },
            {
              'day': '周二',
              'teacher': '尹默林/刘超云',
              'time': '15:45 - 16:30'
            },
            {
              'day': '周三',
              'teacher': '王永/陈婷/林仪煌',
              'time': '15:45 - 16:30'
            },
            {
              'day': '周四',
              'teacher': '陈婷/刘超云/王永/尹默林',
              'time': '15:45 - 16:30'
            },
            {
              'day': '周五',
              'teacher': '卢琳/陈爱鞠',
              'time': '13:30 - 14:15'
            }
          ]
        },
        {
          'name': '游泳',
          'val': 'swimming',
          'place': '游泳馆',
          'items': [
            {
              'day': '周一',
              'teacher': '林仪煌/卢琳/陈爱鞠',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '尹默林/刘超云',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '王永/陈婷/林仪煌',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '陈婷/刘超云/王永/尹默林',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '卢琳/陈爱鞠',
              'time': '13:30 - 15:00'
            }
          ]
        },
        {
          'name': '武术',
          'val': 'gongfu',
          'place': '训练馆2楼',
          'items': [
            {
              'day': '周一',
              'teacher': '申亮/梁志雄',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '王光/李效凯',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '孙敏',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '徐春毅',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            }
          ]
        },
        {
          'name': '旱地冰球',
          'val': 'iceball',
          'place': '训练馆2楼',
          'items': [
            {
              'day': '周一',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '唐冬菊',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            }
          ]
        },
        {
          'name': '跆拳道',
          'val': 'taewondo',
          'place': '体育馆2楼南侧',
          'items': [
            {
              'day': '周一',
              'teacher': '林大参',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '陈琳',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            }
          ]
        },
        {
          'name': '击剑',
          'val': 'sword',
          'place': '体育馆2楼北侧',
          'items': [
            {
              'day': '周一',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '徐漫云',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '周珏',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            }
          ]
        },
        {
          'name': '攀岩',
          'val': 'climb',
          'place': 'C区攀岩墙',
          'items': [
            {
              'day': '周一',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '何颖强',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '陈利荣',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            }
          ]
        },
        {
          'name': '高尔夫球',
          'val': 'golf',
          'place': 'J区南侧',
          'items': [
            {
              'day': '周一',
              'teacher': '邵斌',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周二',
              'teacher': '黄军海',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周三',
              'teacher': '沙俊波',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周四',
              'teacher': '郭平',
              'time': '15:45 - 17:15'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 17:15'
            }
          ]
        },
        {
          'name': '跑步（嘉定）',
          'val': 'runningJiaDing',
          'place': '田径场南侧',
          'items': [
            {
              'day': '周一',
              'teacher': '王伟忠/张耘/许凤',
              'time': '15:45 - 16:45'
            },
            {
              'day': '周二',
              'teacher': '陆英浩/张玲芳',
              'time': '15:45 - 16:45'
            },
            {
              'day': '周三',
              'teacher': '刘春辉/陆志超',
              'time': '15:45 - 16:45'
            },
            {
              'day': '周四',
              'teacher': '闵伟',
              'time': '15:45 - 16:45'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 16:45'
            }
          ]
        },
        {
          'name': '跑步（延长）',
          'val': 'runningYanChang',
          'place': '田径场北侧',
          'items': [
            {
              'day': '周一',
              'teacher': '林建华',
              'time': '15:45 - 16:45'
            },
            {
              'day': '周二',
              'teacher': '陶涛',
              'time': '15:45 - 16:45'
            },
            {
              'day': '周三',
              'teacher': '自己玩',
              'time': '15:45 - 16:45'
            },
            {
              'day': '周四',
              'teacher': '谢秀雯',
              'time': '15:45 - 16:45'
            },
            {
              'day': '周五',
              'teacher': '自己玩',
              'time': '15:45 - 16:45'
            }
          ]
        }
      ]
    }
  },
  created() {
    console.log(2)
    this.getSportSchedule()
  },
  computed: {
    sportsFiltered: function() {
      console.log('233333')
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
        console.log('hhhh')
        return
      }
      this.$http.get('/static/sports_17_winter.json', {}, {
        baseURL: ''
      }).then(response => {
        // this.sports.push(response.data)
        console.log(response)
      })
      .catch(e => {
        console.log(e)
      })
    }
  }
}
</script>
<style scoped>
.container {
  /* padding: 10px; */
  /* padding-right: 10px; */
  min-height: 100vh;
  /* padding-bottom: 10px; */
  /* padding-top: 10px; */
  box-sizing: border-box;
  background: #fff;
}
.card {
  padding: 0;
  margin: 10px;
  box-sizing: border-box;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 2px 0 rgba(0,0,0,0.16), 0 0 0 1px rgba(0,0,0,0.08);
} 
.card-title {
  font-size: 16px;
  padding: 15px 20px 15px 20px;
}
.card-content {
  padding: 0px;
}
.shadow {
  box-shadow: 0 2px 2px 0 rgba(0,0,0,0.16), 0 0 0 1px rgba(0,0,0,0.08);
}
.line {
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.checkbox {
  width: 10px;
}
.list {
  padding: 15px 20px 15px 20px;
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.list-title {
  font-size: 14px;
}
.list-content {
  font-size: 14px;
  color: rgba(0,0,0,0.5);
}
.name {
  font-size: 14px;
}
.place {
  font-size: 14px;
  color: #4c4c4c;
}
</style>

