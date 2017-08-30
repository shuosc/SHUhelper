<template>
  <div>
    <v-card>
      <v-card-title>
        赵逸群
      </v-card-title>
      <v-card-text>
        <v-layout row wrap>
          <v-flex xs12>{{$route.params.id}}</v-flex>
          <v-flex xs12>学院</v-flex>
          <v-flex xs12>专业</v-flex>

        </v-layout>
      </v-card-text>
      <v-card-actions>
        <v-btn primary block>发消息</v-btn>

      </v-card-actions>
    </v-card>
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
          this.user = response.data
        })
    }
  }
}

</script>
