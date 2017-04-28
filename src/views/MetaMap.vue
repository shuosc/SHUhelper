<template>
  <div class="amap-page-container">
    <el-amap :vid="'amap-vue'"
             :center="center"
             :zoom="zoom"
             :map-manager="amapManager"
             :plugin="plugin"
             :events="events">
      <el-amap-info-window :position="window.position"
                           :content="window.content"
                           :events="window.events"
                           :visible="window.open"></el-amap-info-window>
      <el-amap-marker v-for="marker in markers"
                      :position="marker.position"
                      :visible="marker.visible"
                      :content="marker.content"></el-amap-marker>
    </el-amap>
    <button @click="changeDisplayType('')">changeDisplayType</button>
  </div>
</template>
<script>
import { AMapManager } from 'vue-amap'
import { Popup, Datetime, Group, Selector, XButton, XTextarea, XInput } from 'vux'
let amapManager = new AMapManager()
export default {
  components: {
    Popup, Datetime, Group, Selector, XButton, XTextarea, XInput
  },
  name: 'amap-page',
  data: function () {
    return {
      vid: 'amap-vue-1',
      zoom: 17,
      window: {
        position: [121.393351, 31.3160044],
        content: 'Hi! I am here!',
        open: false,
        events: {
          close() {
            console.log('close infowindow')
          }
        }
      },
      center: [121.393351, 31.3160044],
      events: {
        'moveend': () => {
          let mapCenter = this.amapManager.getMap().getCenter()
          this.center = [mapCenter.getLng(), mapCenter.getLat()]
        },
        'zoomchange': () => {
          this.zoom = this.amapManager.getMap().getZoom()
        }
      },
      plugin: [],
      amapManager: amapManager,
      markers: [
        {
          visible: true,
          position: [121.393351, 31.3160044],
          type: '',
          content: '<i style="color:red;"class="iconfont icon-shu"></i>',
          text: ''
        }
      ]
    }
  },
  methods: {
    changeDisplayType(type) {
      for (var i = 0; i < this.markers.length; i++) {
        if (this.makers[i].type !== type) {
          this.markers[i].visible = false
        }
      }
    },
    displayAll() {
      for (var i = 0; i < this.markers.length; i++) {
        this.markers[i].visible = true
      }
    },
    addZoom() {
      this.zoom++
    },
    subZoom() {
      this.zoom--
    },
    setFeatures() {
      var map = this.amapManager.getMap()
      var features = ['bg', 'road', 'building']
      map.setFeatures(features)
    }
  }
}
</script>
<style>
.amap-page-container {
  height: 90%;
}
</style>
