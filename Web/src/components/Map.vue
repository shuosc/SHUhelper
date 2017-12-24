<template lang="pug">
  div(style="padding-botom:51px;width:100%" ref='map')
    q-card.container
      el-amap.box(:center='center' :zoom='zoom' :map-manager='amapManager' :resizeEnable='true' :events='events' :plugin='plugin')
</template>

<script>
  export default {
    data() {
      // let that = this
      let amapManager = new this.$map.AMapManager()
      return {
        amapManager,
        zoom: 17,
        center: [121.393351, 31.3160044],
        plugin: [
          // { pName: 'Scale' },
          // {
          //   pName: 'Geolocation',
          //   events: {
          //     init(o) {
          //       o.getCurrentPosition((status, result) => {
          //         if (result && result.position) {
          //           console.log(status)
          //           console.log(result)
          //           that.$nextTick()
          //         }
          //       })
          //     }
          //   }
          // }
        ],
        events: {
          init(map) {
            map.setFeatures(['bg', 'road', 'building'])
          }
        }
      }
    },
    mounted() {
      // console.log(this.amapManager)
    }
  }
</script>

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

