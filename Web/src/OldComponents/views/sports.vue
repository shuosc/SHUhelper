<template>
  <div>
    <v-card class="my-2">
      <v-card-title>
        晨跑查询
      </v-card-title>
      <v-card-text v-html="data.html">
        {{data.html}}
      </v-card-text>
    </v-card>
    <v-card class="my-2">
      <v-card-title>
        课外活动安排表
      </v-card-title>
      <v-card-text><img src="/static/activities.png" style="object-fit: cover;" alt="lorem" width="100%" /> </v-card-text>
    </v-card>
    <v-card class="my-2">
      <v-card-title>
        一点灵息为你准备了推文：
      </v-card-title>
      <v-card-text>
        <v-container grid-list-lg style="border-style:solid;border-width:2px;border-color:#eee;" class="pa-0 ma-2" @click.stop>
          <v-layout row style="min-height:5rem;">
            <v-flex xs3>
              <v-icon x-large style="height:100%;display:flex;" class="blue--text text--darken-2">public</v-icon>
            </v-flex>
            <v-flex xs9>
              <a href="http://mp.weixin.qq.com/s/Mmvoyrk6kL__UzlPylgsTw" target="_blank" style="text-decoration:none;">
                <p style="font-size:1rem;height:100%;" class="black--text text-xs-left py-2 ma-0">
                  【SHU·一点灵息】 新学期，三个校区一起刷晨跑课外吧<br/>
                  <span style="color:grey;font-size:0.8rem;">mp.weixin.qq.com</span>
                </p>
              </a>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
    </v-card>
    <data-status @renewData="renewData" :status="status"></data-status>
  </div>
</template>

<script>
// import CryptoJS from '../libs/encryption.js'
import dataStatus from '@/components/dataStatus'
import { decrypt } from '@/libs/utils.js'
import { Popup, Cell } from 'mint-ui'
export default {
  components: {
    Popup,
    Cell,
    dataStatus
  },
  data () {
    return {
      passwordVisiable: false,
      data: { html: '' },
      popup: false,
      detail: null,
      phypassword: '',
      status: {
        lastModified: null,
        status: 'loading',
        remark: '信息来自上海大学体育学院'
      }
    }
  },
  created () {
    this.getData()
  },
  methods: {
    onDetailClick (detail) {
      this.detail = detail
      this.popup = true
    },
    getData () {
      this.$http.get(`/api/v1/users/${this.$store.state.user.cardID}/data/tiyu/`)
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
    renewData () {
      this.status.status = 'loading'
      this.$http.post(`/api/v1/users/${this.$store.state.user.cardID}/data/tiyu/`, {
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
