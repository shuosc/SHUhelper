<template>
  <q-list no-border class=" no-padding">
    <q-card flat class="full-width no-margin left-banner">
      <q-card-main>
        <q-side-link item :to="$store.state.user.cardID===''?'/login':`/profile/${$store.state.user.cardID}`">
          <q-item-side :avatar="`//static.shuhelper.cn/${$store.state.user.avatar}`" />
          <q-item-main>
            <q-item-tile label>{{$store.state.user.name}}</q-item-tile>
            <q-item-tile sublabel>{{$store.state.user.cardID}}</q-item-tile>
          </q-item-main>
          <q-item-side>
            <q-btn flat @click.stop="logout">注销</q-btn>
          </q-item-side>
        </q-side-link>
      </q-card-main>
    </q-card>
    <!-- <q-list-header>Essential Links</q-list-header> -->
    <q-side-link item sparse to="/index">
      <q-item-side icon="fa-xuexiao" />
      <q-item-main label="首页" />
    </q-side-link>
    <!-- <q-side-link item sparse to="/square">
      <q-item-side icon="record_voice_over" />
      <q-item-main label="广场" />
    </q-side-link> -->
    <!-- <q-side-link item sparse to="/apps">
      <q-item-side icon="record_voice_over" />
      <q-item-main label="应用" />
    </q-side-link> -->
    <q-side-link item sparse to="/schedule">
      <q-item-side icon="fa-calendar1" />
      <q-item-main label="日程" />
    </q-side-link>
    <!-- <q-side-link item sparse to="/message">
      <q-item-side icon="chat" />
      <q-item-main label="消息" />
    </q-side-link> -->
    <!-- <q-item link sparse @click="launch('http://quasar-framework.org')">
          <q-item-side icon="school" />
          <q-item-main label="设置" />
        </q-item> -->
  </q-list>
</template>

<script>
import { Toast } from 'quasar'
export default {
  name: 'leftPanel',
  methods: {
    logout() {
      localStorage.clear()
      sessionStorage.clear()
      let token = this.$store.state.user.token
      this.$store.commit('clearAccount')
      this.$router.push('/login')
      Toast.create({ html: '已注销' })
      this.$http.get('/api/users/logout?token=' + token)
    }
  }
}
</script>

<style lang="stylus" scoped>
</style>
