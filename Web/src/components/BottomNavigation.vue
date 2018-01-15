<template lang="pug">
  q-tabs(align="justify")
    q-route-tab(icon="fa-xuexiao" to="/" exact slot="title")
    q-route-tab(icon="fa-filtervintage" to="/square" exact slot="title")
    q-route-tab(icon="fa-calendar1" to="/schedule" exact slot="title")
    // <q-route-tab icon="fa-message" to="/message" exact slot="title" /> 
    //</q-scroll-area>
</template>

<script>
import { QTabs, QRouteTab } from 'quasar'
export default {
  components: {
    QTabs,
    QRouteTab
  }
}
</script>

<style>

</style>
