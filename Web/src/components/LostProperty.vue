<template lang="pug">
  div
    q-card(v-if='select=="wanted"' v-for="item in Finditems" :key='index')
      q-card-media
        q-parallax(:src="item.img" :height="150")
      q-card-separator
      q-collapsible(:label='item.name' :sublabel='item.time')
        q-list(no-border)
          q-item
            q-item-side(icon='room')
            q-item-main 
              | {{item.place}} 
          q-item
            q-item-side(icon='report')
            q-item-main 
              | {{item.detail}} 
          q-item
            q-item-side(icon='account_box')
            q-item-main 
              | {{item.person.name}} 
          q-item
            q-item-side(icon='call')
            q-item-main
             | {{item.person.contact}}
          q-btn-inner(v-if='item.status==1' class='full-width text-black row col flex-center' disabled )
            | 已归还
          q-btn-inner(v-else class='full-width text-black row col flex-center' disabled)
            | 未归还
    q-card(v-if='select=="find"' v-for="item in Lostitems" :key='index' )
      q-card-media
        q-parallax(:src="item.img" :height="150")
      q-card-separator
      q-collapsible(:label='item.name' :sublabel='item.time')
        q-list(no-border)
          q-item
            q-item-side(icon='room')
            q-item-main 
              | {{item.place}} 
          q-item
            q-item-side(icon='report')
            q-item-main 
              | {{item.detail}} 
          q-item
            q-item-side(icon='account_box')
            q-item-main 
              | {{item.person.name}} 
          q-item
            q-item-side(icon='call')
            q-item-main
             | {{item.person.contact}}
          q-btn-inner(v-if='item.status==1' class='full-width text-black row col flex-center' disabled )
            | 已归还
          q-btn-inner(v-else class='full-width text-black row col flex-center' disabled)
            | 未归还
    q-modal(v-model='add' minimized  :content-css="{minWidth: '80vw'}")
      q-card(flat)
        //q-card-title
         | 新增失物招领信息
        //q-card-separator
        q-card-main
          q-select(v-model='model' :options='options')  
          q-field(label="填写个人信息" icon="person")
            q-input(v-model='ItemInformations.name'  float-label="姓名")
            q-input(v-model='ItemInformations.contact'  float-label="电话")
      q-card(flat)
        q-card-main
          q-field(label="填写物品信息" icon="card_giftcard")
            q-input(v-model='ItemInformations.item'  float-label="物品名称")
            q-datetime(v-model="ItemInformations.time" float-label="失物/拾物时间")
            q-input(v-model='ItemInformations.place'  float-label="失物/拾物地点")
            q-input(v-model='ItemInformations.detail' float-label="详情" :min-rows='2' type='textarea')



    div(slot="footer")
      q-tabs(align="justify")
        q-tab(slot='title' icon='pan_tool' label='招领' @click="OnClick('wanted')")
        q-tab(slot='title' icon='add_circle' label='新增信息' @click="OnClick('add')")
        q-tab(slot='title' icon='live_help' label='寻物' @click="OnClick('find')")

        
</template>

<script>
import { QTabs, QTab, QCollapsible, QDatetime, QInput, QParallax } from 'quasar'
export default {
  components: {
    QInput,
    QDatetime,
    QParallax,
    QTabs,
    QCollapsible,
    QTab
  },
  data() {
    return {
      ItemInformations: {
        name: '',
        item: '',
        place: '',
        detail: '',
        img: '',
        contact: '',
        time: ''
      },
      model: 'lost',
      select: 'wanted',
      add: false,
      options: [{
        label: '失物挂失',
        value: 'lost'
      },
      {
        label: '拾物招领',
        value: 'find'
      }],
      Lostitems: [{
        'name': '学生卡',
        'time': '2018.1.2',
        'place': '新世纪',
        'detail': '新世纪保安亭领取',
        'img': '/statics/course-back.jpg',
        'status': '0',
        'person': {
          'name': 'zyq',
          'contact': '假装有的手机号'
        }
      },
      {
        'name': '8G内存条',
        'time': '2018.2.2',
        'place': '东区计算机大楼',
        'detail': '被私吞了',
        'img': '/statics/course-back.jpg',
        'status': '1',
        'person': {
          'name': 'zmy',
          'contact': '假装有的手机号'
        }
      }],
      Finditems: [{
        'name': '学生卡',
        'time': '2018.1.2',
        'place': '新世纪',
        'detail': '新世纪保安亭领取',
        'img': '/statics/course-back.jpg',
        'status': '0',
        'person': {
          'name': 'zyq',
          'contact': '假装有的手机号'
        }
      },
      {
        'name': '16G内存条',
        'time': '2018.2.2',
        'place': '东区计算机大楼',
        'detail': '被私吞了',
        'img': '/statics/course-back.jpg',
        'status': '1',
        'person': {
          'name': 'zmy',
          'contact': '假装有的手机号'
        }
      }]
    }
  },
  methods: {
    OnClick(name) {
      if (name==="add")
        this.add = true
      else if (name==="wanted")
        this.select = 'wanted'
      else 
        this.select = 'find'
    }
  }
}
</script>    