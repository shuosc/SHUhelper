 <template>
  <v-layout row justify-center class="ma-0 pa-0">
    <v-dialog v-model="$store.state.ui.loginDialog" fullscreen transition="dialog-bottom-transition" hide-overlay persistent>
      <v-card>
        <v-toolbar dark class="primary">
          <v-btn icon @click.native="$store.commit('closeLoginDialog')" dark>
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>登录</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-container fluid class="px-3">
          <v-layout row wrap>
            <v-flex xs12>
              <v-text-field label="一卡通" v-model="cardID"></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field label="密码" :append-icon="passwordVisiable ? 'visibility' : 'visibility_off'" :append-icon-cb="() => (passwordVisiable = !passwordVisiable)" :type="passwordVisiable ? 'password' : 'text'" v-model="password"></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-checkbox v-bind:label="'记住我'" hint="不是自己的设备请不要勾选此项" persistent-hint v-model="remeberMe" light></v-checkbox>
            </v-flex>
            <v-flex xs12>
  
              <v-btn primary dark block @click.native="login()">
                <v-progress-circular v-show="loginLoading" :indeterminate="loginLoading" class="red--text"></v-progress-circular>登录</v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-dialog>
  </v-layout>
</template>
<script>
export default {
  data () {
    return {
      cardID: '',
      password: '',
      passwordVisiable: true,
      loginLoading: false,
      remeberMe: false
    }
  },
  methods: {
    login () {
      var _this = this
      this.loginLoading = true
      this.$http.post('/api/users/login/', {
        card_id: this.cardID,
        password: this.password
      })
        .then((response) => {
          var payload = {
            cardID: this.cardID,
            password: this.password,
            name: response.data.name,
            nickname: response.data.nickname,
            token: response.data.token
          }
          try {
            localStorage.setItem('loginstate', JSON.stringify(payload))
          } catch (err) {
            _this.$store.commit('showSnackbar', { text: `本地存储失败，如果您在使用APP，请升级到最新版本(http://static.shuhelper.cn/SHUhelper.apk)，如果在使用浏览器，请关闭无痕浏览模式` })
          }
          _this.$store.commit('updateAccount', payload)
          _this.$store.commit('closeLoginDialog')
          _this.$store.commit('showSnackbar', { text: `${response.data.name}，欢迎登陆` })
          this.loginLoading = false
        })
        .catch(function (error) {
          error
          _this.loginLoading = false
          _this.$store.commit('showSnackbar', { text: '登陆失败' + error })
        })
    }
  }
}
</script>
