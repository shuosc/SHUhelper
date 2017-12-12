<template>
  <div style="height:100%;">
    <iframe style="height:100%;width:100%"
            :src="'/static/' + $route.params.name + '.html'"></iframe>
  </div>
</template>

<script>

export default {
  components: {},
  data() {
    return {
    }
  },
  computed: {
  },
  methods: {
  }
}
</script>

<style>

</style>
