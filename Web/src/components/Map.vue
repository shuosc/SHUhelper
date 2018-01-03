<template lang="pug">
  div(style="padding-botom:51px;width:100%", ref="map")
    q-card.container
      el-amap.box(:center="center", :amap-manager="amapManager", :zoom="zoom", :resize-enable="true", :events="events", :plugin="plugin", viewMode="3D")
</template>

<script>
  export default {
    data() {
      let amapManager = new this.$map.AMapManager()
      return {
        amapManager,
        zoom: 17,
        center: [121.393351, 31.3160044],
        plugin: [
          {pName: 'Scale'},
          {
            pName: 'Geolocation',
            buttonPosition: 'RB',
            buttonDom: '<button class="q-btn row inline flex-center q-focusable q-hoverable relative-position q-btn-round q-btn-small bg-primary text-white" style="z-index: 2"><div class="desktop-only q-focus-helper"></div><span class="q-btn-inner row col flex-center"><i aria-hidden="true" class="q-icon material-icons">my_location</i></span></button>',
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
    },
    mounted() {
    }
  }
</script>

<style lang="stylus">
  .amap-geolocation-con {
    z-index: 2 !important;
  }

  .amap-logo {
    display: none;
  }

  .amap-copyright {
    display: none !important;
  }
</style>

<style lang="stylus" scoped>
  .box {
    height: 100%;
    width: 100%;
  }

  .container {
    height: 65vh;
    margin: 10px;
  }
</style>

