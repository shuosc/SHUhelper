<template>
  <div style="height:100%;">
  <view-box ref="viewBox" body-padding-top="46px" body-padding-bottom="0px">
    <x-header slot="header" title="SHUhelper 2.0 preview" style="width:100%;position:absolute;left:0;top:0;z-index:100;">
    </x-header>
      <group title="查询信息" >
        <cell title="信息名" :value="$route.params.name"></cell>
        <cell title="来源网站" value="value"></cell>
        <cell title="上次更新日期" value="value"></cell>
        <x-button type="primary" style="margin-top:10px;" @click.native="updateData()">更新数据</x-button>
      </group>
      <divider>数据库中的信息</divider>
      <div style="height:100%;font-size:0.8rem;" v-html="content"></div>
      <divider v-if="data.status=='no records'">无记录</divider>
    </view-box>
  </div>
</template>

<script>
import { XHeader, ViewBox, Divider, Group, Cell, XButton } from 'vux'
import CryptoJS from '../libs/encryption.js'
export default {
  components: {
    XHeader,
    ViewBox,
    Divider,
    Group,
    Cell,
    XButton
  },
  data () {
    return {
      content: '',
      data: {},
      captcha_img: '',
      captcha: ''
    }
  },
  created: function () {
    this.getData()
  },
  computed: {
  },
  methods: {
    getData () {
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
            var decrypted = CryptoJS.AES.decrypt(response.data.content, _this.$store.state.account.password)
            _this.content = decrypted.toString(CryptoJS.enc.Utf8)
          }
        } else {
          _this.$vux.alert.show({
            title: '状态',
            content: '请先登录',
            onHide () {
              _this.$router.replace('/')
            }
          })
        }
      })
      .catch(function (response) {
        _this.$vux.loading.hide()
        _this.$vux.alert.show({
          title: '提示',
          content: '错误，我也不知道怎么回事',
          onShow () {
          },
          onHide () {
            console.log(response)
            _this.$router.replace('/')
          }
        })
      })
    },
    updateData () {
      var _this = this
      this.$vux.loading.show({
        text: '少女祈祷中...'
      })
      _this.prepareUpdate()
    },
    prepareUpdate () {
      var _this = this
      this.$http.get('/api/queries/' + this.$route.params.name + '/refresh')
      .then((response) => {
        if (response.data.success) {
          _this.captcha_img = response.data.captcha_img
          _this.postUpdate()
        } else {
          _this.$vux.alert.show({
            title: '状态',
            content: '准备查询失败，服务器故障'
          })
        }
        this.$vux.loading.hide()
      })
    },
    saveToServer () {
      var _this = this
      this.$http.post('/api/queries/' + this.$route.params.name + '/save', {
        data: CryptoJS.AES.encrypt(this.content, _this.$store.state.account.password).toString(),
        site: this.$route.params.name
      })
      .then((response) => {
        if (response.data.success) {
          _this.$vux.alert.show({
            title: '状态',
            content: '保存成功'
          })
        }
      })
    },
    postUpdate () {
      var _this = this
      if (this.captcha_img !== '' && this.captcha === '') {
        this.captchaForm = true
        return
      }
      this.$vux.loading.show({
        text: '少女祈祷中...'
      })
      this.$http.post('/api/queries/' + this.$route.params.name + '/refresh', {
        'card_id': this.$store.state.account.card_id,
        'password': this.$store.state.account.password,
        'captcha': this.captcha
      })
      .then((response) => {
        _this.$vux.loading.hide()
        if (response.data.success) {
          _this.content = response.data.content.data
          _this.$vux.alert.show({
            title: '状态',
            content: '成功'
          })
          _this.saveToServer()
          console.log(_this.data)
        } else {
          _this.$vux.alert.show({
            title: '状态',
            content: '查询失败'
          })
        }
      })
    }
  }
}
</script>

<style>

</style>
