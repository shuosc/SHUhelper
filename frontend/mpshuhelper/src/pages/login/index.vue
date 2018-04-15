<template lang="pug">
  .page
    .content
      div(square='', flat='', style='position:absolute;top:-5rem;width:100%;')
        div(style='text-align:center;')
          span(style='font-weight:bold;font-size:1.5rem;color:white;text-shadow:yellow 0 1px 0;') SHUhelper
          br
          small(style='color:white;text-shadow:green 0 1px 0;')
            span(style='color:red;') ♥
            | meow~
      div
        input(@blur='$v.form.cardID.$touch', v-model='form.cardID', type='number', required='', float-label='一卡通账号')
        //- q-input(v-model='form.cardID', type='number', required='', float-label='一卡通账号')
        //- q-input( v-model='form.password', type='password', required='', float-label='密码')
        input(@blur='$v.form.password.$touch', v-model='form.password', type='password', required='', float-label='密码')
        //- checkbox(v-model='rememberMe', label='记住我')
        button.full-width(:size="mini" loader='', color='primary', @click='login')
          | 登录
      div(square='', flat='', style='position:absolute;bottom:-4rem;width:100%;')
        div(style='text-align:center;color:white;font-size:0.8rem;')
          small 上海大学开源社区
          br
          small SHU Open Source Community
</template>

<script>
export default {
  //   components: {
  //     QCheckbox,
  //     QInput
  //   },
  data() {
    return {
      form: {
        cardID: '',
        password: ''
      },
      passwordVisiable: true,
      loginLoading: false,
      rememberMe: false
    }
  },
  // validations: {
  //   form: {
  //     cardID: { required },
  //     password: { required }
  //   }
  // },
  mounted() {
    // this.$refs.basicModal.open()
  },
  beforeDestory() {
    // this.$refs.basicModal.close()
    // debugger
  },
  methods: {
    // login(e, done) {
    //   var _this = this
    //   this.$v.form.$touch()
    //   if (this.$v.form.$error) {
    //     done()
    //     Toast.create('请正确填写账号和密码')
    //     return
    //   }
    //   this.form.cardID = this.form.cardID.toString()
    //   this.loginLoading = true
    //   this.$http
    //     .post('/api/users/login/', {
    //       card_id: this.form.cardID,
    //       password: this.form.password
    //     })
    //     .then(response => {
    //       var payload = {
    //         cardID: this.form.cardID,
    //         password: this.form.password,
    //         name: response.data.name,
    //         nickname: response.data.nickname,
    //         token: response.data.token,
    //         avatar: response.data.avatar
    //       }
    //       try {
    //         payload.custom = JSON.parse(response.data.custom)
    //       } catch (error) {
    //         done()
    //         createToast(error)
    //         payload.custom = {}
    //       }
    //       try {
    //         if (this.rememberMe) {
    //           localStorage.setItem('loginstate', JSON.stringify(payload))
    //         } else {
    //           sessionStorage.setItem('loginstate', JSON.stringify(payload))
    //         }
    //       } catch (err) {
    //         createToast('本地存储失败，如果在使用浏览器，请关闭无痕浏览模式')
    //       }
    //       _this.$store.commit('updateAccount', payload)
    //       done()
    //       // _this.$store.commit('closeLoginDialog')
    //       try {
    //         var custom = JSON.parse(payload.custom)
    //         var loginText = custom.loginText
    //       } catch (e) {
    //         console.log(e)
    //       }

    //       // debugger
    //       createToast(
    //         loginText === undefined
    //           ? `${response.data.name}，欢迎登录`
    //           : `${loginText}`
    //       )
    //       ga.loginUser(payload.cardID)
    //       Events.$emit('app:hideLeft')
    //       // Events.$emit('app:hideLeft')
    //       _this.$router.push('/index')
    //       // if (_this.$route.query.redirect) {
    //       //   _this.$router.replace(_this.$route.query.redirect)
    //       // } else {
    //       //   _this.$router.push('/index')
    //       // }
    //     })
    //     .catch(function(error) {
    //       console.log(error)
    //       done()
    //       createToast('登录失败' + error)
    //     })
    // }
  }
}
</script>

<style scoped>
.page {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: #50a3a2;
  background: -webkit-linear-gradient(top left, #50a3a2 0%, #53e3a6 100%);
  background: linear-gradient(to bottom right, #50a3a2 0%, #53e3a6 100%);
  height: 100vh; /* Allow spacing based on window height */
  margin: 0;
  min-height: 240px;
  z-index: 6000;
}

/* The background from https://codepen.io/lotap/pen/yNYxRz */
/* The form part */
.content {
  /* A box that the form resides in - centered vertically and horizontally based on the window. The max-width and % width combo allow it to resize for small devices */
  background: #FFF;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: block;
  left: 50%;
  max-width: 360px;
  position: absolute;
  top: 50%;
  -ms-transform: translate(-50%, -50%);
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  width: 90%;
  z-index: 2;
}

/* The Background Part - Each svg element will act as a column that rises. Within each svg column will be a rect element that rotates. Due to an error FF regarding the transform-origin of objects in an svg, the transform-orgin must be explicitly given without percents */
.bg-boxes {
  /* Set the container for the svg elements to take up the whole window and hide objects outside of the window */
  height: 100%;
  min-height: 240px;
  position: absolute;
  overflow: hidden;
  width: 100%;
  z-index: 1;
}
</style>
