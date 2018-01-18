
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
class NavHistory {
  constructor () {
    this.value = []
    this.action = 'push'
  }

  push (path) {
    let index = this.value.indexOf(path)
    if (index > -1 && index === this.value.length - 1) {
      return
    }
    this.value.push(path)
    this.action = 'push'
  }

  pushSingle (path) {
    var index = -1
    for (let i = 0; i < this.value.length; i++) {
      if (this.value[i] === path) {
        index = i
        break
      }
    }
    if (index >= 0) {
      this.value.splice(index, this.value.length - index)
    }
    this.value.push(path)
    this.action = 'pushSingle'
  }

  pop () {
    this.action = 'pop'
    return this.value.pop()
  }

  clear () {
    this.value.splice(0, this.value.length)
  }

  size () {
    return this.value.length
  }

  isForward (path) {
    var index = this.value.lastIndexOf(path)
    if (index > -1 && index === this.value.length - 2) {
      return false
    }
    return true
  }
}

let history = new NavHistory()
export default history
