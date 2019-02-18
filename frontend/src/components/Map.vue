<template>
  <div id="map">
    <l-map ref="map" :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <v-geosearch :options="geosearchOptions"></v-geosearch>
    </l-map>
  </div>
</template>

<script>
import { L, LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import VGeosearch from 'vue2-leaflet-geosearch';
import { bus } from '../main'

export default {
  components: {
        VGeosearch,
        'l-map': LMap,
        'l-tile-layer': LTileLayer,
    },
  data() {
    return {
      zoom: 20,
      center: L.latLng(37.983917, 23.72936),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      coordinates: [],
      address: null,
      geosearchOptions: {
        provider: new OpenStreetMapProvider(),
        style: 'bar',
        autoComplete: true,
        showMarker: true,
        showPopup: false,
        marker: {
          icon: new L.Icon.Default(),
          draggable: true,
        },
        maxMarkers: 1,
        autoClose: true,
        searchLabel: 'Προσθήκη Διεύθυνσης',
        keepResult: true
      },
    }
  },
  methods: {
    showlocation: function(event) {
      this.coordinates[0] = event.location.y;  // lat
      this.coordinates[1] = event.location.x;  // lng
      this.address = event.location.label;
      const temp = [];
      temp[0] = this.coordinates[0];
      temp[1] = this.coordinates[1];
      temp[2] = this.address;
      bus.$emit('markerChanged',temp);
    },
    dragged: function(event){
      this.coordinates[0] = event.location.lat;  // lat
      this.coordinates[1] = event.location.lng;  // lng
      const temp = [];
      temp[0] = this.coordinates[0];
      temp[1] = this.coordinates[1];
      temp[2] = this.address;
      bus.$emit('markerChanged',temp);
    },
  },
  mounted(){
    this.$refs.map.mapObject.on('geosearch/showlocation', this.showlocation);
    this.$refs.map.mapObject.on('geosearch/marker/dragend', this.dragged);
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
