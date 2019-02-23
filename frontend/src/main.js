import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import '@fortawesome/fontawesome-free/css/all.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import App from './App.vue'
import router from './router'
import store from './store'
import VeeValidate, { Validator }  from 'vee-validate'
import { L } from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'
import VueTagsInput from '@johmun/vue-tags-input'
import el from 'vee-validate/dist/locale/el'
import './plugins/axios'

Vue.config.productionTip = false;


Vue.use(VeeValidate, {inject: true, fieldsBagName: 'veeFields', locale: 'el'});
// Use packages
Vue.use(VueSidebarMenu);
Vue.use(BootstrapVue);
Vue.use(VueTagsInput);
Validator.localize({ el: el });

export const bus = new Vue();

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
