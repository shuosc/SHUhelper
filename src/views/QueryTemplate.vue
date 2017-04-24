<template>
  <div>
    <group title="查询信息">
      <cell title="信息名" :value="$route.params.name"></cell>
      <cell title="来源网站" :value="$route.params.name"></cell>
      <cell title="上次更新日期" :value="data.date"></cell>
      <x-button type="primary" style="margin-top:10px;" @click.native="updateData()">更新数据</x-button>
    </group>
    <divider>数据库中的信息</divider>
    <div style="font-size:0.8rem;" v-html="data.content"></div>
    <popup v-model="showCaptcha" is-transparent height="270px">
      <div class="popup">
        <group label-width="4em" label-margin-right="2em" label-align="right">
          <x-input title="验证码" v-model="captcha"><img slot="label" :src="'data:image/gif;base64,' + captcha_img" /></x-input>
        </group>
        <group label-width="4em" label-margin-right="2em" label-align="right">
          <x-button type="primary" @click.native="postUpdate()">确认</x-button>
        </group>
      </div>
    </popup>
  </div>
</template>

<script>
import { numberPad, XHeader, ViewBox, Divider, Group, Cell, XButton, Popup, XInput } from 'vux'
import CryptoJS from '../libs/encryption.js'
export default {
  components: {
    XHeader,
    ViewBox,
    XInput,
    Popup,
    Divider,
    Group,
    Cell,
    XButton
  },
  data() {
    return {
      content: '',
      data: {
        site: '',
        subject: '',
        content: '',
        date: ''
      },
      captcha_img: '',
      captcha: '',
      showCaptcha: false
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
      this.$http.get('/api/queries/' + this.$route.params.name)
        .then((response) => {
          this.$vux.loading.hide()
          if (response.data.success) {
            if (response.data.status === 'no records') {
              _this.$vux.alert.show({
                title: '状态',
                content: '数据库中没有查询记录，请点击更新数据'
              })
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
        .catch(function (error) {
          _this.$vux.loading.hide()
          if (error.response.status === 401) {
            _this.$vux.alert.show({
              title: '状态',
              content: '请先登录',
              onHide() {
                _this.$router.replace('/')
              }
            })
          } else {
            _this.$vux.alert.show({
              title: '提示',
              content: '错误，我也不知道怎么回事',
              onShow() {
              },
              onHide() {
                console.log(error)
                _this.$router.replace('/')
              }
            })
          }
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
      this.$http.get('/api/queries/' + this.$route.params.name + '/refresh')
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
      this.$http.post('/api/queries/' + this.$route.params.name + '/save', {
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
      this.$http.post('/api/queries/' + this.$route.params.name + '/refresh', {
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
            content: '错误，我也不知道怎么回事',
            onShow() {
            },
            onHide() {
              console.log(response)
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
