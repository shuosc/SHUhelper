<template>
  <v-container>
    <v-layout row wrap style="text-align:center;">
      <v-flex xs12>
        <h4>您正在前往...</h4>
      </v-flex>
      <v-flex xs12>
        <v-card>
          <v-flex xs12 style="text-align:center;">
            <v-icon x-large>iconfont-paw</v-icon>
          </v-flex>
          <v-flex xs12>
            <h3>{{link.title}}</h3>
          </v-flex>
          <v-flex xs12 class="pb-3" style="color:grey">{{link.URL}}</v-flex>
          <v-flex xs12>
            <p v-html="link.desc"></p>
          </v-flex>
          <v-card-actions>
            <v-btn primary large block  :href="link.URL" target="_blank">直接访问</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      link: {
        icon: 'iconfont-paw',
        URL: 'https://SHUer.link',
        title: '上大导航',
        desc: '上大导航是为上大师生量身定做的导航网站<br/>目前由开源社区维护'
      }
    }
  },
  created () {
    this.getInfo()
  },
  methods: {
    getInfo () {
      this.$http.get(`/api/v1/link/${this.$route.params.id}`)
        .then((response) => {
          this.link = response.data
        })
    }
  }
}
</script>

<style>

</style>
