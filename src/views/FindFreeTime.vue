<template>
  <div>
    <group title="查询信息">
      <x-input title="小组代码"
               placeholder=""
               v-model="code"></x-input>
      <selector title="周数"
                :options="[1,2,3,4,5,6,7,8,9,10]"
                v-model="week"></selector>
      <cell title="选课更新日期"
            :value="data.date"></cell>
    </group>
          <x-button v-if="!record"
                type="primary"
                style="margin-top:10px;"
                @click.native="find()">开始寻找</x-button>
      <x-button v-if="record"
                type="primary"
                style="margin-top:10px;"
                @click.native="answer()">更新结果</x-button>
    <divider v-if="!record">课表</divider>
    <divider v-if="record">小组公共时间表 {{count}}人已录入</divider>
    <div v-if="!record"
         style="font-size:0.8rem;"
         v-html="data.content"></div>
    <div v-if="result!=''"
         style="font-size:0.8rem;">
      <table style="width:100%;text-align:center;">
      <tr>
          <th v-for="i in 5">{{i}}</th>
        </tr>
        <tr v-for="j in 13">
          <td v-for="i in 5"><div v-if="result[j-1][i-1]">{{result[j-1][i-1]}}</div><div v-if="!result[j-1][i-1]"  style="background-color:green">{{result[j-1][i-1]}}</div></td>
        </tr>
      </table>
    </div>
  
    <popup v-model="showCaptcha"
           is-transparent
           height="270px">
      <div class="popup">
        <group label-width="4em"
               label-margin-right="2em"
               label-align="right">
          <x-input title="验证码"
                   v-model="captcha"><img slot="label"
                 :src="'data:image/gif;base64,' + captcha_img" /></x-input>
        </group>
        <group label-width="4em"
               label-margin-right="2em"
               label-align="right">
          <x-button type="primary"
                    @click.native="postUpdate()">确认</x-button>
        </group>
      </div>
    </popup>
  </div>
</template>

<script>
import { numberPad, Divider, Group, Cell, XButton, Popup, XInput, Selector } from 'vux'
import CryptoJS from '../libs/encryption.js'
export default {
  components: {
    XInput,
    Popup,
    Divider,
    Group,
    Cell,
    XButton,
    Selector
  },
  data() {
    return {
      record: false,
      content: '',
      result: '',
      data: {
        site: '',
        subject: '',
        content: '',
        date: ''
      },
      captcha_img: '',
      captcha: '',
      showCaptcha: false,
      week: null,
      code: null
    }
  },
  created: function () {
    this.getData()
  },
  computed: {
  },
  methods: {
    getData() {
      this.$vux.loading.show({
        text: '少女祈祷中...'
      })
      var _this = this
      this.$http.get('/api/queries/xk')
        .then((response) => {
          this.$vux.loading.hide()
          if (response.data.success) {
            if (response.data.status === 'no records') {
              _this.$vux.alert.show({
                title: '状态',
                content: '数据库中没有查询记录，请点击更新数据'
              })
              this.updateData()
            } else {
              var date = new Date(response.data.date * 1000)
              var decrypted = CryptoJS.AES.decrypt(response.data.content, _this.$store.state.account.password)
              _this.data.content = decrypted.toString(CryptoJS.enc.Utf8)
              _this.data.site = response.data.site
              _this.data.subject = response.data.subject
              _this.data.date = date.getMonth() + '/' + date.getDate() + ' ' + numberPad(date.getHours(), 2) + ':' + numberPad(date.getMinutes(), 2)
              _this.$vux.toast.show({
                position: 'bottom',
                type: 'text',
                text: '读取成功'
              })
            }
          } else {
            _this.$vux.alert.show({
              title: '状态',
              content: '请先登录',
              onHide() {
                _this.$router.replace('/')
              }
            })
          }
        })
        .catch(function (response) {
          _this.$vux.loading.hide()
          _this.$vux.alert.show({
            title: '提示',
            content: '错误，我也不知道怎么回事，但是你可能是没有完成教学评估',
            onShow() {
            },
            onHide() {
              _this.$router.replace('/')
            }
          })
        })
    },
    updateData() {
      var _this = this
      if (this.$store.state.account.card_id === '') {
        this.$vux.alert.show({
          title: '状态',
          content: '请先登录',
          onHide() {
            _this.$router.replace('/')
          }
        })
      }
      this.$vux.loading.show({
        text: '少女祈祷中...'
      })
      _this.prepareUpdate()
    },
    prepareUpdate() {
      var _this = this
      this.$http.get('/api/queries/xk/refresh')
        .then((response) => {
          this.$vux.loading.hide()
          if (response.data.success) {
            _this.captcha_img = response.data.captcha_img
            _this.postUpdate()
          } else {
            _this.$vux.alert.show({
              title: '状态',
              content: '准备查询失败，服务器故障'
            })
          }
        })
    },
    saveToServer() {
      var _this = this
      this.$http.post('/api/queries/xk/save', {
        data: CryptoJS.AES.encrypt(this.data.content, _this.$store.state.account.password).toString(),
        site: this.$route.params.name
      })
        .then((response) => {
          if (response.data.success) {
            _this.$vux.toast.show({
              position: 'bottom',
              type: 'text',
              text: '保存成功'
            })
          }
        })
    },
    find() {
      if (this.code == null || this.week == null) {
        this.$vux.toast.show({
          position: 'bottom',
          type: 'text',
          text: '请输入小组代号和聚会的周数'
        })
        return
      }
      this.$vux.loading.show({
        text: '少女祈祷中...'
      })
      this.$http.post('/api/findfreetime', {
        schedule: this.data.content,
        week: this.week,
        code: this.code
      }).then((response) => {
        if (response.data.success) {
          this.$vux.toast.show({
            position: 'bottom',
            type: 'text',
            text: '您的课表已成功录入，请点击更新结果查看结果'
          })
          this.$vux.loading.hide()
          this.record = true
          this.answer()
        }
      })
    },
    answer() {
      this.$vux.loading.show({
        text: '少女祈祷中...'
      })
      this.$http.get('/api/findfreetime?code=' + this.code)
        .then((response) => {
          if (response.data.success) {
            this.result = response.data.answer
            this.count = response.data.count
          }
          this.$vux.loading.hide()
        })
    },
    postUpdate() {
      var _this = this
      this.$vux.loading.show({
        text: '少女祈祷中...'
      })
      if (this.captcha_img !== '' && this.captcha === '') {
        this.showCaptcha = true
        _this.$vux.loading.hide()
        return
      }
      this.$http.post('/api/queries/xk/refresh', {
        'card_id': this.$store.state.account.card_id,
        'password': this.$store.state.account.password,
        'captcha': this.captcha
      })
        .then((response) => {
          _this.$vux.loading.hide()
          _this.showCaptcha = false
          if (response.data.success) {
            _this.data.content = response.data.content.data
            _this.saveToServer()
          } else {
            _this.$vux.alert.show({
              title: '状态',
              content: '查询失败'
            })
          }
        })
        .catch(function (response) {
          _this.$vux.loading.hide()
          _this.$vux.alert.show({
            title: '提示',
            content: '错误，我也不知道怎么回事，但是你可能是没有完成教学评估 http://cj.shu.edu.cn/',
            onShow() {
            },
            onHide() {
              _this.$router.replace('/')
            }
          })
        })
    }
  }
}
</script>

<style>

</style>
