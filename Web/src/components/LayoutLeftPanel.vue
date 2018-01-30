<template lang="pug">
  q-list.no-padding(no-border='')
    q-card.full-width.no-margin.left-banner(flat='')
      q-card-main( v-if="$store.state.user.cardID!==''")
        q-side-link(item='', :to="`/profile/${$store.state.user.cardID}`")
          q-item-side(:avatar='`//static.shuhelper.cn/${$store.state.user.avatar}`')
          q-item-main
            q-item-tile(label='') {{$store.state.user.name}}
            q-item-tile(sublabel='') {{$store.state.user.cardID}}
          q-item-side
            q-btn(flat='' @click='logout') 注销
      q-card-main( v-else)
        q-side-link(item='', :to="'/login'")
          q-item-side(:avatar='`//static.shuhelper.cn/avatar_default.jpg`')
          q-item-main
            q-item-tile(label='') 游客
          q-item-side 登录
    // <q-list-header>Essential Links</q-list-header>
    div(v-if="$q.platform.is.ios")
      q-side-link(v-for="link in internalNavigationiOS" :key="link.name" item='', sparse='', :to='link.to')
        q-item-side(:icon='link.icon')
        q-item-main(:label='link.name')
    div(v-else)
      q-side-link(v-for="link in internalNavigationAndroid" :key="link.name" item='', sparse='', :to='link.to')
        q-item-side(:icon='link.icon')
        q-item-main(:label='link.name')
</template>

<script>
import { Toast } from 'quasar'
export default {
  name: 'leftPanel',
  data() {
    return {
      internalNavigationAndroid: [
        { to: '/index', icon: 'fa-xuexiao', name: '首页' },
        { to: '/apps', icon: 'explore', name: '应用' },
        { to: '/square', icon: 'fa-filtervintage', name: '广场' },
        { to: '/schedule', icon: 'fa-calendar1', name: '日程' },

        { to: '/about', icon: 'info', name: '关于' }
        // { to: '/message', icon: 'fa-xuexiao', name: '消息' },
        // { to: '/config', icon: 'fa-xuexiao', name: '设置  ' }
      ],
      internalNavigationiOS: [
        { to: '/index', icon: 'fa-xuexiao', name: '首页' },
        { to: '/apps', icon: 'explore', name: '应用' },
        { to: '/square', icon: 'fa-filtervintage', name: '广场' },
        { to: '/schedule', icon: 'fa-calendar1', name: '日程' },
        { to: '/about', icon: 'info', name: '关于' }
        // { to: '/config', icon: 'fa-xuexiao', name: '设置  ' }
      ]
    }
  },
  methods: {
    handleTitleChange(title) {
      this.$parent.$parent.changeTitle(title)
    },
    logout() {
      localStorage.clear()
      sessionStorage.clear()
      let token = this.$store.state.user.token
      this.$store.commit('clearAccount')
      this.$emit('logout')
      this.$http.get('/api/users/logout?token=' + token)
      Toast.create({ html: '已注销' })
    }
  }
}
</script>

<style lang="stylus" scoped>
</style>
