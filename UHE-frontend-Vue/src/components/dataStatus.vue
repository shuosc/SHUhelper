<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" lazy absolute>
      <v-btn absolute bottom right fab style="bottom:70px;" slot="activator" :class="{'accent':status.status === 'failed','primary':status.status === 'success'}">
        <v-progress-circular indeterminate class="amber--text" v-if="status.status === 'loading'"></v-progress-circular>
        <v-icon v-else>info</v-icon>
      </v-btn>
      <v-card>
        <v-card-text>
          <v-layout row wrap>
            <v-flex xs4>
              <h5>数据状态</h5>
            </v-flex>
            <v-flex xs8> {{status.status|statusText}}</v-flex>
            <v-divider></v-divider>
            <v-flex xs4>
              <h5>更新时间</h5>
            </v-flex>
            <v-flex xs8> {{new Date(status.time - 8*3600*1000)|moment("from")}}</v-flex>
            <v-divider></v-divider>
            <v-flex xs4>
              <h5>数据备注</h5>
            </v-flex>
            <v-flex xs8>{{status.remark}}</v-flex>
            <v-divider></v-divider>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-btn class="primary" flat @click.native="onRenewClick" block>更新数据</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
import { Cell } from 'mint-ui'
const statusMap = {
  'success': '更新成功',
  'loading': '更新中',
  'pending': '更新中',
  'failed': '更新失败',
  'expired': '已过期'
}
export default {
  components: {
    Cell
  },
  props: ['status'],
  data () {
    return {
      dialog: false
    }
  },
  filters: {
    statusText: function (status) {
      return statusMap[status]
    }
  },
  methods: {
    onRenewClick () {
      this.$emit('renewData')
      this.dialog = false
      console.log(this.status)
      // this.$store.commit('showSnackbar', { text: '开始更新数据' })
    }
  }
}
</script>

<style scope>
h5 {
  font-size: 1.2rem;
}
</style>
