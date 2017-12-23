<template>
  <v-container fluid grid-list-xs>
    <v-layout row wrap>
      <v-flex xs12 v-for="(item,index) in items" :key="index" class="pa-1">
        <v-card class="green darken-3 white--text"  hover @click="$router.push(item.url)">
          <v-card-title primary-title>{{item.name}}</v-card-title>
          <v-card-text></v-card-text>
          <v-list two-line>
            <v-list-tile>
              <v-list-tile-action>
                <v-icon class="indigo--text">phone</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>(650) 555-1234</v-list-tile-title>
                <v-list-tile-sub-title>Mobile</v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-icon dark>chat</v-icon>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider inset></v-divider>
            <v-list-tile>
              <v-list-tile-action>
                <v-icon class="indigo--text">mail</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>aliconnors@example.com</v-list-tile-title>
                <v-list-tile-sub-title>Personal</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-divider inset></v-divider>
            <v-list-tile>
              <v-list-tile-action>
                <v-icon class="indigo--text">location_on</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>1400 Main Street</v-list-tile-title>
                <v-list-tile-sub-title>Orlando, FL 79938</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
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
