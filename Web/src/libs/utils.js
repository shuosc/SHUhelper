/* eslint-disable */
export const convertTimeString = function (date) {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}-${date.getHours()}-${date.getMinutes()}`
}

export const randomColor = function () {
  return '#' + Math.floor(Math.random() * 16777215).toString(16)
}

export const parseURL = function (url) {
  var a = document.createElement('a')
  a.href = url
  return {
    source: url,
    protocol: a.protocol.replace(':', ''),
    host: a.hostname,
    port: a.port,
    query: a.search,
    params: (function () {
      var ret = {},
        seg = a.search.replace(/^\?/, '').split('&'),
        len = seg.length,
        i = 0,
        s
      for (; i < len; i++) {
        if (!seg[i]) {
          continue
        }
        s = seg[i].split('=')
        ret[s[0]] = s[1]
      }
      return ret
    })(),
    file: (a.pathname.match(/\/([^\/?#]+)$/i) || [, ''])[1],
    hash: a.hash.replace('#', ''),
    path: a.pathname.replace(/^([^\/])/, '/$1'),
    relative: (a.href.match(/tps?:\/\/[^\/]+(.+)/) || [, ''])[1],
    segments: a.pathname.replace(/^\//, '').split('/')
  }
}
import CryptoJS from './encryption.js'
export function decrypt(data, pw) {
  function pad(str, n) {
    var i = (str).length
    while (i++ < n) str = str + '0'
    return str
  }
  var key = CryptoJS.enc.Utf8.parse(pad(pw.slice(0, 16), 16))
  var iv = CryptoJS.enc.Hex.parse('000102030405060708090a0b0c0d0e0f')
  var decrypted = CryptoJS.AES.decrypt(data, key, {
    iv: iv
  })
  // console.log(decrypted.toString(CryptoJS.enc.Utf8))
  return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8))
}
// export default convertTimeString
// export default parseURL
