<template>
  <div>
    <v-list>
      <template v-for="item in lists">
        <v-list-tile v-if="item.action" v-bind:key="item.title">
          <v-list-tile-action>
            <v-icon light>{{ item.action }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content class="black--text">
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-divider v-else-if="item.divider" light></v-divider>
        <v-subheader v-else-if="item.header" v-text="item.header" class="teal--text text--lighten-2"></v-subheader>
      </template>
    </v-list>
  </div>
</template>
<script>
export default {
  data () {
    return {
      items: [
        { header: 'Today' },
        { avatar: '/static/doc-images/lists/1.jpg', title: 'Brunch this weekend?', subtitle: "<span class='grey--text text--darken-2'>Ali Connors</span> — I'll be in your neighborhood doing errands this weekend. Do you want to hang out?" },
        { divider: true, inset: true },
        { avatar: '/static/doc-images/lists/2.jpg', title: 'Summer BBQ <span class="grey--text text--lighten-1">4</span>', subtitle: "<span class='grey--text text--darken-2'>to Alex, Scott, Jennifer</span> — Wish I could come, but I'm out of town this weekend." },
        { divider: true, inset: true },
        { avatar: '/static/doc-images/lists/3.jpg', title: 'Oui oui', subtitle: "<span class='grey--text text--darken-2'>Sandra Adams</span> — Do you have Paris recommendations? Have you ever been?" }
      ],
      lists: [
        { header: '上海大学' },
        { divider: true },
        {
          action: 'move_to_inbox',
          title: this.$store.state.user.name
        },
        {
          action: 'send',
          title: this.$store.state.user.card_id
        },
        {
          action: 'delete',
          title: '消息'
        },
        {
          action: 'report',
          title: 'Spam'
        },
        { divider: true },
        { header: 'Labels' },
        {
          action: 'label',
          title: '清除缓存'
        },
        {
          action: 'label',
          title: '关于我们'
        }
      ]
    }
  }
}
</script>
<style lang="stylus">

</style>
