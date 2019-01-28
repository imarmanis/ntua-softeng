import Vue from 'vue'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'
import Routes from './routes'
import App from './App.vue'
import VeeValidate, { Validator }  from 'vee-validate'
import { L } from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'
import VueTagsInput from '@johmun/vue-tags-input'
import el from 'vee-validate/dist/locale/el'


Vue.use(VeeValidate, {locale: 'el'})
// Use packages
Vue.use(VueResource);
Vue.use(VueRouter);
Vue.use(VueTagsInput);
Validator.localize({ el: el })

export const bus = new Vue();
// Register routes
const router = new VueRouter({
    routes: Routes,
    mode: 'history'
});

// this part resolve an issue where the markers would not appear
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});
new Vue({
  el: '#app',
  render: h => h(App),
  router: router
})
