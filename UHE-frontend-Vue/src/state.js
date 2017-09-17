const state = {
  state: {
    user: {
      cardID: '',
      openID: '',
      name: '游客',
      nickname: '',
      password: '',
      phypassword: '',
      token: '',
      custom: {
        theme: 'bluetheme'
      }
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
    showLoginForm: false,
    date: {
      year: '',
      term: '',
      week: '',
      course: ''
    },
    toolbar: {
      actions: [],
      states: []
    }
  },
  mutations: {
    updateToolBar(state, payload) {
      state.toolbar = payload
    },
    clearToolbar(state) {
      state.toolbar = {
        actions: [],
        states: []
      }
    },
    // updateToolbarAction(state, index, subindex, key, value) {
    //   state.toolbar.actions[index].items[subindex][key] = value
    // },
    updateToolbarState(state, payload) {
      state.toolbar.states[payload.index] = payload.value
      console.log(payload.index, payload.value)
    },
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
      state.user.custom = payload.custom
      if (!state.user.custom.theme) {
        state.user.custom.theme = 'bluetheme'
      }
    },
    changeTheme(state, theme) {
      state.user.custom.theme = theme
    },
    clearAccount(state) {
      state.user = {
        cardID: '',
        openID: '',
        name: '',
        nickname: '',
        password: '',
        token: '',
        custom: {
          theme: 'bluetheme'
        }
      }
    }
  }
}

export default state
