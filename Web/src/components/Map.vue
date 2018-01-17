<template lang="pug">
  div(style="padding-botom:51px;width:100%", ref="map")
    <q-toolbar color="primary">
      <q-btn slot="left" flat round small class="primary" v-back>
          <q-icon name="keyboard_backspace" /></q-btn>
      <q-toolbar-title>
        | 地图
      </q-toolbar-title>
    </q-toolbar>
    q-card.container
      el-amap.box(:center="center", :amap-manager="amapManager", :zoom="zoom", :resize-enable="true", :events="events", :plugin="plugin", viewMode="3D")
        el-amap-ground-image(v-for="groundimage in groundimages" :key="groundimage.url" :url="groundimage.url" :bounds="groundimage.bounds" :events="groundimage.events")
</template>

<script>
export default {
  created() {
    // console.log(window.history)
  },
  data() {
    let amapManager = new this.$map.AMapManager()
    return {
      amapManager,
      zoom: 17,
      center: [121.393351, 31.3160044],
      groundimages: [
        {
          url: '/statics/map.jpg',
          bounds: [[121.38551, 31.306444], [121.40551, 31.32525044]],
          events: {
            click() {
              alert('click groundimage')
            }
          }
        }
      ],
      plugin: [
        { pName: 'Scale' },
        {
          pName: 'Geolocation',
          buttonPosition: 'RB',
          buttonDom:
            '<button class="q-btn row inline flex-center q-focusable q-hoverable relative-position q-btn-round q-btn-small bg-primary text-white" style="z-index: 2"><div class="desktop-only q-focus-helper"></div><span class="q-btn-inner row col flex-center"><i aria-hidden="true" class="q-icon material-icons">my_location</i></span></button>',
          GeoLocationFirst: true,
          events: {
            init(map) {
              map.getCurrentPosition((status, result) => {
                console.log(result)
              })
            }
          }
        }
      ],
      events: {
        init(map) {
          map.setFeatures(['bg', 'road', 'building'])
        }
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.amap-geolocation-con
  z-index 2 !important

.amap-logo
  display none

.amap-copyright
  display none !important

.box
  height 100%
  width 100%

.container
  height 65vh
  margin 10px
</style>

