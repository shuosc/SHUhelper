<template lang="pug">
  .page
    .content
      q-card.no-margin(square='', flat='', style='position:absolute;top:-5rem;width:100%;')
        q-card-main(style='text-align:center;')
          span(style='font-weight:bold;font-size:2rem;color:white;text-shadow:yellow 0 1px 0;') SHUhelper.cn Beta
          br
          small(style='color:white;text-shadow:green 0 1px 0;')
            span(style='color:red;') ♥ 
            | Do have faith in what you're doing.
      q-card.no-margin(flat='')
        q-card-main
          q-input(@blur='$v.form.cardID.$touch', v-model='form.cardID', type='number', required='', float-label='一卡通账号')
          q-input(@blur='$v.form.password.$touch', v-model='form.password', type='password', required='', float-label='密码')
          q-checkbox(v-model='rememberMe', label='记住我')
        q-card-actions
          q-btn.full-width(loader='', color='primary', @click='login')
            | 登录
      q-card.no-margin(square='', flat='', style='position:absolute;bottom:-4rem;width:100%;')
        q-card-main(style='text-align:center;color:white;')
          small 上海大学开源社区
          br
          small SHU Open Source Community
    .bg-boxes
      svg#col1(width='300px', height='100%')
        rect#bub1.bubble(width='150px', height='150px', x='75px', y='75px')
      svg#col2(width='200px', height='100%')
        rect#bub2.bubble(width='100px', height='100px', x='50px', y='50px')
      svg#col3(width='260px', height='100%')
        rect#bub3.bubble(width='130px', height='130px', x='65px', y='65px')
      svg#col4(width='160px', height='100%')
        rect#bub4.bubble(width='80px', height='80px', x='40px', y='40px')
      svg#col5(width='240px', height='100%')
        rect#bub5.bubble(width='120px', height='120px', x='60px', y='60px')
      // Here is a triangle
      svg#col6(width='200px', height='100%')
        polygon#bub6.bubble(points='50,150 100,50 150,150')
      svg#col7(width='200px', height='100%')
        rect#bub7.bubble(width='100px', height='100px', x='50px', y='50px')
      svg#col8(width='200px', height='100%')
        rect#bub8.bubble(width='100px', height='100px', x='50px', y='50px')
      svg#col9(width='200px', height='100%')
        rect#bub9.bubble(width='100px', height='100px', x='50px', y='50px')
      svg#col10(width='200px', height='100%')
        rect#bub10.bubble(width='100px', height='100px', x='50px', y='50px')
      svg#col11(width='100px', height='100%')
        rect#bub11.bubble(width='50px', height='50px', x='25px', y='25px')
</template>

<script>
import { Toast } from 'quasar'
import { required } from 'vuelidate/lib/validators'
import ga from '../libs/analytics'
function createToast(text) {
  Toast.create({
    html: text,
    timeout: 2500,
    button: {
      color: '#fff'
    }
  })
}
export default {
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
  validations: {
    form: {
      cardID: { required },
      password: { required }
    }
  },
  mounted() {
    // this.$refs.basicModal.open()
  },
  beforeDestory() {
    // this.$refs.basicModal.close()
    // debugger
  },
  methods: {
    login(e, done) {
      var _this = this
      this.$v.form.$touch()
      if (this.$v.form.$error) {
        done()
        Toast.create('请正确填写账号和密码')
        return
      }
      this.form.cardID = this.form.cardID.toString()
      this.loginLoading = true
      this.$http
        .post('/api/users/login/', {
          card_id: this.form.cardID,
          password: this.form.password
        })
        .then(response => {
          var payload = {
            cardID: this.form.cardID,
            password: this.form.password,
            name: response.data.name,
            nickname: response.data.nickname,
            token: response.data.token,
            avatar: response.data.avatar
          }
          try {
            payload.custom = JSON.parse(response.data.custom)
          } catch (error) {
            done()
            createToast(error)
            payload.custom = {}
          }
          try {
            if (this.rememberMe) {
              localStorage.setItem('loginstate', JSON.stringify(payload))
            } else {
              sessionStorage.setItem('loginstate', JSON.stringify(payload))
            }
          } catch (err) {
            createToast('本地存储失败，如果在使用浏览器，请关闭无痕浏览模式')
          }
          _this.$store.commit('updateAccount', payload)
          done()
          // _this.$store.commit('closeLoginDialog')
          try {
            var custom = JSON.parse(payload.custom)
            var loginText = custom.loginText
          } catch (e) {
            console.log(e)
          }

          // debugger
          createToast(
            loginText === undefined
              ? `${response.data.name}，欢迎登陆`
              : `${loginText}`
          )
          ga.loginUser(payload.cardID)
          _this.$router.push('/index')
          // if (_this.$route.query.redirect) {
          //   _this.$router.replace(_this.$route.query.redirect)
          // } else {
          //   _this.$router.push('/index')
          // }
        })
        .catch(function(error) {
          console.log(error)
          done()
          createToast('登陆失败' + error)
        })
    }
  }
}
</script>

<style scoped lang="stylus">
.page {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: #50a3a2;
  background: -webkit-linear-gradient(top left, #50a3a2 0%, #53e3a6 100%);
  background: linear-gradient(to bottom right, #50a3a2 0%, #53e3a6 100%);
  // font-family: 'Roboto', sans-serif;
  // font-weight: 300;
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

svg {
  /* Set defaults for svg columns. Opacity set to 0 so the elements are invisible before the animation begins and will not show up on browsers without animation */
  -webkit-animation: riser 20s infinite;
  animation: riser 20s infinite;
  opacity: 0;
  overflow: visible;
  position: absolute;
}

.bubble {
  /* Set the defaults for the "bubbles". transform-origin should always be the center-point of the object including blank-space within the svg. Since the object should be centered, this is equal to the width of the object. The default bubble is 100px by 100px in an svg object with a width of 200px */
  -webkit-animation: rotator 20s linear infinite;
  animation: rotator 20s linear infinite;
  fill: #FFF;
  -webkit-transform-origin: 100px 100px;
  transform-origin: 100px 100px;
}

#col1 {
  /* Since this element is larger than the set default, I want it to rise a little faster to give a subtle sense of depth */
  -webkit-animation-duration: 15s;
  animation-duration: 15s;
}

#bub1 {
  /* The transform-origin has to be redefined because this bubble is not the set default size */
  -webkit-transform-origin: 150px 150px;
  transform-origin: 150px 150px;
}

#col2 {
  /* To offset the columns, adjust their left attribute and add an animation-delay */
  left: 15%;
  -webkit-animation-delay: 18s;
  animation-delay: 18s;
}

#col3 {
  left: 30%;
  -webkit-animation-delay: 14s;
  animation-delay: 14s;
  -webkit-animation-duration: 17s;
  animation-duration: 17s;
}

#bub3 {
  -webkit-animation-delay: 14s;
  animation-delay: 14s;
  -webkit-transform-origin: 130px 130px;
  transform-origin: 130px 130px;
}

#col4 {
  left: 45%;
  -webkit-animation-delay: 8s;
  animation-delay: 8s;
  -webkit-animation-duration: 22s;
  animation-duration: 22s;
}

#bub4 {
  -webkit-animation-delay: 8s;
  animation-delay: 8s;
  -webkit-transform-origin: 80px 80px;
  transform-origin: 80px 80px;
}

#col5 {
  left: 60%;
  -webkit-animation-delay: 15s;
  animation-delay: 15s;
  -webkit-animation-duration: 18s;
  animation-duration: 18s;
}

#bub5 {
  -webkit-animation-delay: 15s;
  animation-delay: 15s;
  -webkit-transform-origin: 120px 120px;
  transform-origin: 120px 120px;
}

#col6 {
  left: 75%;
  -webkit-animation-delay: 19s;
  animation-delay: 19s;
}

#col7 {
  left: 90%;
  -webkit-animation-delay: 4s;
  animation-delay: 4s;
}

#col8 {
  left: -5%;
  -webkit-animation-delay: 11s;
  animation-delay: 11s;
}

#col9 {
  left: 25%;
  -webkit-animation-delay: 5s;
  animation-delay: 5s;
}

#col10 {
  left: 50%;
  -webkit-animation-delay: 12s;
  animation-delay: 12s;
}

#col11 {
  left: 67%;
  -webkit-animation-delay: 1s;
  animation-delay: 1s;
  -webkit-animation-duration: 25s;
  animation-duration: 25s;
}

#bub11 {
  -webkit-animation-delay: 1s;
  animation-delay: 1s;
  -webkit-transform-origin: 50px 50px;
  transform-origin: 50px 50px;
}

/* Rotation Animation - Should be set to a factor of 360 to prevent jumpiness */
@keyframes rotator {
  to {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@keyframes rotator {
  to {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@keyframes riser {
  0% {
    opacity: 0.2;
    -webkit-transform: translateY(100%);
    transform: translateY(100%);
  }

  100% {
    opacity: 0.2;
    -webkit-transform: translateY(-250px);
    transform: translateY(-250px);
  }
}

@keyframes riser {
  0% {
    opacity: 0.2;
    -webkit-transform: translateY(100%);
    transform: translateY(100%);
  }

  100% {
    opacity: 0.2;
    -webkit-transform: translateY(-250px);
    transform: translateY(-250px);
  }
}
</style>
