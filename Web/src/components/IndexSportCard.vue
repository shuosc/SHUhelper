<template lang="pug">
  div
    q-card.namecard
      q-card-main
        q-item
          q-item-side
            q-icon(color='primary', name='fa-tiyujiankang', style='font-size:2rem;')
          q-item-main
            q-item-tile(label='') 晨跑查询稍后上线~
            q-item-tile(sublabel='') 
      q-card-separator
      q-card-actions
        q-btn.full-width(flat @click="open()")
          | 查看本学期课外活动表（图片）
    q-modal(ref="activitiesTable" :content-css="{minWidth: '80vw', minHeight: '80vh'}")
      q-modal-layout
        q-toolbar(slot="header" color="primary")
          q-btn(color="white" flat @click="close")
            q-icon(name="close")
            q-toolbar-title
              | 课外活动表
        div(v-if="activitiesTableOpen")
          img.responsive(src="/statics/activities_17_2.jpg")
</template>

<script>
export default {
  name: 'sportCard',
  data() {
    return {
      activitiesTableOpen: false
    }
  },
  created() {
  },
  methods: {
    open() {
      this.activitiesTableOpen = true
      this.$refs.activitiesTable.open()
    },
    close() {
      this.activitiesTableOpen = false
      this.$refs.activitiesTable.close()
    }
  }
}
</script>

<style>

</style>
