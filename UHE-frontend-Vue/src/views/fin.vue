<template>
  <div>
    <v-card>
      <!-- <v-card-title>学生信息</v-card-title> -->
      <v-card-text>
        <v-layout row wrap>
          <v-flex xs3> 姓名</v-flex>
          <v-flex xs3>{{data.name}}</v-flex>
          <v-flex xs3>证件</v-flex>
          <v-flex xs3>{{data.ID_type}}</v-flex>
          <v-flex xs3> 证件号</v-flex>
          <v-flex xs9>{{data.ID}}</v-flex>
          <v-flex xs3> 欠缴金额</v-flex>
          <v-flex xs4>{{data.arrearageAmount}}</v-flex>
        </v-layout>
      </v-card-text>
    </v-card>
    <v-tabs light fixed centered>
      <v-tabs-bar class="white">
        <v-tabs-slider class="blue"></v-tabs-slider>
        <v-tabs-item v-for="i in items" :key="i" :href="'#tab-' + i">
          {{ i }}
        </v-tabs-item>
      </v-tabs-bar>
      <v-tabs-items>
        <v-tabs-content id="tab-缴费情况">
          <v-card flat>
            <!-- <v-card-text> -->
            <v-expansion-panel expand>
              <v-expansion-panel-content v-for="payment in data.paymentcondition" :key="payment.digst[0]">
                <div slot="header">{{payment.digst[0]}}</div>
                <v-card flat>
                  <v-card-text class="white lighten-3">
                    <v-layout row wrap>
                      <v-flex xs3>应收金额 </v-flex>
                      <v-flex xs3>{{payment.digst[1]}}</v-flex>
                      <v-flex xs3>减免金额 </v-flex>
                      <v-flex xs3>{{payment.digst[2]}}</v-flex>
                      <v-flex xs3>缓缴金额 </v-flex>
                      <v-flex xs3>{{payment.digst[3]}}</v-flex>
                      <v-flex xs3>已交费金额 </v-flex>
                      <v-flex xs3>{{payment.digst[4]}}</v-flex>
                      <v-flex xs3>欠费金额 </v-flex>
                      <v-flex xs3>{{payment.digst[5]}}</v-flex>
                      <v-flex xs3>待退金额 </v-flex>
                      <v-flex xs3>{{payment.digst[6]}}</v-flex>
                    </v-layout>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn block @click="onDetailClick(payment.detail)">查看明细</v-btn>
                  </v-card-actions>
                </v-card>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-card>
        </v-tabs-content>
        <v-tabs-content id="tab-缴费记录">
          <v-card flat>
            <v-card-text>
            </v-card-text>
          </v-card>
        </v-tabs-content>
        <v-tabs-content id="tab-欠缴情况">
          <v-card flat>
            <!-- <v-card-text>{11111</v-card-text> -->
          </v-card>
        </v-tabs-content>
      </v-tabs-items>
    </v-tabs>
    <popup v-model="popup" popup-transition="popup-fade">
      <v-card style="width:300px;">
        <v-expansion-panel>
          <v-expansion-panel-content v-for="unit in detail" :key="unit[0]">
            <div slot="header">{{unit[0]}}</div>
            <v-card flat>
              <v-card-text class="white lighten-3">
                <v-layout row wrap>
                  <v-flex xs3>应收金额 </v-flex>
                  <v-flex xs3>{{unit[1]}}</v-flex>
                  <v-flex xs3>减免金额 </v-flex>
                  <v-flex xs3>{{unit[2]}}</v-flex>
                  <v-flex xs3>缓缴金额 </v-flex>
                  <v-flex xs3>{{unit[3]}}</v-flex>
                  <v-flex xs3>已交费金额 </v-flex>
                  <v-flex xs3>{{unit[4]}}</v-flex>
                  <v-flex xs3>欠费金额 </v-flex>
                  <v-flex xs3>{{unit[5]}}</v-flex>
                  <v-flex xs3>待退金额 </v-flex>
                  <v-flex xs3>{{unit[6]}}</v-flex>
                </v-layout>
              </v-card-text>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-card>
    </popup>
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
      items: ['缴费情况', '缴费记录', '欠缴情况'],
      data: {},
      popup: false,
      detail: null,
      status: {
        lastModified: null,
        status: 'loading',
        remark: '信息来自上海大学财务处新版网站'
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
      this.$http.get('/api/v1/fin/')
        .then((response) => {
          this.status.status = response.data.status
          this.status.time = response.data.last_modified.$date
          this.data = decrypt(response.data.data, this.$store.state.user.password)
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
      this.$http.post('/api/v1/fin/sync', {
        card_id: this.$store.state.user.cardID,
        password: this.$store.state.user.password
      })
        .then((response) => {
          if (response.data.success === 'ok') {
            this.getData()
            this.$store.commit('showSnackbar', { text: '更新成功' })
          }
        })
        .catch((err)=>{
          console.log(err)
          this.getData()
        })
    }
  }
}
</script>

<style>

</style>
