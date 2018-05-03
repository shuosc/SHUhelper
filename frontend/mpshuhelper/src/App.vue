<script>
// import userAPI from './api/user'

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
@import '../static/iconfont.css'
.column,
.flex,
.row {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
}

.column.inline,
.flex.inline,
.row.inline {
  display: -webkit-inline-box;
  display: -ms-inline-flexbox;
  display: inline-flex;
}

.row.reverse {
  -webkit-box-orient: horizontal;
  -webkit-box-direction: reverse;
  -ms-flex-direction: row-reverse;
  flex-direction: row-reverse;
}

.column {
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: column;
}

.column,
.column.reverse {
  -webkit-box-orient: vertical;
}

.column.reverse {
  -webkit-box-direction: reverse;
  -ms-flex-direction: column-reverse;
  flex-direction: column-reverse;
}

.wrap {
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
}

.no-wrap {
  -ms-flex-wrap: nowrap;
  flex-wrap: nowrap;
}

.reverse-wrap {
  -ms-flex-wrap: wrap-reverse;
  flex-wrap: wrap-reverse;
}

.col {
  -ms-flex-preferred-size: 0;
  flex-basis: 0;
  -webkit-box-flex: 1;
  -ms-flex-positive: 1;
  flex-grow: 1;
  min-height: 1px;
}

.row > .col {
  max-width: 100%;
}

.row > .col,
.row > .col-xs {
  width: 100%;
}

.col-xs {
  min-height: 1px;
}

.row > .col-xs-1 {
  width: 100%;
}

.col-xs-1 {
  min-height: 1px;
}

.row > .col-xs-2 {
  width: 100%;
}

.col-xs-2 {
  min-height: 1px;
}

.row > .col-xs-3 {
  width: 100%;
}

.col-xs-3 {
  min-height: 1px;
}

.row > .col-xs-4 {
  width: 100%;
}

.col-xs-4 {
  min-height: 1px;
}

.row > .col-xs-5 {
  width: 100%;
}

.col-xs-5 {
  min-height: 1px;
}

.row > .col-xs-6 {
  width: 100%;
}

.col-xs-6 {
  min-height: 1px;
}

.row > .col-xs-7 {
  width: 100%;
}

.col-xs-7 {
  min-height: 1px;
}

.row > .col-xs-8 {
  width: 100%;
}

.col-xs-8 {
  min-height: 1px;
}

.row > .col-xs-9 {
  width: 100%;
}

.col-xs-9 {
  min-height: 1px;
}

.row > .col-xs-10 {
  width: 100%;
}

.col-xs-10 {
  min-height: 1px;
}

.row > .col-xs-11 {
  width: 100%;
}

.col-xs-11 {
  min-height: 1px;
}

.row > .col-xs-12 {
  width: 100%;
}

.col-xs-12 {
  min-height: 1px;
}

.row > .col-sm {
  width: 100%;
}

.col-sm {
  min-height: 1px;
}

.row > .col-sm-1 {
  width: 100%;
}

.col-sm-1 {
  min-height: 1px;
}

.row > .col-sm-2 {
  width: 100%;
}

.col-sm-2 {
  min-height: 1px;
}

.row > .col-sm-3 {
  width: 100%;
}

.col-sm-3 {
  min-height: 1px;
}

.row > .col-sm-4 {
  width: 100%;
}

.col-sm-4 {
  min-height: 1px;
}

.row > .col-sm-5 {
  width: 100%;
}

.col-sm-5 {
  min-height: 1px;
}

.row > .col-sm-6 {
  width: 100%;
}

.col-sm-6 {
  min-height: 1px;
}

.row > .col-sm-7 {
  width: 100%;
}

.col-sm-7 {
  min-height: 1px;
}

.row > .col-sm-8 {
  width: 100%;
}

.col-sm-8 {
  min-height: 1px;
}

.row > .col-sm-9 {
  width: 100%;
}

.col-sm-9 {
  min-height: 1px;
}

.row > .col-sm-10 {
  width: 100%;
}

.col-sm-10 {
  min-height: 1px;
}

.row > .col-sm-11 {
  width: 100%;
}

.col-sm-11 {
  min-height: 1px;
}

.row > .col-sm-12 {
  width: 100%;
}

.col-sm-12 {
  min-height: 1px;
}

.row > .col-md {
  width: 100%;
}

.col-md {
  min-height: 1px;
}

.row > .col-md-1 {
  width: 100%;
}

.col-md-1 {
  min-height: 1px;
}

.row > .col-md-2 {
  width: 100%;
}

.col-md-2 {
  min-height: 1px;
}

.row > .col-md-3 {
  width: 100%;
}

.col-md-3 {
  min-height: 1px;
}

.row > .col-md-4 {
  width: 100%;
}

.col-md-4 {
  min-height: 1px;
}

.row > .col-md-5 {
  width: 100%;
}

.col-md-5 {
  min-height: 1px;
}

.row > .col-md-6 {
  width: 100%;
}

.col-md-6 {
  min-height: 1px;
}

.row > .col-md-7 {
  width: 100%;
}

.col-md-7 {
  min-height: 1px;
}

.row > .col-md-8 {
  width: 100%;
}

.col-md-8 {
  min-height: 1px;
}

.row > .col-md-9 {
  width: 100%;
}

.col-md-9 {
  min-height: 1px;
}

.row > .col-md-10 {
  width: 100%;
}

.col-md-10 {
  min-height: 1px;
}

.row > .col-md-11 {
  width: 100%;
}

.col-md-11 {
  min-height: 1px;
}

.row > .col-md-12 {
  width: 100%;
}

.col-md-12 {
  min-height: 1px;
}

.row > .col-xl {
  width: 100%;
}

.col-xl {
  min-height: 1px;
}

.row > .col-xl-1 {
  width: 100%;
}

.col-xl-1 {
  min-height: 1px;
}

.row > .col-xl-2 {
  width: 100%;
}

.col-xl-2 {
  min-height: 1px;
}

.row > .col-xl-3 {
  width: 100%;
}

.col-xl-3 {
  min-height: 1px;
}

.row > .col-xl-4 {
  width: 100%;
}

.col-xl-4 {
  min-height: 1px;
}

.row > .col-xl-5 {
  width: 100%;
}

.col-xl-5 {
  min-height: 1px;
}

.row > .col-xl-6 {
  width: 100%;
}

.col-xl-6 {
  min-height: 1px;
}

.row > .col-xl-7 {
  width: 100%;
}

.col-xl-7 {
  min-height: 1px;
}

.row > .col-xl-8 {
  width: 100%;
}

.col-xl-8 {
  min-height: 1px;
}

.row > .col-xl-9 {
  width: 100%;
}

.col-xl-9 {
  min-height: 1px;
}

.row > .col-xl-10 {
  width: 100%;
}

.col-xl-10 {
  min-height: 1px;
}

.row > .col-xl-11 {
  width: 100%;
}

.col-xl-11 {
  min-height: 1px;
}

.row > .col-xl-12 {
  width: 100%;
}

.col-xl-12 {
  min-height: 1px;
}

.row > .col-auto {
  width: auto;
}

.col-auto {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 auto;
  flex: 0 0 auto;
}

.col-grow {
  -webkit-box-flex: 1;
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
}

.justify-start {
  -webkit-box-pack: start;
  -ms-flex-pack: start;
  justify-content: flex-start;
}

.justify-end {
  -webkit-box-pack: end;
  -ms-flex-pack: end;
  justify-content: flex-end;
}

.flex-center,
.justify-center {
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
}

.justify-between {
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
}

.justify-around {
  -ms-flex-pack: distribute;
  justify-content: space-around;
}

.items-start {
  -webkit-box-align: start;
  -ms-flex-align: start;
  align-items: flex-start;
}

.items-end {
  -webkit-box-align: end;
  -ms-flex-align: end;
  align-items: flex-end;
}

.flex-center,
.items-center {
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
}

.items-stretch {
  -webkit-box-align: stretch;
  -ms-flex-align: stretch;
  align-items: stretch;
}

.content-start {
  -ms-flex-line-pack: start;
  align-content: flex-start;
}

.content-end {
  -ms-flex-line-pack: end;
  align-content: flex-end;
}

.content-center {
  -ms-flex-line-pack: center;
  align-content: center;
}

.content-between {
  -ms-flex-line-pack: justify;
  align-content: space-between;
}

.content-around {
  -ms-flex-line-pack: distribute;
  align-content: space-around;
}

.self-start {
  -ms-flex-item-align: start;
  align-self: flex-start;
}

.self-end {
  -ms-flex-item-align: end;
  align-self: flex-end;
}

.self-center {
  -ms-flex-item-align: center;
  -ms-grid-row-align: center;
  align-self: center;
}

.self-stretch {
  -ms-flex-item-align: stretch;
  -ms-grid-row-align: stretch;
  align-self: stretch;
}

.col-1 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 8.3333%;
  flex: 0 0 8.3333%;
}

.row > .col-1 {
  max-width: 8.3333%;
}

.offset-1 {
  margin-left: 8.3333%;
}

.col-2 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 16.6667%;
  flex: 0 0 16.6667%;
}

.row > .col-2 {
  max-width: 16.6667%;
}

.offset-2 {
  margin-left: 16.6667%;
}

.col-3 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 25%;
  flex: 0 0 25%;
}

.row > .col-3 {
  max-width: 25%;
}

.offset-3 {
  margin-left: 25%;
}

.col-4 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 33.3333%;
  flex: 0 0 33.3333%;
}

.row > .col-4 {
  max-width: 33.3333%;
}

.offset-4 {
  margin-left: 33.3333%;
}

.col-5 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 41.6667%;
  flex: 0 0 41.6667%;
}

.row > .col-5 {
  max-width: 41.6667%;
}

.offset-5 {
  margin-left: 41.6667%;
}

.col-6 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 50%;
  flex: 0 0 50%;
}

.row > .col-6 {
  max-width: 50%;
}

.offset-6 {
  margin-left: 50%;
}

.col-7 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 58.3333%;
  flex: 0 0 58.3333%;
}

.row > .col-7 {
  max-width: 58.3333%;
}

.offset-7 {
  margin-left: 58.3333%;
}

.col-8 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 66.6667%;
  flex: 0 0 66.6667%;
}

.row > .col-8 {
  max-width: 66.6667%;
}

.offset-8 {
  margin-left: 66.6667%;
}

.col-9 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 75%;
  flex: 0 0 75%;
}

.row > .col-9 {
  max-width: 75%;
}

.offset-9 {
  margin-left: 75%;
}

.col-10 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 83.3333%;
  flex: 0 0 83.3333%;
}

.row > .col-10 {
  max-width: 83.3333%;
}

.offset-10 {
  margin-left: 83.3333%;
}

.col-11 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 91.6667%;
  flex: 0 0 91.6667%;
}

.row > .col-11 {
  max-width: 91.6667%;
}

.offset-11 {
  margin-left: 91.6667%;
}

.col-12 {
  -webkit-box-flex: 0;
  -ms-flex: 0 0 100%;
  flex: 0 0 100%;
}

.row > .col-12 {
  max-width: 100%;
}

.offset-12 {
  margin-left: 100%;
}

.xs-gutter {
  margin: -8px 0 0 -8px;
}

.xs-gutter > div {
  padding: 8px 0 0 8px;
}

.sm-gutter {
  margin: -16px 0 0 -16px;
}

.sm-gutter > div {
  padding: 16px 0 0 16px;
}

.md-gutter {
  margin: -32px 0 0 -32px;
}

.md-gutter > div {
  padding: 32px 0 0 32px;
}

.xl-gutter {
  margin: -64px 0 0 -64px;
}

.xl-gutter > div {
  padding: 64px 0 0 64px;
}

.no-horiz-gutter {
  margin-left: 0;
}

.no-horiz-gutter > div {
  padding-left: 0;
}

.no-vert-gutter {
  margin-top: 0;
}

.no-vert-gutter > div {
  padding-top: 0;
}

@media (min-width: 0) {
  .col-xs {
    max-width: 100%;
    -ms-flex-preferred-size: 0;
    flex-basis: 0;
    -webkit-box-flex: 1;
    -ms-flex-positive: 1;
    flex-grow: 1;
  }
  .col-xs-auto {
    width: auto;
    -webkit-box-flex: 0;
    -ms-flex: 0 0 auto;
    flex: 0 0 auto;
  }
  .col-xs-1 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 8.3333%;
    flex: 0 0 8.3333%;
  }
  .row > .col-xs-1 {
    max-width: 8.3333%;
  }
  .offset-xs-1 {
    margin-left: 8.3333%;
  }
  .col-xs-2 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 16.6667%;
    flex: 0 0 16.6667%;
  }
  .row > .col-xs-2 {
    max-width: 16.6667%;
  }
  .offset-xs-2 {
    margin-left: 16.6667%;
  }
  .col-xs-3 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 25%;
    flex: 0 0 25%;
  }
  .row > .col-xs-3 {
    max-width: 25%;
  }
  .offset-xs-3 {
    margin-left: 25%;
  }
  .col-xs-4 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 33.3333%;
    flex: 0 0 33.3333%;
  }
  .row > .col-xs-4 {
    max-width: 33.3333%;
  }
  .offset-xs-4 {
    margin-left: 33.3333%;
  }
  .col-xs-5 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 41.6667%;
    flex: 0 0 41.6667%;
  }
  .row > .col-xs-5 {
    max-width: 41.6667%;
  }
  .offset-xs-5 {
    margin-left: 41.6667%;
  }
  .col-xs-6 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 50%;
    flex: 0 0 50%;
  }
  .row > .col-xs-6 {
    max-width: 50%;
  }
  .offset-xs-6 {
    margin-left: 50%;
  }
  .col-xs-7 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 58.3333%;
    flex: 0 0 58.3333%;
  }
  .row > .col-xs-7 {
    max-width: 58.3333%;
  }
  .offset-xs-7 {
    margin-left: 58.3333%;
  }
  .col-xs-8 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 66.6667%;
    flex: 0 0 66.6667%;
  }
  .row > .col-xs-8 {
    max-width: 66.6667%;
  }
  .offset-xs-8 {
    margin-left: 66.6667%;
  }
  .col-xs-9 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 75%;
    flex: 0 0 75%;
  }
  .row > .col-xs-9 {
    max-width: 75%;
  }
  .offset-xs-9 {
    margin-left: 75%;
  }
  .col-xs-10 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 83.3333%;
    flex: 0 0 83.3333%;
  }
  .row > .col-xs-10 {
    max-width: 83.3333%;
  }
  .offset-xs-10 {
    margin-left: 83.3333%;
  }
  .col-xs-11 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 91.6667%;
    flex: 0 0 91.6667%;
  }
  .row > .col-xs-11 {
    max-width: 91.6667%;
  }
  .offset-xs-11 {
    margin-left: 91.6667%;
  }
  .col-xs-12 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 100%;
    flex: 0 0 100%;
  }
  .row > .col-xs-12 {
    max-width: 100%;
  }
  .offset-xs-12 {
    margin-left: 100%;
  }
}

@media (min-width: 576px) {
  .col-sm {
    max-width: 100%;
    -ms-flex-preferred-size: 0;
    flex-basis: 0;
    -webkit-box-flex: 1;
    -ms-flex-positive: 1;
    flex-grow: 1;
  }
  .col-sm-auto {
    width: auto;
    -webkit-box-flex: 0;
    -ms-flex: 0 0 auto;
    flex: 0 0 auto;
  }
  .col-sm-1 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 8.3333%;
    flex: 0 0 8.3333%;
  }
  .row > .col-sm-1 {
    max-width: 8.3333%;
  }
  .offset-sm-1 {
    margin-left: 8.3333%;
  }
  .col-sm-2 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 16.6667%;
    flex: 0 0 16.6667%;
  }
  .row > .col-sm-2 {
    max-width: 16.6667%;
  }
  .offset-sm-2 {
    margin-left: 16.6667%;
  }
  .col-sm-3 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 25%;
    flex: 0 0 25%;
  }
  .row > .col-sm-3 {
    max-width: 25%;
  }
  .offset-sm-3 {
    margin-left: 25%;
  }
  .col-sm-4 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 33.3333%;
    flex: 0 0 33.3333%;
  }
  .row > .col-sm-4 {
    max-width: 33.3333%;
  }
  .offset-sm-4 {
    margin-left: 33.3333%;
  }
  .col-sm-5 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 41.6667%;
    flex: 0 0 41.6667%;
  }
  .row > .col-sm-5 {
    max-width: 41.6667%;
  }
  .offset-sm-5 {
    margin-left: 41.6667%;
  }
  .col-sm-6 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 50%;
    flex: 0 0 50%;
  }
  .row > .col-sm-6 {
    max-width: 50%;
  }
  .offset-sm-6 {
    margin-left: 50%;
  }
  .col-sm-7 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 58.3333%;
    flex: 0 0 58.3333%;
  }
  .row > .col-sm-7 {
    max-width: 58.3333%;
  }
  .offset-sm-7 {
    margin-left: 58.3333%;
  }
  .col-sm-8 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 66.6667%;
    flex: 0 0 66.6667%;
  }
  .row > .col-sm-8 {
    max-width: 66.6667%;
  }
  .offset-sm-8 {
    margin-left: 66.6667%;
  }
  .col-sm-9 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 75%;
    flex: 0 0 75%;
  }
  .row > .col-sm-9 {
    max-width: 75%;
  }
  .offset-sm-9 {
    margin-left: 75%;
  }
  .col-sm-10 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 83.3333%;
    flex: 0 0 83.3333%;
  }
  .row > .col-sm-10 {
    max-width: 83.3333%;
  }
  .offset-sm-10 {
    margin-left: 83.3333%;
  }
  .col-sm-11 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 91.6667%;
    flex: 0 0 91.6667%;
  }
  .row > .col-sm-11 {
    max-width: 91.6667%;
  }
  .offset-sm-11 {
    margin-left: 91.6667%;
  }
  .col-sm-12 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 100%;
    flex: 0 0 100%;
  }
  .row > .col-sm-12 {
    max-width: 100%;
  }
  .offset-sm-12 {
    margin-left: 100%;
  }
}

@media (min-width: 768px) {
  .col-md {
    max-width: 100%;
    -ms-flex-preferred-size: 0;
    flex-basis: 0;
    -webkit-box-flex: 1;
    -ms-flex-positive: 1;
    flex-grow: 1;
  }
  .col-md-auto {
    width: auto;
    -webkit-box-flex: 0;
    -ms-flex: 0 0 auto;
    flex: 0 0 auto;
  }
  .col-md-1 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 8.3333%;
    flex: 0 0 8.3333%;
  }
  .row > .col-md-1 {
    max-width: 8.3333%;
  }
  .offset-md-1 {
    margin-left: 8.3333%;
  }
  .col-md-2 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 16.6667%;
    flex: 0 0 16.6667%;
  }
  .row > .col-md-2 {
    max-width: 16.6667%;
  }
  .offset-md-2 {
    margin-left: 16.6667%;
  }
  .col-md-3 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 25%;
    flex: 0 0 25%;
  }
  .row > .col-md-3 {
    max-width: 25%;
  }
  .offset-md-3 {
    margin-left: 25%;
  }
  .col-md-4 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 33.3333%;
    flex: 0 0 33.3333%;
  }
  .row > .col-md-4 {
    max-width: 33.3333%;
  }
  .offset-md-4 {
    margin-left: 33.3333%;
  }
  .col-md-5 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 41.6667%;
    flex: 0 0 41.6667%;
  }
  .row > .col-md-5 {
    max-width: 41.6667%;
  }
  .offset-md-5 {
    margin-left: 41.6667%;
  }
  .col-md-6 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 50%;
    flex: 0 0 50%;
  }
  .row > .col-md-6 {
    max-width: 50%;
  }
  .offset-md-6 {
    margin-left: 50%;
  }
  .col-md-7 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 58.3333%;
    flex: 0 0 58.3333%;
  }
  .row > .col-md-7 {
    max-width: 58.3333%;
  }
  .offset-md-7 {
    margin-left: 58.3333%;
  }
  .col-md-8 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 66.6667%;
    flex: 0 0 66.6667%;
  }
  .row > .col-md-8 {
    max-width: 66.6667%;
  }
  .offset-md-8 {
    margin-left: 66.6667%;
  }
  .col-md-9 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 75%;
    flex: 0 0 75%;
  }
  .row > .col-md-9 {
    max-width: 75%;
  }
  .offset-md-9 {
    margin-left: 75%;
  }
  .col-md-10 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 83.3333%;
    flex: 0 0 83.3333%;
  }
  .row > .col-md-10 {
    max-width: 83.3333%;
  }
  .offset-md-10 {
    margin-left: 83.3333%;
  }
  .col-md-11 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 91.6667%;
    flex: 0 0 91.6667%;
  }
  .row > .col-md-11 {
    max-width: 91.6667%;
  }
  .offset-md-11 {
    margin-left: 91.6667%;
  }
  .col-md-12 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 100%;
    flex: 0 0 100%;
  }
  .row > .col-md-12 {
    max-width: 100%;
  }
  .offset-md-12 {
    margin-left: 100%;
  }
}

@media (min-width: 1200px) {
  .col-xl {
    max-width: 100%;
    -ms-flex-preferred-size: 0;
    flex-basis: 0;
    -webkit-box-flex: 1;
    -ms-flex-positive: 1;
    flex-grow: 1;
  }
  .col-xl-auto {
    width: auto;
    -webkit-box-flex: 0;
    -ms-flex: 0 0 auto;
    flex: 0 0 auto;
  }
  .col-xl-1 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 8.3333%;
    flex: 0 0 8.3333%;
  }
  .row > .col-xl-1 {
    max-width: 8.3333%;
  }
  .offset-xl-1 {
    margin-left: 8.3333%;
  }
  .col-xl-2 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 16.6667%;
    flex: 0 0 16.6667%;
  }
  .row > .col-xl-2 {
    max-width: 16.6667%;
  }
  .offset-xl-2 {
    margin-left: 16.6667%;
  }
  .col-xl-3 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 25%;
    flex: 0 0 25%;
  }
  .row > .col-xl-3 {
    max-width: 25%;
  }
  .offset-xl-3 {
    margin-left: 25%;
  }
  .col-xl-4 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 33.3333%;
    flex: 0 0 33.3333%;
  }
  .row > .col-xl-4 {
    max-width: 33.3333%;
  }
  .offset-xl-4 {
    margin-left: 33.3333%;
  }
  .col-xl-5 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 41.6667%;
    flex: 0 0 41.6667%;
  }
  .row > .col-xl-5 {
    max-width: 41.6667%;
  }
  .offset-xl-5 {
    margin-left: 41.6667%;
  }
  .col-xl-6 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 50%;
    flex: 0 0 50%;
  }
  .row > .col-xl-6 {
    max-width: 50%;
  }
  .offset-xl-6 {
    margin-left: 50%;
  }
  .col-xl-7 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 58.3333%;
    flex: 0 0 58.3333%;
  }
  .row > .col-xl-7 {
    max-width: 58.3333%;
  }
  .offset-xl-7 {
    margin-left: 58.3333%;
  }
  .col-xl-8 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 66.6667%;
    flex: 0 0 66.6667%;
  }
  .row > .col-xl-8 {
    max-width: 66.6667%;
  }
  .offset-xl-8 {
    margin-left: 66.6667%;
  }
  .col-xl-9 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 75%;
    flex: 0 0 75%;
  }
  .row > .col-xl-9 {
    max-width: 75%;
  }
  .offset-xl-9 {
    margin-left: 75%;
  }
  .col-xl-10 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 83.3333%;
    flex: 0 0 83.3333%;
  }
  .row > .col-xl-10 {
    max-width: 83.3333%;
  }
  .offset-xl-10 {
    margin-left: 83.3333%;
  }
  .col-xl-11 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 91.6667%;
    flex: 0 0 91.6667%;
  }
  .row > .col-xl-11 {
    max-width: 91.6667%;
  }
  .offset-xl-11 {
    margin-left: 91.6667%;
  }
  .col-xl-12 {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 100%;
    flex: 0 0 100%;
  }
  .row > .col-xl-12 {
    max-width: 100%;
  }
  .offset-xl-12 {
    margin-left: 100%;
  }
}
/* .container {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 200rpx 0;
  box-sizing: border-box;
} */
/* this rule will be remove */
* {
  transition: width 2s;
  -moz-transition: width 2s;
  -webkit-transition: width 2s;
  -o-transition: width 2s;
}
</style>
