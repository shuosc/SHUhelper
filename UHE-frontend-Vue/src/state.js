const state = {
  state: {
    user: {
      cardID: '',
      openID: '',
      name: '游客',
      nickname: '',
      password: '',
      token: ''
    },
    ui: {
      toolbarVisible: true,
      bottomNavigationVisible: true,
      loginDialog: false
    },
    passwords: {
      main: ''
    },
    snackbar: {
      timeout: 2000,
      y: 'bottom',
      x: null,
      mode: '',
      visible: false,
      text: 'hi',
      context: 'info'
    },
    showLoginForm: false
  },
  mutations: {
    closeLoginDialog(state) {
      state.ui.loginDialog = false
    },
    showLoginDialog(state) {
      state.ui.loginDialog = true
    },
    showBottomNavgation(state) {
      state.ui.bottomNavigationVisible = true
    },
    hideBottomNavgation(state) {
      state.ui.bottomNavigationVisible = false
    },
    hideToolbar(state) {
      state.ui.toolbarVisible = false
    },
    showToolbar(state) {
      state.ui.toolbarVisible = false
    },
    resetSnackbar(state) {
      state.snackbar = {
        timeout: 3000,
        y: 'top',
        x: null,
        mode: '',
        visible: false,
        text: 'hi',
        context: 'info'
      }
    },
    showSnackbar(state, payload) {
      state.snackbar.text = payload.text
      state.snackbar.visible = true
    },

    updateToken(state, token) {
      state.token = token
    },
    changeLoginFormShow(state) {
      state.showLoginForm = !state.showLoginForm
    },
    updateAccount(state, payload) {
      state.user.cardID = payload.cardID
      state.user.name = payload.name
      state.user.nickname = payload.nickname
      state.user.password = payload.password
      state.user.token = payload.token
    },
    clearAccount(state) {
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
