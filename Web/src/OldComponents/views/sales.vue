<template>
  <div>
    <v-card class="grey lighten-4 elevation-0">
      <v-btn fab dark small color="primary" @click.native="refresh">
        刷新
      </v-btn>
      <v-container fluid class="py-0 px-2">
        <v-layout row wrap>
          <v-flex xs12 v-for="(good,index) in goods" :key="good.name">
            {{good.name}}-{{good.record.length}}
            <v-btn fab dark small color="primary" @click.native="deleteOne(index)">
              <v-icon dark>remove</v-icon>
            </v-btn>
            <v-btn fab dark small color="primary" @click.native="addOne(index)">
              <v-icon dark>add</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      goods: []
    }
  },
  created() {
    this.$http.get('/api/v1/goods/').then(response => {
      this.goods = response.data
    })
  },
  methods: {
    refresh() {
      this.$http.get('/api/v1/goods/').then(response => {
        this.goods = response.data
      })
    },
    deleteOne(index) {
      this.$http
        .delete(`/api/v1/goods/${this.goods[index].id}`)
        .then(response => {
          this.goods = response.data
        })
    },
    addOne(index) {
      this.$http
        .put(`/api/v1/goods/${this.goods[index].id}`)
        .then(response => {
          this.goods = response.data
        })
    }
  }
}
</script>

<style>

</style>
