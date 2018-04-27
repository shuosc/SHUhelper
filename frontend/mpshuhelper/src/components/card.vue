<template lang="pug">
  div
    p.card {{text}}
</template>

<script>
export default {
  props: ['text']
}
</script>

<style>
.card {
  padding: 10px;
}
</style>
