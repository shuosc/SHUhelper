<template lang="pug">
  map(id="map" :longitude="longitude" :latitude="latitude" :markers="markers" scale="19" show-location style="width: 100%; height: 100vh;")
</template>
<script>
export default {
  mounted: function() {
    this.longitude = this.$root.$mp.query.longitude
    this.latitude = this.$root.$mp.query.latitude
  },
  data() {
    return {
      longitude: 0,
      latitude: 0
    }
  },
  computed: {
    markers: function() {
      return [
        {
          iconPath: '/static/marker.png',
          id: 0,
          latitude: this.latitude,
          longitude: this.longitude,
          width: 50,
          height: 50
        }
      ]
    }
  }
}
</script>
