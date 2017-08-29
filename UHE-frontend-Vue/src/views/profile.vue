<template>
  <div>

  </div>
</template>

<script>
export default {
  data () {
    return {
      user: {}
    }
  },
  created () {
    this.getProfile()
  },
  methods: {
    getProfile () {
      this.$http.get(`/api/users/${this.$route.params.id}`)
        .then((response) => {
          this.user = reponse.data
        })
    }
  }
}

</script>
