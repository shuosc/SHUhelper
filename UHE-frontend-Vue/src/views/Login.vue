 <template>
  <v-card>
    <v-card-text class="px-0">
      <v-container fluid class="px-3 py-0">
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
            <v-btn primary dark block @click.native="login()" :loading="loginLoading" >
              登录</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
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
      this.$http.post('/api/v1/users/login/', {
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
            payload.custom = JSON.parse(response.data.custom)
          } catch (e) {
            e
            payload.custom = {}
          }
          try {
            sessionStorage.setItem('loginstate', JSON.stringify(payload))
          } catch (err) {
            _this.$store.commit('showSnackbar', { text: `本地存储失败，如果在使用浏览器，请关闭无痕浏览模式` })
          }
          if (this.remeberMe) {
            try {
              localStorage.setItem('loginstate', JSON.stringify(payload))
            } catch (err) {
              _this.$store.commit('showSnackbar', { text: `本地存储失败，如果在使用浏览器，请关闭无痕浏览模式` })
            }
          }
          _this.$store.commit('updateAccount', payload)
          // _this.$store.commit('closeLoginDialog')
          try {
            var custom = JSON.parse(payload.custom)
            var loginText = custom.loginText
          } catch (e) {
            e
          }
          if (loginText === undefined) {
            _this.$store.commit('showSnackbar', { text: `${response.data.name}，欢迎登陆` })
          } else {
            _this.$store.commit('showSnackbar', { text: `${loginText}` })
          }
          this.loginLoading = false
          this.$router.go(-1)
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
