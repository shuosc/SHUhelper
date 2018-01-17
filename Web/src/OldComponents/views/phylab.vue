<template>
  <div>
    <v-card>
      <!-- <v-card-title>学生信息</v-card-title> -->
      <v-card-text v-html="data.html">
      </v-card-text>
    </v-card>
    <popup v-model="popup" popup-transition="popup-fade" persistent>
      <v-card style="width:300px;">
        <v-card-text>
          <v-flex xs12>
            <v-text-field label="物理实验查询密码" :append-icon="passwordVisiable ? 'visibility' : 'visibility_off'" :append-icon-cb="() => (passwordVisiable = !passwordVisiable)" :type="passwordVisiable ? 'password' : 'text'" v-model="phypassword" hint="密码每学期重置为学号，若您本学期还没有修改密码，密码是学号，因为很重要所以说两遍再问自杀"></v-text-field>
          </v-flex>
        </v-card-text>
        <v-card-actions>
          <v-btn primary block @click.native="renewData()">查询</v-btn>
        </v-card-actions>
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
      passwordVisiable: false,
      data: { html: '' },
      popup: false,
      detail: null,
      phypassword: '',
      status: {
        lastModified: null,
        status: 'loading',
        remark: '信息来自上海大学物理教学网站'
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
      this.$http.get('/api/v1/phylab/')
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
      if (this.phypassword === '') {
        this.popup = true
        return
      } else {
        this.popup = false
      }
      this.status.status = 'loading'
      this.$http.post('/api/v1/phylab/sync', {
        card_id: this.$store.state.user.cardID,
        phypassword: this.phypassword,
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
div {
  background-color: #2da5f5
}
</style>
