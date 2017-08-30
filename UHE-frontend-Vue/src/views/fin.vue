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
        <v-tabs-slider class="yellow"></v-tabs-slider>
        <v-tabs-item v-for="i in items" :key="i" :href="'#tab-' + i">
          {{ i }}
        </v-tabs-item>
      </v-tabs-bar>
      <v-tabs-items>
        <v-tabs-content id="tab-缴费情况">
          <v-card flat>
            <!-- <v-card-text> -->
            <v-expansion-panel expand>
              <v-expansion-panel-content v-for="payment in data.paymentcondition">
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
              <!-- <v-expansion-panel>
                      <v-expansion-panel-content v-for="(item,i) in 5" :key="i">
                        <div slot="header">Item</div>
                        <v-card>
                          <v-card-text class="grey lighten-3">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</v-card-text>
                        </v-card>
                      </v-expansion-panel-content>
                    </v-expansion-panel> -->
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
  </div>
</template>

<script>
import { Popup, Cell } from 'mint-ui'
export default {
  components: {
    Popup,
    Cell
  },
  data () {
    return {
      items: ['缴费情况', '缴费记录', '欠缴情况'],
      data: {},
      popup: false,
      detail: null
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
      this.$http.get('/api/fin/')
        .then((response) => {
          this.data = response.data
        })
        .catch((err) => {
          if (err.response.status === 404) {
            this.renewData()
          }
        })
    },
    renewData () {
      this.$http.post('/api/fin/sync', {
        card_id: this.$store.state.user.cardID,
        password: this.$store.state.user.password
      })
        .then((response) => {
          if (response.data.success === 'ok') {
            this.getData()
          }
        })
    }
  }
}
</script>

<style>

</style>
