<script>
// import userAPI from './api/user'
import './weui.css'
import './iconfont.css'
export default {
  beforeCreate() {
    wx.showLoading()
    this.$store.dispatch('refreshToken').then(() => {
      wx.hideLoading()
    })
    // this.$store.dispatch('timeSync')
  },
  created() {
    // 调用API从本地缓存中获取数据
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    console.log('app created and cache logs by setStorageSync')
    // userAPI.wxAutoLogin(
    //   resp => {
    //     console.log(resp)
    //     wx.setStorageSync('user', resp)
    //   },
    //   err => {
    //     console.log(err)
    //     wx.redirectTo({
    //       url: `/pages/login/main?authID=${err.response.data.authID}`
    //     })
    //   }
    // )
    console.log(this.$store.state.count)
  },
  methods: {}
}
</script>

<style lang="stylus">
/* @import '../static/iconfont.css' */
@import './grid.styl'
</style>
