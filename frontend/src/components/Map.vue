<template>
  <div id="map">
    <link rel="stylesheet" href="https://unpkg.com/leaflet-geosearch@2.6.0/assets/css/leaflet.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet.locatecontrol/dist/L.Control.Locate.min.css" />

    <l-map ref="map" :zoom="zoom" :center="center" @contextmenu="rightClick">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <v-geosearch v-if="withGeocoding" :options="geosearchOptions"></v-geosearch>
      <l-marker ref="dataMarkers" v-for="d in data" @click="markerSelected($event, d)" :key="d.id" :lat-lng="d.latlng">
        <l-popup v-if="d.name"> {{ d.name }}</l-popup>
      </l-marker>
      <l-marker v-if="clickedPos" :lat-lng="clickedPos" :icon="redMarkerIcon"></l-marker>
    </l-map>
  </div>
</template>

<script>
import { L, LMap, LTileLayer, LMarker, LPopup} from 'vue2-leaflet';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import VGeosearch from 'vue2-leaflet-geosearch';
import 'leaflet.locatecontrol';

export default {
  components: {
        VGeosearch,
        'l-map': LMap,
        'l-tile-layer': LTileLayer,
        'l-marker' : LMarker,
        'l-popup' : LPopup
    },
  props: {
    withLocation: Boolean,
    withGeocoding: Boolean,
    withRclick: Boolean,
    data: Array
  },
  data() {
    return {
      zoom: 6,
      center: L.latLng(38.757264, 22.468469), // default center ~= middle of greece
      clickedPos : null,
      redMarkerIcon : new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      }),
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
    rightClick: function(event) {
        if(!this.withRclick) return;
        this.clickedPos = L.latLng(event.latlng.lat, event.latlng.lng);
        this.$emit('rclickedPos', this.clickedPos);
    },
    markerSelected : function(e, x) {
      this.$emit('markerSelected', x);
      this.$refs.dataMarkers.forEach((m) => {
        m.mapObject.setIcon(new L.Icon.Default());
      });
      e.target.setIcon(new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      }));
    },
    showlocation: function(event) {
      this.coordinates[0] = event.location.y;  // lat
      this.coordinates[1] = event.location.x;  // lng
      this.address = event.location.label;
      const temp = [];
      temp[0] = this.coordinates[0];
      temp[1] = this.coordinates[1];
      temp[2] = this.address;
      this.$emit('markerChanged',temp);
    },
    dragged: function(event){
      this.coordinates[0] = event.location.lat;  // lat
      this.coordinates[1] = event.location.lng;  // lng
      const temp = [];
      temp[0] = this.coordinates[0];
      temp[1] = this.coordinates[1];
      temp[2] = this.address;
      this.$emit('markerChanged',temp);
    },
  },
  mounted(){
    if (this.withGeocoding) {
      this.$refs.map.mapObject.on('geosearch/showlocation', this.showlocation);
      this.$refs.map.mapObject.on('geosearch/marker/dragend', this.dragged);
    }
    if (this.withLocation) {
      L.control.locate({
        drawCircle : false,
        strings : {
          title: "Δείξε μου που βρίσκομαι!"
        },
        showPopup: false
      }).addTo(this.$refs.map.mapObject);
    }
  }
}
</script>

<style scoped>
#map {
  height: 300px;
  width: 150px;
  min-height: 100%; 
  min-width: 100%;
  display: block;
}

</style>
