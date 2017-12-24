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
          | 查看本学期课外活动表（图片）
    q-modal(ref="activitiesTable" :content-css="{minWidth: '80vw', minHeight: '80vh'}")
      q-modal-layout
        q-toolbar(slot="header" color="primary")
          q-btn(color="white" flat @click="close")
            q-icon(name="close")
            q-toolbar-title
              | 课外活动表
        div(v-if="activitiesTableOpen")
          img.responsive(src="/statics/activities_17_2.jpg")
</template>

<script>
import { decrypt } from 'src/libs/utils.js'
import { Dialog } from 'quasar'
export default {
  name: 'sportCard',
  data() {
    return {
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

<style>

</style>
