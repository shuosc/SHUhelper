<template>
  <v-app>
    <v-navigation-drawer
      :clipped="false"
      app
      fixed
      v-model="drawer"
    >
      <v-list>
        <v-list-tile
          :key="i"
          :to="item.to"
          exact
          router
          v-for="(item, i) in items"
        >
          <v-list-tile-action>
            <v-icon v-html="item.icon"/>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title"/>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      :clipped-left="false"
      app
      fixed
    >
      <v-toolbar-side-icon @click="drawer = !drawer"/>
      <v-toolbar-title>{{title}}</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container>
        <nuxt/>
      </v-container>
    </v-content>
    <v-footer
      :fixed="false"
      app
    >
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
  export default {
    data() {
      return {
        drawer: true,
        items: [
          { icon: 'apps', title: 'Welcome', to: '/' },
          { icon: 'bubble_chart', title: 'Inspire', to: '/inspire' }
        ],
        title: 'SHUHelper'
      };
    }
  };
</script>
