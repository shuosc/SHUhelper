<template lang="pug">
  q-tabs(align="justify")
    q-route-tab(icon="fa-xuexiao" to="/" exact @click="onClick('index')" slot="title")
    q-route-tab(icon="explore" to="/apps" exact  @click="onClick" slot="title")
    q-route-tab(icon="fa-filtervintage" to="/square" exact @click="onClick('square')" slot="title")
    q-route-tab(icon="fa-calendar1" to="/schedule" exact @click="onClick" slot="title")
    // <q-route-tab icon="fa-message" to="/message" exact slot="title" /> 
    //</q-scroll-area>
</template>

<script>
import { QTabs, QRouteTab, Events } from 'quasar'
export default {
  components: {
    QTabs,
    QRouteTab
  },
  methods: {
    onClick(name) {
      // console.log('on click bottom')
      Events.$emit('app:refresh:' + name, () => {})
    }
  }
}
</script>

<style>

</style>
