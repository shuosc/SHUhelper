<template>
  <div class="amap-page-container">
    <el-amap :vid="'amap-vue'"
             :center="center"
             :zoom="zoom"
             :map-manager="amapManager"
             :plugin="plugin"
             :events="events">
      <el-amap-info-window 
                           :position="window.position"
                           :content="window.content"
                           :events="window.events"
                           :visible="window.open"></el-amap-info-window>
      <el-amap-marker :position="firstMarker.position"
                      :events="firstMarker.events"
                      :visible="firstMarker.visible"
                      :draggable="firstMarker.draggable"
                      :content="firstMarker.content"></el-amap-marker>
      <el-amap-marker v-for="marker in markers"
                      :position="marker.position"
                      :events="marker.events"
                      :visible="marker.visible"
                      :draggable="marker.draggable"></el-amap-marker>
    </el-amap>
    <button type="button"
            name="button"
            @click="addMarker">添加安全事件</button>
    <button @click="window.open=!window.open">window</button>
      <popup :value="showAddForm"
             height="400px"
             @on-hide="showAddForm=false">
        <group>
          <x-input title="事件标题"
                   v-model="submitForm.title"
                   placeholder="简要描述事件"></x-input>
          <selector title="事件类型"
                    v-model="submitForm.type"
                    :options="types"></selector>
          <datetime v-model="submitForm.datetime"
                    title="发生时间"
                    format="YYYY-MM-DD HH:mm"
                    year-row="{value}年"
                    month-row="{value}月"
                    day-row="{value}日"
                    hour-row="{value}点"
                    minute-row="{value}分"
                    confirm-text="完成"
                    cancel-text="取消"></datetime>
          <x-input title="经纬度"
                   v-model="submitForm.Location"
                   disabled></x-input>
          <x-input title="详细地点"
                   v-model="submitForm.detailedLocation"
                   placeholder="如某楼某层某教室或某某路"></x-input>
          <x-textarea title="详情描述"
                      v-model="submitForm.detail"
                      placeholder="关于事件更详细的描述"></x-textarea>
          <x-button type="primary"
                    @click.native="submit">提交</x-button>
  
        </group>
      </popup>
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
      submitForm: {
        title: '',
        type: '',
        location: [],
        datetime: undefined,
        detail: '',
        detailedLocation: ''
      },
      window: {
        position: [121.393351, 31.3160044],
        content: 'Hi! I am here!',
        open: true,
        events: {
          close() {
            console.log('close infowindow')
          }
        }
      },
      types: ['广东', '广西'],
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
      showAddForm: false,
      amapManager: amapManager,
      firstMarker: {
        visible: false,
        position: [121.393351, 31.3160044],
        draggable: true,
        events: {
          click: () => {
            this.window.open = true
          },
          dragend: (e) => {
            this.firstMarker.position = [e.lnglat.lng, e.lnglat.lat]
          }
        },
        content: '<i style="color:red;"class="iconfont icon-shu"></i>'
      },
      currentMarker: {
        visible: false,
        position: [121.393351, 31.3160044],
        draggable: true,
        events: {
          click: () => {
            this.showAddForm = true
          },
          dragend: (e) => {
            this.firstMarker.position = [e.lnglat.lng, e.lnglat.lat]
          }
        },
        content: '<i style="color:red;"class="iconfont icon-shu"></i>'
      },
      markers: [
        {
          position: [121.393351, 31.3160044],
          type: '',
          content: '<i style="color:red;"class="iconfont icon-shu"></i>',
          text: ''
        }
      ]
    }
  },
  methods: {
    getMap: function () {
      console.log(this.amapManager.getMap())
      console.log(this.center)
      return this.amapManager.getMap()
    },
    addMarker: function () {
      this.firstMarker.position = this.center
      this.firstMarker.visible = true
    },
    addZoom() {
      this.zoom++
    },
    subZoom() {
      this.zoom--
    },
    changeCenter() {
      // this.center = [this.center[0] + 0.1, this.center[1] + 0.1]
      console.log(this.center)
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
