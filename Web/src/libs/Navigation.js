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
import NavHistory from './NavHistory'

function getFirstComponentChild (children) {
  if (Array.isArray(children)) {
    for (let i = 0; i < children.length; i++) {
      const c = children[i]
      if (isDef(c) && isDef(c.componentOptions)) {
        return c
      }
    }
  }
}

function isDef (v) {
  return v !== undefined && v !== null
}

function getComponentName (opts) {
  return opts && (opts.Ctor.options.name || opts.tag)
}

export default {
  name: 'stack',
  abstract: true,

  created () {
    this.cache = Object.create(null)
    this.stack = []
  },

  destroyed () {
    for (let item of this.stack) {
      item.$vnode.data.hook.destroy(item.$vnode)
      item.$destroy()
    }
  },

  render () {
    const vnode = getFirstComponentChild(this.$slots.default)
    const componentOptions = vnode && vnode.componentOptions
    if (componentOptions) {
      const name = getComponentName(componentOptions)
      var data = vnode.data
      ;(data.hook || (data.hook = {})).create = (_, vnode) => {
        this.stack.push(vnode.componentInstance)
      }
      if (NavHistory.action === 'pop') {
        for (let i = this.stack.length - 1; i >= 0; i--) {
          if (getComponentName(this.stack[i].$vnode.componentOptions) === name) {
            vnode.componentInstance = this.stack[i]

            for (let j = this.stack.length - 1; j > i; j--) {
              this.stack[j].$vnode.data.hook.destroy(this.stack[j].$vnode)
              this.stack[j].$destroy()
            }
            this.stack.splice(i, this.stack.length - i)
            break
          }
        }
        NavHistory.action = 'push' // 重置
      } else if (NavHistory.action === 'pushSingle') {
        for (let i = this.stack.length - 1; i >= 0; i--) {
          if (getComponentName(this.stack[i].$vnode.componentOptions) === name) {
            for (let j = this.stack.length - 1; j > i - 1; j--) {
              this.stack[j].$vnode.data.hook.destroy(this.stack[j].$vnode)
              this.stack[j].$destroy()
            }
            this.stack.splice(i, this.stack.length - i)
            break
          }
        }
        NavHistory.action = 'push' // 重置
      } else if (NavHistory.action === 'replace') {
        if (getComponentName(this.stack[this.stack.length - 1].$vnode.componentOptions) !== name) {
          this.stack.splice(this.stack.length - 1, 1)
        }
        NavHistory.action = 'push' // 重置
      } else if (NavHistory.action === 'clearPush') {
        this.stack.splice(0, this.stack.length)
        NavHistory.action = 'push' // 重置
      }
      vnode.data.keepAlive = true
    }
    return vnode
  }
}
