import userAPI from '../../api/user'

// initial state
// shape: [{ id, quantity }]
const state = {
  posts: [],
  draft: {}
}

// getters
const getters = {
  username: state => state.username,
  checkoutStatus: state => state.checkoutStatus,

  cartProducts: (state, getters, rootState) => {
    return state.added.map(({ id, quantity }) => {
      const product = rootState.products.all.find(product => product.id === id)
      return {
        title: product.title,
        price: product.price,
        quantity
      }
    })
  },

  cartTotalPrice: (state, getters) => {
    return getters.cartProducts.reduce((total, product) => {
      return total + product.price * product.quantity
    }, 0)
  }
}

// actions
const actions = {
  login({ commit, state }, payload) {
    return new Promise((resolve, reject) => {
      userAPI.login(
        payload.userID,
        payload.password,
        payload => {
          commit('updateUserInfo', payload)
          resolve()
        },
        () => {
          reject()
        }
      )
    })
  },
  refreshToken({ commit, state }) {
    userAPI.refreshToken(state.token, token => {
      commit('updateToken', token)
    })
  }
}

// mutations
const mutations = {
  updateAccountInfo(state, payload) {
    state.userID = payload.userID
    state.password = payload.password
    state.authID = payload.authID
  },
  updateToken(state, token) {
    state.token = token
  },
  clearUserInfo(state) {
    state.userID = ''
    state.password = ''
    state.name = ''
    state.username = ''
    state.nickname = ''
    state.token = ''
    state.avatarURL = 'https://static.shuhelper.cn/avatar_default.jpg'
  },
  updateUserInfo(state, payload) {
    state.userID = payload.userID
    state.password = payload.password
    state.name = payload.name
    state.username = payload.username
    state.nickname = payload.nickname
    state.token = payload.token
    state.avatarURL = payload.avatarURL
  },
  pushProductToCart(state, { id }) {
    state.added.push({
      id,
      quantity: 1
    })
  },

  incrementItemQuantity(state, { id }) {
    const cartItem = state.added.find(item => item.id === id)
    cartItem.quantity++
  },

  setCartItems(state, { items }) {
    state.added = items
  },

  setCheckoutStatus(state, status) {
    state.checkoutStatus = status
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
