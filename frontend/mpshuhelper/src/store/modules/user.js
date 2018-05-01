import user from '../../api/user'

// initial state
// shape: [{ id, quantity }]
const state = {
  ID: '',
  password: '',
  name: '',
  username: '',
  nickname: '',
  token: '',
  avatarURL: ''
}

// getters
const getters = {
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
  login({ commit, state }) {
    user.wxAutoLogin(payload => {
      commit('clearUserInfo')
      commit('updateUserInfo', payload)
    })
  }

  // addProductToCart ({ state, commit }, product) {
  //   commit('setCheckoutStatus', null)
  //   if (product.inventory > 0) {
  //     const cartItem = state.added.find(item => item.id === product.id)
  //     if (!cartItem) {
  //       commit('pushProductToCart', { id: product.id })
  //     } else {
  //       commit('incrementItemQuantity', cartItem)
  //     }
  //     // remove 1 item from stock
  //     commit('decrementProductInventory', { id: product.id })
  //   }
  // }
}

// mutations
const mutations = {
  clearUserInfo(state) {
    state.ID = ''
    state.passwor = ''
    state.name = ''
    state.username = ''
    state.nickname = ''
    state.token = ''
    state.avatarURL = ''
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
