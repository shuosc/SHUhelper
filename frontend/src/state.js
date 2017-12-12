const state = {
  state: {
    account: {
      card_id: '',
      open_id: '',
      name: '',
      nickname: '',
      password: '',
      token: ''
    },
    passwords: {
      main: ''
    },
    showLoginForm: false
  },
  mutations: {
    updateToken (state, token) {
      state.token = token
    },
    changeLoginFormShow (state) {
      state.showLoginForm = !state.showLoginForm
    },
    updateAccount (state, payload) {
      state.account.card_id = payload.card_id
      state.account.name = payload.name
      state.account.nickname = payload.nickname
      state.account.password = payload.password
      state.account.token = payload.token
    },
    clearAccount (state) {
      state.account = {
        card_id: '',
        open_id: '',
        name: '',
        nickname: '',
        password: '',
        token: ''
      }
    }
  }
}

export default state
