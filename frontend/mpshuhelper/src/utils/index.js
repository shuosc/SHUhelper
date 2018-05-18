/* eslint-disable */
import app from '../main'
import CryptoJS from 'crypto-js'

function formatNumber(n) {
  const str = n.toString()
  return str[1] ? str : `0${str}`
}
export const lostNFoundSites = [{
    name: '没有放到任何失物招领点',
    value: null
  },
  {
    name: '花儿小站（菜鸟驿站）',
    value: 'HE'
  },
  {
    name: '益新一楼充值处',
    value: 'YX'
  },
  {
    name: '南区食堂',
    value: 'N1'
  },
  {
    name: '南二门武保处',
    value: 'NWB'
  },
  {
    name: '南区食堂一楼充值处',
    value: 'N2'
  }, {
    name: '新世界大学生村门卫处',
    value: 'XSJ'
  },
  {
    name: '西门门卫处',
    value: 'XM'
  },
  {
    name: '图书馆（三楼人文社科）',
    value: 'T3'
  },
  {
    name: '图书馆（四楼人文社科）',
    value: 'T4'
  },
  {
    name: '东区食堂',
    value: 'DQ'
  },
  {
    name: '东门武保处',
    value: 'DWB'
  },
  {
    name: 'A楼收发室',
    value: 'AL'
  },
  {
    name: '南大门武保处',
    value: 'NWB'
  },
  {
    name: '北门武保处',
    value: 'BWB'
  }
]

const CNNUM = {
  一: 1,
  二: 2,
  三: 3,
  四: 4,
  五: 5
}
export function hashCode(s) {
  var h = 0,
    l = s.length,
    i = 0
  if (l > 0)
    while (i < l) h = ((h << 5) - h + s.charCodeAt(i++)) | 0
  return h
}
export function formatTime(date) {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()

  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  const t1 = [year, month, day].map(formatNumber).join('/')
  const t2 = [hour, minute, second].map(formatNumber).join(':')

  return `${t1} ${t2}`
}
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

export function isCourseInWeek(time, week) {
  let inWeek = false
  if (time[4]) {
    if (time[4] === '单') {
      if (week % 2 === 1) {
        inWeek = true
      }
    } else if (time[4] === '双') {
      if (week % 2 === 0) {
        inWeek = true
      }
    }
  } else if (time[5]) {
    if (parseInt(time[5]) <= week && week <= parseInt(time[6])) {
      inWeek = true
    }
  } else if (time[7]) {
    if (week === parseInt(time[7]) || week === parseInt(time[8])) {
      inWeek = true
    }
  } else {
    inWeek = true
  }
  return inWeek
}
export function coursetimeToNum(time, week) {
  var patt = /([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468).*?\)|\((?:([0-9]+),([0-9]+)\u5468).*?\))*/
  var timelist = []
  var str = time
  while (patt.test(str)) {
    var coursetime = patt.exec(str)
    str = str.replace(patt, '')
    var item = {
      day: parseInt(CNNUM[coursetime[1]] - 1),
      Start: parseInt(coursetime[2]),
      End: parseInt(coursetime[3]),
      thisWeek: isCourseInWeek(coursetime, week)
    }
    timelist.push(item)
  }
  return timelist
}
