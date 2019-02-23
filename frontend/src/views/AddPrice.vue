<template>
    <div id="add-price">
          <form @submit.prevent="post">
              <h2>Προσθήκη τιμής</h2>
              <label>Τιμή(€):</label>
              <label>
                  <input name="price" type="text"
                      v-validate="'required|decimal:2|min_value:0.01'"
                      data-vv-as="*Το πεδίο"
                      v-model="price.cost" />
              </label>
              <span>{{ errors.first('price') }}</span>
              <h4>Χρονικό διάστημα που το προϊόν έχει την παραπάνω τιμή:</h4>
              <label>Ημερομηνία  από:</label>
              <label>
                  <input name="date_from" type="text"
                      v-validate="'required|date_format:YYYY/MM/DD'"
                      ref="fromDate"
                      data-vv-as="*Η ημερομηνία"
                      v-model="price.dateFrom" />
              </label>
              <span>{{ errors.first('date_from') }}</span>
              <label>Ημερομηνία εώς:</label>
              <label>
                  <input name="date_to" type="text"
                      v-validate="'required|date_format:YYYY/MM/DD|after:fromDate,true'"
                      data-vv-as="*Η ημερομηνία"
                      v-model="price.dateTo" />
              </label>
              <span>{{ errors.first('date_to') }}</span>
              <label>Επέλεξε το προϊόν:</label>
              <label>
                  <select v-model="price.productId"
                      v-validate="'required'"
                      name="product_name"
                      data-vv-as="*Το πεδίο">
                    <option v-for="product in products"
                            v-bind:value="product.id"
                            v-bind:key="product.id">
                        {{ product.name }}
                    </option>
                  </select>
              </label>
              <span>{{ errors.first('product_name') }}</span>
              <label>Επέλεξε το κατάστημα:</label>
              <label>
                  <myMap :with-location="true" :data="shops" @markerSelected="shopSelected"></myMap>
                  <select hidden v-model="price.shopId"
                      v-validate="'required'"
                      name="shop_name"
                      data-vv-as="*Το κατάστημα">
                      <!-- Hack-ish, how to add v-validate without html ? -->
                  </select>
              </label>
              <span>{{ errors.first('shop_name') }}</span>
              <div v-if="true">
                  {{ shopData }}
              </div>
              <p>
                <input type="submit" value="Προσθήκη">
              </p>
          </form>
    </div>
</template>

<script>
import qs from 'qs';
import myMap from '../components/Map.vue'
import { L } from 'vue2-leaflet'
export default {
  components:{
    myMap
  },
  data() {
    return {
      price:{
        cost: null,
        dateFrom: null,
        dateTo: null,
        productId: null,
        shopId: null,
      },
      shops: [],
      products: [],
      shopData: null
    }
  },
  methods:{
      shopSelected: function (shop) {
          this.price.shopId = shop.id;
          this.shopData = shop;
      },
      post: function(){
          this.$validator.validateAll().then(valid => {
              if (valid) {
                  this.$axios.post('/prices',
                      qs.stringify({
                          price: this.price.cost,
                          dateFrom: this.price.dateFrom,
                          dateTo: this.price.dateTo,
                          productId: this.price.productId,
                          shopId: this.price.shopId
                      })
                  ).then(() => {
                      alert("Ευχαριστούμε για την προσθήκη μιας νέας τιμής!");
                      this.doReset();
                  });
              }
          });
      },
    doReset: function(){
      this.$validator.reset();
      this.price.cost = null;
      this.price.dateFrom = null;
      this.price.dateTo = null;
      this.price.productId = null;
      this.price.shopId = null;
    }
  },
  mounted(){
    this.$axios.get('/products').then((response) => {
         this.products = response.data.products;
      });
     this.$axios.get('/shops').then((response) => {
         const shops = response.data.shops;
         shops.forEach((x) => x['latlng'] = new L.latLng(x.lat, x.lng));
         this.shops = shops;
     });
  },
}
</script>

<style scoped>
#add-price *{
    box-sizing: border-box;
}
#add-price{
    margin: 20px auto;
    max-width: 500px;
}
label{
    display: block;
    margin: 20px 0 10px;
}
input[type="text"], textarea{
    display: block;
    width: 100%;
    padding: 8px;
}

h3{
    margin-top: 10px;
}

</style>
