<template lang="pug">
  q-card
    q-card-main.text-center
      q-item
        q-item-side.text-center.flex
          q-icon(color='primary', name='fa-map-o', style='font-size:2rem;')
        q-item-main
          q-item-tile(label) 校园地图
          q-item-tile(sublabel)
            | 给在自己学校也找不到路的你
            br
            | 查看可能需要消耗很多流量(~2M)
    q-card-separator
    q-card-actions
      q-btn.full-width(style='padding:0 !important;' flat @click="$router.push('/map')")
        | 查看校园地图
</template>

<script>
export default {}
</script>

<style>

</style>
