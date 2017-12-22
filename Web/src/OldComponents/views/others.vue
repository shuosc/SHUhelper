<template>
  <v-container fluid grid-list-xs>
    <v-layout row wrap>
      <v-flex xs6 v-for="(item,index) in items" :key="index" class="pa-1">
        <v-card class="green darken-3 white--text" height="100px" hover @click="$router.push(item.url)">
          <v-card-title primary-title>{{item.name}}
            <v-spacer></v-spacer>
            <v-icon x-large dark :class="item.class">{{item.icon}}</v-icon>
            <i ></i>
          </v-card-title>
          <v-card-text></v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
export default {
  data () {
    return {
      items: [{
        name: '树洞',
        url: '/',
        class: 'iconfont icon-shu',
        icon: ''
      }, {
        name: '表白墙',
        url: '/',
        icon: 'favorite'
      }, {
        name: '留言板',
        url: '',
        class: 'iconfont icon-kaoshi',
        icon: ''
      }, {
        name: '校园安全地图',
        url: '',
        class: 'iconfont icon-baoan-copy',
        icon: ''
      }]
    }
  }
}
</script>
<style>

</style>
