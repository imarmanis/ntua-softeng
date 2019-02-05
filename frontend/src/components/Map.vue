<template>
  <div id="map">
    <l-map :zoom="zoom" :center="center"
    @contextmenu="rightClick">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker :lat-lng="coordinates">
        <l-popup>{{ coordinates }}</l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<script>
import { L, LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet';
import { bus } from '../main'

export default {
  components: {
        'l-map': LMap,
        'l-tile-layer': LTileLayer,
        'l-marker': LMarker,
        'l-popup': LPopup
    },
  data() {
    return {
      zoom: 20,
      center: L.latLng(37.983917, 23.72936),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      coordinates: L.latLng(37.983917, 23.72936),
    }
  },
  methods: {
    rightClick: function(event) {
      this.coordinates = event.latlng;
      const temp = [];
      temp[0] = event.latlng.lat;
      temp[1] = event.latlng.lng;
      bus.$emit('coordChanged',temp);
    }
  }
}
</script>

<style scoped>
#map {
  height: 380px;
  width: 600px;
  margin: 0;
}
</style>
