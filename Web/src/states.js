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
      avatar: 'avatar_default.jpg',
      custom: {
        theme: 'bluetheme'
      },
      config: {
        locale: '本部'
      }
    },
    feeds: [],
    ui: {
      toolbarVisible: true,
      bottomNavigationVisible: true,
      loginDialog: false,
      closeModal: null
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
    time: {
      year: 17,
      term: 2,
      week: 0,
      course: 0,
      day: 0,
      updated: false
    },
    toolbar: {
      actions: [],
      states: []
    }
  },
  getters: {
    feeds: state => {
      return state.feeds
    }
  },
  mutations: {
    addFeed(state, payload) {
      state.feeds.push(payload)
    },
    updateFeed(state, payload) {
      state.feeds.splice(payload.index, 1, payload.feed)
    },
    deleteFeed(state, index) {
      state.feeds[index].deleted = true
    },
    clearFeeds(state) {
      state.feeds = []
    },
    updateToolBar(state, payload) {
      state.toolbar = payload
    },
    updateTime(state, payload) {
      state.time = payload
      state.time.updated = true
    },
    clearToolbar(state) {
      state.toolbar = {
        actions: [],
        states: []
      }
    },
    showImageModal(state, close) {
      state.ui.closeModal = close
    },
    hideImageModal(state) {
      state.ui.closeModal = null
    },
    setAvatar(state, avatar) {
      state.user.avatar = avatar
    },
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
      state.user.avatar = payload.avatar
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
