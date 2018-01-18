// MIT License

// Copyright(c) 2017 nearspears

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files(the "Software"), to deal
//   in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
/* eslint-disable */
import Navigation from './Navigation'
import NavHistory from './NavHistory'

export default {
  install: (Vue, {router, store}) => {
    if (!router) {
      console.error('stack need router')
      return
    }
    if (store) {
      store.registerModule('stack', {
        state: {
          direction: 'forward'
        },
        mutations: {
          updateDirection: function (state, direction) {
            state.direction = direction
          }
        }
      })
    }

    // replace 比较特殊，所以只能监控编程式导航
    let replace = router.push
    router.replace = function (location, onComplete, onAbort) {
      replace.apply(router, [location, () => {
        var name = NavHistory.pop()
        NavHistory.pop()
        NavHistory.push(name)
        NavHistory.action = 'replace'
        if (onComplete) {
          onComplete(arguments)
        }
      }, onAbort])
    }

    router.clearPush = function (location, onComplete, onAbort) {
      router.push(location, () => {
        var name = NavHistory.pop()
        NavHistory.clear()
        NavHistory.push(name)
        NavHistory.action = 'clearPush'
        if (onComplete) {
          onComplete(arguments)
        }
      }, onAbort)
    }

    router.beforeEach((to, from, next) => {
      let matched = to.matched[0]
      if (matched && matched.components) {
        let component = matched.components.default
        // console.log(matched.components.default)
        if (typeof component === 'function') {
          // async component
          matched.components.default = (r) => {
            return component((c) => {
              c.name = c.name || 'AC-' + matched.name
              // for dev environment
              c._Ctor && (c._Ctor[0].options.name = c.name)
              r(c)
            })
          }
        } else {
          component.name = component.name || 'AC-' + matched.name
        }
        // console.log(matched.components.default)
        if (store) {
          if (NavHistory.isForward(component.name)) {
            store.commit('updateDirection', 'forward')
          } else {
            store.commit('updateDirection', 'backward')
          }
        }
      }
      next()
    })

    // handle router change
    router.afterEach((to, from) => {
      let matched = to.matched[0]
      if (matched && matched.components) {
        let component = matched.components.default
        if (NavHistory.isForward(component.name)) {
          if (component.stackType && component.stackType === 'single') {
            NavHistory.pushSingle(component.name)
          } else {
            NavHistory.push(component.name)
          }
        } else {
          NavHistory.pop()
        }
      }
    })
    Vue.component('navigation', Navigation)
  }
}
