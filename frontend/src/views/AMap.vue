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
      <el-amap-marker :position="firstMarker.position"
                      :events="firstMarker.events"
                      :visible="firstMarker.visible"
                      :draggable="firstMarker.draggable"
                      :content="firstMarker.content"
                      :icon="firstMarker.icon"
                      :offset="firstMarker.offset"
                      :raiseOnDrag="true"></el-amap-marker>
      <el-amap-marker v-for="marker in markers"
                      :position="marker.position"
                      :events="marker.events"
                      :visible="true"
                      :draggable="false"
                      :key="marker.oid"></el-amap-marker>
    </el-amap>
    <div style="position:fixed;left:0px;right:0;bottom:70px;">
      <div style="float:right;display:inline-block;margin-right:10px;border-radius: 40px;width:40px;height:40px;background-color: rgba(200, 134, 200, 0.80);"
           @click="$vux.alert.show({
                        title: '使用说明',
                        content: '拖动红色标记到目标位置<br/>点击标记可以添加事件<br/>点击已有事件标记可以查看详情<br/>默认显示两个月内的所有事件'
                      })">
        <h1 style="text-align:center;color:white;margin:auto;padding:0;font-size:1.5rem;">？</h1>
      </div>
      <div style="margin-right:10px;float:right;border-radius: 40px;width:40px;height:40px;background-color: rgba(200, 134, 200, 0.80);"
           @click="$vux.alert.show({
                        title: '武保处值班室电话',
                        content: '宝山武保处值班室电话：66134278<br/>延长武保处值班室电话：56331897<br/>嘉定武保处值班室电话：69982400'
                      })">
        <i class="iconfont icon-baoan" style="display:block;margin-left:10px;text-align:center;color:white;margin:auto;padding:0;font-size:1.5rem;"></i>
        </div>
    </div>
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
                 :value="firstMarker.position.toString()"
                 readonly
                 disabled></x-input>
        <x-input title="详细地点"
                 v-model="submitForm.detailedLocation"
                 placeholder="如某楼某层某教室或某某路"></x-input>
        <x-textarea title="详情描述"
                    v-model="submitForm.detail"
                    placeholder="关于事件更详细的描述"></x-textarea>
        <x-button type="primary"
                  @click.native="submitEvent">提交</x-button>
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
        position: [],
        datetime: undefined,
        detail: '',
        detailedLocation: ''
      },
      window: {
        position: [121.393351, 31.3160044],
        content: '<p>标题：Hi! I am here!</p><p>事件分类：Hi! I am here!</p><p>发生时间：Hi! I am here!</p><p>详细地点：Hi! I am here!</p><p>事件详情：Hi! I am here!</p>',
        open: false,
        events: {
          'close': () => {
            this.window.open = false
          }
        }
      },
      types: ['财物失窃', '可疑人士', '可疑事件', '交通事故', '消防事故', '人身安全', '其他事件'],
      center: [121.393351, 31.3160044],
      events: {
        'dragging': () => {
          // let mapCenter = this.amapManager.getMap().getCenter()
          // var center = [mapCenter.getLng(), mapCenter.getLat()]
          // this.firstMarker.position = center
        },
        'moveend': () => {
          let mapCenter = this.amapManager.getMap().getCenter()
          this.center = [mapCenter.getLng(), mapCenter.getLat()]
          this.firstMarker.position = this.center
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
        offset: [-15, -20],
        content: '<img src="/static/pin.png" >',
        icon: '/static/pin.png',
        events: {
          click: () => {
            this.showAddForm = true
          },
          dragend: (e) => {
            this.firstMarker.position = [e.lnglat.lng, e.lnglat.lat]
            this.$vux.toast.show({
              position: 'top',
              type: 'text',
              text: '点击红色标记添加事件'
            })
          }
        }
      },
      currentMarkerOid: '',
      markers: [],
      markEvents: {}
    }
  },
  created: function () {
    this.getEvents()
    this.addMarker()
    this.$vux.toast.show({
      position: 'top',
      type: 'text',
      text: '拖拽红色标记到目标地点'
    })
  },
  methods: {
    onMarkerClick(oid) {
      if (this.window.open === true) {
        this.window.open = false
      }
      this.currentMarkerOid = oid
      this.window.position = this.markEvents[oid].position
      var content = ''
      var date = new Date(this.markEvents[oid].datetime)
      date.setMinutes(date.getMinutes() + date.getTimezoneOffset())
      date = (date.getMonth() + 1) + '/' + date.getDate() + ' ' + date.getHours() + ':' + date.getMinutes()
      content += '<p>标题：' + this.markEvents[oid].title + '</p>'
      content += '<p>事件分类：' + this.markEvents[oid].type + '</p>'
      content += '<p>发生时间：' + date + '</p>'
      content += '<p>详细地点：' + this.markEvents[oid].detailedLocation + '</p>'
      content += '<p>事件详情：' + this.markEvents[oid].detail + '</p>'
      this.window.content = content
      this.window.open = true
    },
    submitEvent: function () {
      // var _this = this
      this.$http.post('/api/security-map/new', {
        'title': this.submitForm.title,
        'event_type': this.submitForm.type,
        'position': this.firstMarker.position,
        'datetime': this.submitForm.datetime,
        'detailed_location': this.submitForm.detailedLocation,
        'detail': this.submitForm.detail
      })
        .then((response) => {
          if (response.data.success) {
            this.showAddForm = false
            this.$vux.toast.show({
              position: 'bottom',
              type: 'text',
              text: '发送成功'
            })
            this.getEvents()
          }
        })
    },
    getEvents: function () {
      var _this = this
      this.$http.get('/api/security-map/latest')
        .then((response) => {
          this.markers = []
          this.markEvents = {}
          function a(oid) {
            return function () {
              _this.onMarkerClick(oid)
            }
          }
          for (var oid in response.data) {
            this.markEvents[oid] = response.data[oid]
            var event = this.markEvents[oid]
            event.events = {
              'click': a(oid)
            }
            this.markers.push(event)
          }
        })
    },
    getMap: function () {
      console.log(this.amapManager.getMap())
      console.log(this.center)
      return this.amapManager.getMap()
    },
    addMarker: function () {
      this.firstMarker.position = this.center
      this.firstMarker.visible = true
      this.$vux.toast.show({
        position: 'top',
        type: 'text',
        text: '标记点已置于屏幕中央'
      })
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
<style scoped>
.amap-page-container {
  height: 100%;
}
</style>
