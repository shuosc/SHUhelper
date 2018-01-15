<template>
  <q-card class="full-width" flat style="margin:0;">
    <q-card-main style="text-align:left;" class="title">
      {{news.title}}
    </q-card-main>
    <q-card-separator />
  </q-card>
</template>

<script>
export default {
  props: {
    news: Object
  },
  data() {
    return { open: false }
  }
}
</script>

<style scoped>
.title {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
