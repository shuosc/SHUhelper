import Fly from 'flyio/dist/npm/wx'
// var Fly = require('flyio/dist/npm/wx')
export var http = new Fly()
http.config.baseURL = 'https://api.shuhelper.cn/v1'

function redirectToLogin(authID) {
  wx.redirectTo({
    url: `/pages/login/main?authID=${authID}`
  })
}

function reAuth() {
  wx.login({
    success: res => {
      http
        .get(`/auth/mp/app?code=${res.code}&source=shuhelper_mp_app`)
        .then(response => {
          redirectToLogin(response.data.authID)
        })
        .catch(err => {
          redirectToLogin(err.response.data.authID)
        })
    }
  })
}
http.interceptors.response.use(
  (response) => {
    // Do something with response data .
    // Just return the data field of response
    return response.data
  },
  (err) => {
    console.log(err)
    if (err.response.status === 401) {
      reAuth()
    }
    // Do something with response error
    // return Promise.resolve("ssss")
  }
)
