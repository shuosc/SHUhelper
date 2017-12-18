<template>
  <q-layout ref="layout" view="lHh Lpr fff" :left-class="{'bg-grey-2': true}">
    <q-toolbar slot="header">
      <q-btn flat @click="$refs.layout.toggleLeft()">
        <q-icon name="menu" />
      </q-btn>

      <q-toolbar-title>
        首页
        <!-- <div slot="subtitle">Running on University Helper Engine v{{$UHE.version}}</div> -->
      </q-toolbar-title>
    </q-toolbar>

    <div slot="left">
      <!--
        Use <q-side-link> component
        instead of <q-item> for
        internal vue-router navigation
      -->
      <left-panel/>
    </div>
    <!--
      Replace following <div> with
      <router-view /> component
      if using subRoutes
    -->
    <router-view />

  </q-layout>
</template>

<script>
import LeftPanel from '@/LayoutLeftPanel'
export default {
  name: 'index',
  components: {
    LeftPanel
  },
  data() {
    return {}
  },
  methods: {
    refresher(done) {
      done()
    }
  },
  mounted() {
    this.$router.push('/index')
  }
}
</script>

<style lang="stylus" scoped>
.namecard
  opacity 0.9
  // background #EDE574 /* fallback for old browsers */
  // background -webkit-linear-gradient(to left, #E1F5C4, #EDE574) /* Chrome 10-25, Safari 5.1-6 */
  // background linear-gradient(to left, #E1F5C4, #EDE574) /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
</style>
