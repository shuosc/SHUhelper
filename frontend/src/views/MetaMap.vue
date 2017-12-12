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
                      :content="marker.content"
                      :key="marker.oid"></el-amap-marker>
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
        },
        {
          visible: true,
          position: [121.38922, 31.316229],
          type: '',
          icon: 'food1',
          text: ''
        },
        {
          visible: true,
          position: [121.391333, 31.319318],
          type: '',
          icon: 'food1',
          text: ''
        },
        {
          visible: true,
          position: [121.388732, 31.317801],
          type: '',
          icon: 'food1',
          text: ''
        },
        {
          visible: true,
          position: [121.395775, 31.316531],
          type: '',
          icon: 'food1',
          text: ''
        },
        {
          visible: true,
          position: [121.389338, 31.310794],
          type: '',
          icon: 'food1',
          text: ''
        },
        {
          visible: true,
          position: [121.398415, 31.314776],
          type: '',
          icon: 'food1',
          text: ''
        },
        {
          visible: true,
          position: [121.392262, 31.316999],
          type: '',
          icon: 'book',
          text: ''
        },
        {
          visible: true,
          position: [121.388608, 31.316165],
          type: '',
          icon: 'shower',
          text: ''
        },
        {
          visible: true,
          position: [121.388399, 31.32012],
          type: '',
          icon: 'medkit',
          text: ''
        },
        {
          visible: true,
          position: [121.391677, 31.317178],
          type: '',
          icon: 'address-book',
          text: ''
        },
        {
          visible: true,
          position: [121.387434, 31.319918],
          type: '',
          icon: 'clipboard',
          text: ''
        },
        {
          visible: true,
          position: [121.38951, 31.320409],
          type: '',
          icon: 'fortawesome',
          text: ''
        },
        {
          visible: true,
          position: [121.390593, 31.320532],
          type: '',
          icon: 'building',
          text: ''
        },
        {
          visible: true,
          position: [121.395008, 31.320748],
          type: '',
          icon: 'school',
          text: ''
        },
        {
          visible: true,
          position: [121.396961, 31.313475],
          type: '',
          icon: 'government',
          text: ''
        },
        {
          visible: true,
          position: [121.394751, 31.313278],
          type: '',
          icon: 'envelope',
          text: ''
        },
        {
          visible: true,
          position: [121.394123, 31.319533],
          type: '',
          icon: 'swim',
          text: ''
        },
        {
          visible: true,
          position: [121.394649, 31.31968],
          type: '',
          icon: 'badmiton',
          text: ''
        },
        {
          visible: true,
          position: [121.395373, 31.319501],
          type: '',
          icon: 'stadium',
          text: ''
        },
        {
          visible: true,
          position: [121.394209, 31.318319],
          type: '',
          icon: 'music',
          text: ''
        },
        {
          visible: true,
          position: [121.39518, 31.3177],
          type: '',
          icon: 'class',
          text: ''
        },
        {
          visible: true,
          position: [121.393705, 31.312819],
          type: '',
          icon: 'art',
          text: ''
        },
        {
          visible: true,
          position: [121.389038, 31.312489],
          type: '',
          icon: 'tool',
          text: ''
        },
        {
          visible: true,
          position: [121.385905, 31.313026],
          type: '',
          icon: 'social',
          text: ''
        },
        {
          visible: true,
          position: [121.400346, 31.319946],
          type: '',
          icon: 'dna',
          text: ''
        },
        {
          visible: true,
          position: [121.399557, 31.319354],
          type: '',
          icon: 'chemistry',
          text: ''
        },
        {
          visible: true,
          position: [121.39945, 31.318333],
          type: '',
          icon: 'material',
          text: ''
        },
        {
          visible: true,
          position: [121.399825, 31.317416],
          type: '',
          icon: 'computer',
          text: ''
        },
        {
          visible: true,
          position: [121.399321, 31.316999],
          type: '',
          icon: 'communication',
          text: ''
        },
        {
          visible: true,
          position: [121.39871, 31.313337],
          type: '',
          icon: 'net',
          text: ''
        },
        {
          visible: true,
          position: [121.3993, 31.313323],
          type: '',
          icon: 'library',
          text: ''
        },
        {
          visible: true,
          position: [121.398951, 31.313026],
          type: '',
          icon: 'money',
          text: ''
        },
        {
          visible: true,
          position: [121.39666, 31.319359],
          type: '',
          icon: 'playground',
          text: ''
        },
        {
          visible: true,
          position: [121.393206, 31.319107],
          type: '',
          icon: 'playground',
          text: ''
        },
        {
          visible: true,
          position: [121.392363, 31.319309],
          type: '',
          icon: 'sport',
          text: ''
        },
        {
          visible: true,
          position: [121.387825, 31.317086],
          type: '',
          icon: 'sport',
          text: ''
        },
        {
          visible: true,
          position: [121.388142, 31.31518],
          type: '',
          icon: 'sport',
          text: ''
        },
        {
          visible: true,
          position: [121.389349, 31.31331],
          type: '',
          icon: 'sport',
          text: ''
        },
        {
          visible: true,
          position: [121.387745, 31.317865],
          type: '',
          icon: 'volleyball',
          text: ''
        },
        {
          visible: true,
          position: [121.392149, 31.319859],
          type: '',
          icon: 'volleyball',
          text: ''
        },
        {
          visible: true,
          position: [121.388565, 31.319235],
          type: '',
          icon: 'baseball',
          text: ''
        },
        {
          visible: true,
          position: [121.387868, 31.318896],
          type: '',
          icon: 'baseball',
          text: ''
        },
        {
          visible: true,
          position: [121.388367, 31.313887],
          type: '',
          icon: 'football',
          text: ''
        },
        {
          visible: true,
          position: [121.388453, 31.313255],
          type: '',
          icon: 'golf',
          text: ''
        },
        {
          visible: true,
          position: [121.390609, 31.319327],
          type: '',
          icon: 'food',
          text: ''
        },
        {
          visible: true,
          position: [121.388533, 31.315509],
          type: '',
          icon: 'schoolbus',
          text: ''
        },
        {
          visible: true,
          position: [121.389762, 31.319694],
          type: '',
          icon: 'schoolbus',
          text: ''
        },
        {
          visible: true,
          position: [121.389456, 31.312072],
          type: '',
          icon: 'schoolbus',
          text: ''
        },
        {
          visible: true,
          position: [121.393098, 31.318282],
          type: '',
          icon: 'schoolbus',
          text: ''
        },
        {
          visible: true,
          position: [121.397241, 31.31349],
          type: '',
          icon: 'schoolbus',
          text: ''
        },
        {
          visible: true,
          position: [121.395074, 31.311547],
          type: '',
          icon: 'bus',
          text: ''
        },
        {
          visible: true,
          position: [121.397917, 31.312423],
          type: '',
          icon: 'bus',
          text: ''
        },
        {
          visible: true,
          position: [121.397482, 31.317986],
          type: '',
          icon: 'bus',
          text: ''
        },
        {
          visible: true,
          position: [121.391303, 31.320855],
          type: '',
          icon: 'bus',
          text: ''
        },
        {
          visible: true,
          position: [121.38655, 31.320204],
          type: '',
          icon: 'bus',
          text: ''
        },
        {
          visible: true,
          position: [121.388878, 31.320608],
          type: '',
          icon: 'subway',
          text: ''
        }, {
          visible: true,
          position: [121.395524, 31.313619],
          type: '',
          icon: 'A',
          text: 'A',
          content: 'A'
        },
        {
          visible: true,
          position: [121.396645, 31.313981],
          type: '',
          icon: 'AJ',
          text: 'AJ',
          content: 'AJ'
        },
        {
          visible: true,
          position: [121.395133, 31.314072],
          type: '',
          icon: 'B',
          text: 'B',
          content: 'B'
        },
        {
          visible: true,
          position: [121.396248, 31.314407],
          type: '',
          icon: 'BJ',
          text: 'BJ',
          content: 'BJ'
        },
        {
          visible: true,
          position: [121.394779, 31.314512],
          type: '',
          icon: 'C',
          text: 'C',
          content: 'C'
        },
        {
          visible: true,
          position: [121.395905, 31.314824],
          type: '',
          icon: 'CJ',
          text: 'CJ',
          content: 'CJ'
        },
        {
          visible: true,
          position: [121.394473, 31.314916],
          type: '',
          icon: 'D',
          text: 'D',
          content: 'D'
        },
        {
          visible: true,
          position: [121.39561, 31.315227],
          type: '',
          icon: 'DJ',
          text: 'DJ',
          content: 'DJ'
        },
        {
          visible: true,
          position: [121.393792, 31.315402],
          type: '',
          icon: 'J',
          text: 'J',
          content: 'J'
        },
        {
          visible: true,
          position: [121.393985, 31.316121],
          type: '',
          icon: 'E',
          text: 'E',
          content: 'E'
        },
        {
          visible: true,
          position: [121.394934, 31.316245],
          type: '',
          icon: 'EJ',
          text: 'EJ',
          content: 'EJ'
        },
        {
          visible: true,
          position: [121.39369, 31.316575],
          type: '',
          icon: 'F',
          text: 'F',
          content: 'F'
        },
        {
          visible: true,
          position: [121.394623, 31.316712],
          type: '',
          icon: 'FJ',
          text: 'FJ',
          content: 'FJ'
        },
        {
          visible: true,
          position: [121.39333, 31.316978],
          type: '',
          icon: 'G',
          text: 'G',
          content: 'G'
        },
        {
          visible: true,
          position: [121.394264, 31.317143],
          type: '',
          icon: 'GJ',
          text: 'GJ',
          content: 'GJ'
        },
        {
          visible: true,
          position: [121.388846, 31.315429],
          type: '',
          icon: '1',
          text: '1',
          content: '1'
        },
        {
          visible: true,
          position: [121.389146, 31.315003],
          type: '',
          icon: '2',
          text: '2',
          content: '2'
        },
        {
          visible: true,
          position: [121.389377, 31.314613],
          type: '',
          icon: '3',
          text: '3',
          content: '3'
        },
        {
          visible: true,
          position: [121.390192, 31.31509],
          type: '',
          icon: '4',
          text: '4',
          content: '4'
        },
        {
          visible: true,
          position: [121.390348, 31.314668],
          type: '',
          icon: '5',
          text: '5',
          content: '5'
        },
        {
          visible: true,
          position: [121.396586, 31.316781],
          type: '',
          icon: 'HA',
          text: 'HA',
          content: 'HA'
        },
        {
          visible: true,
          position: [121.396849, 31.316391],
          type: '',
          icon: 'HB',
          text: 'HB',
          content: 'HB'
        },
        {
          visible: true,
          position: [121.39701, 31.315782],
          type: '',
          icon: 'HC',
          text: 'HC',
          content: 'HC'
        },
        {
          visible: true,
          position: [121.396216, 31.315864],
          type: '',
          icon: 'HD',
          text: 'HD',
          content: 'HD'
        },
        {
          visible: true,
          position: [121.396731, 31.315269],
          type: '',
          icon: 'HE',
          text: 'HE',
          content: 'HE'
        },
        {
          visible: true,
          position: [121.389865, 31.317863],
          type: '',
          icon: 'I',
          text: 'I',
          content: 'I'
        },
        {
          visible: true,
          position: [121.38965, 31.318573],
          type: '',
          icon: 'K',
          text: 'K',
          content: 'K'
        },
        {
          visible: true,
          position: [121.389307, 31.31888],
          type: '',
          icon: 'L',
          text: 'L',
          content: 'L'
        },
        {
          visible: true,
          position: [121.39002, 31.316194],
          type: '',
          icon: 'M',
          text: 'M',
          content: 'M'
        },
        {
          visible: true,
          position: [121.390219, 31.316552],
          type: '',
          icon: 'N',
          text: 'N',
          content: 'N'
        },
        {
          visible: true,
          position: [121.389736, 31.318183],
          type: '',
          icon: 'O',
          text: 'O',
          content: 'O'
        },
        {
          visible: true,
          position: [121.390069, 31.316854],
          type: '',
          icon: 'P',
          text: 'P',
          content: 'P'
        },
        {
          visible: true,
          position: [121.390251, 31.317207],
          type: '',
          icon: 'Q',
          text: 'Q',
          content: 'Q'
        },
        {
          visible: true,
          position: [121.390085, 31.317519],
          type: '',
          icon: 'R',
          text: 'R',
          content: 'R'
        },
        {
          visible: true,
          position: [121.388974, 31.316946],
          type: '',
          icon: 'S',
          text: 'S',
          content: 'S'
        },
        {
          visible: true,
          position: [121.388824, 31.317267],
          type: '',
          icon: 'T',
          text: 'T',
          content: 'T'
        },
        {
          visible: true,
          position: [121.392027, 31.318422],
          type: '',
          icon: 'U',
          text: 'U',
          content: 'U'
        },
        {
          visible: true,
          position: [121.388792, 31.318202],
          type: '',
          icon: 'V',
          text: 'V',
          content: 'V'
        },
        {
          visible: true,
          position: [121.39171, 31.318752],
          type: '',
          icon: 'W',
          text: 'W',
          content: 'W'
        },
        {
          visible: true,
          position: [121.391158, 31.318202],
          type: '',
          icon: 'X',
          text: 'X',
          content: 'X'
        },
        {
          visible: true,
          position: [121.3909, 31.318518],
          type: '',
          icon: 'Y',
          text: 'Y',
          content: 'Y'
        },
        {
          visible: true,
          position: [121.390589, 31.31899],
          type: '',
          icon: 'Z',
          text: 'Z',
          content: 'Z'
        }, {
          visible: true,
          position: [121.389403, 31.308302],
          type: '',
          icon: '1',
          text: '1',
          content: '1'
        },
        {
          visible: true,
          position: [121.388835, 31.30833],
          type: '',
          icon: '2',
          text: '2',
          content: '2'
        },
        {
          visible: true,
          position: [121.389532, 31.308637],
          type: '',
          icon: '3',
          text: '3',
          content: '3'
        },
        {
          visible: true,
          position: [121.388787, 31.308678],
          type: '',
          icon: '4',
          text: '4',
          content: '4'
        },
        {
          visible: true,
          position: [121.389452, 31.309068],
          type: '',
          icon: '5',
          text: '5',
          content: '5'
        },
        {
          visible: true,
          position: [121.38876, 31.309031],
          type: '',
          icon: '6',
          text: '6',
          content: '6'
        },
        {
          visible: true,
          position: [121.3895, 31.309457],
          type: '',
          icon: '7',
          text: '7',
          content: '7'
        },
        {
          visible: true,
          position: [121.388652, 31.309407],
          type: '',
          icon: '8',
          text: '8',
          content: '8'
        },
        {
          visible: true,
          position: [121.389452, 31.309874],
          type: '',
          icon: '9',
          text: '9',
          content: '9'
        },
        {
          visible: true,
          position: [121.38862, 31.309847],
          type: '',
          icon: '10',
          text: '10',
          content: '10'
        },
        {
          visible: true,
          position: [121.389382, 31.310356],
          type: '',
          icon: '11',
          text: '11',
          content: '11'
        },
        {
          visible: true,
          position: [121.388433, 31.310434],
          type: '',
          icon: '12',
          text: '12',
          content: '12'
        },
        {
          visible: true,
          position: [121.388497, 31.310883],
          type: '',
          icon: '14',
          text: '14',
          content: '14'
        }, {
          visible: true,
          position: [121.386641, 31.31482],
          type: '',
          icon: '1',
          text: '1',
          content: '1'
        },
        {
          visible: true,
          position: [121.386952, 31.314545],
          type: '',
          icon: '2',
          text: '2',
          content: '2'
        },
        {
          visible: true,
          position: [121.386405, 31.314522],
          type: '',
          icon: '3',
          text: '3',
          content: '3'
        },
        {
          visible: true,
          position: [121.38699, 31.31426],
          type: '',
          icon: '4',
          text: '4',
          content: '4'
        },
        {
          visible: true,
          position: [121.386421, 31.314219],
          type: '',
          icon: '5',
          text: '5',
          content: '5'
        },
        {
          visible: true,
          position: [121.387022, 31.313972],
          type: '',
          icon: '6',
          text: '6',
          content: '6'
        },
        {
          visible: true,
          position: [121.386426, 31.31393],
          type: '',
          icon: '7',
          text: '7',
          content: '7'
        },
        {
          visible: true,
          position: [121.387022, 31.313665],
          type: '',
          icon: '8',
          text: '8',
          content: '8'
        },
        {
          visible: true,
          position: [121.386378, 31.313633],
          type: '',
          icon: '9',
          text: '9',
          content: '9'
        },
        {
          visible: true,
          position: [121.387027, 31.313362],
          type: '',
          icon: '10',
          text: '10',
          content: '10'
        },
        {
          visible: true,
          position: [121.386201, 31.313046],
          type: '',
          icon: '11',
          text: '11',
          content: '11'
        },
        {
          visible: true,
          position: [121.387075, 31.312794],
          type: '',
          icon: '12',
          text: '12',
          content: '12'
        },
        {
          visible: true,
          position: [121.387118, 31.312519],
          type: '',
          icon: '14',
          text: '14',
          content: '14'
        },
        {
          visible: true,
          position: [121.38648, 31.312473],
          type: '',
          icon: '15',
          text: '15',
          content: '15'
        },
        {
          visible: true,
          position: [121.387134, 31.312212],
          type: '',
          icon: '16',
          text: '16',
          content: '16'
        },
        {
          visible: true,
          position: [121.386593, 31.312189],
          type: '',
          icon: '17',
          text: '17',
          content: '17'
        },
        {
          visible: true,
          position: [121.38737, 31.311882],
          type: '',
          icon: '18',
          text: '18',
          content: '18'
        },
        {
          visible: true,
          position: [121.386877, 31.311744],
          type: '',
          icon: '19',
          text: '19',
          content: '19'
        },
        {
          visible: true,
          position: [121.387054, 31.311474],
          type: '',
          icon: '20',
          text: '20',
          content: '20'
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
<style scoped>
.amap-page-container {
  height: 90%;
}
</style>
