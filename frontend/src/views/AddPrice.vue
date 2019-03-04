<template>
    <div id="add-price">
        <b-jumbotron lead="Προσθήκη τιμής">  
        <b-form @submit.prevent="post">
          <b-form-group 
             :invalid-feedback="errors.first('price')"
             id="pricegroup" label="Τιμή(€/L):" label-for="price"
             label-cols = 3 >
            <b-form-input
                name="price"
                id="price" 
                type="text"
                v-validate="'required|decimal:3|min_value:0.01'"
                data-vv-as="*Η τιμή"
                v-model="price.cost"
                :state="errors.has('price') ? false :null" 
             />
          </b-form-group>
          <b-form-group
              id="dategroupfrom"
              :invalid-feedback="errors.first('date_from')"
              label="Ημερομηνία  από:"
              label-cols = 3 >
                  <b-form-input name="date_from" type="date"
                      v-validate="'required|date_format:YYYY-MM-DD'"
                      ref="_fromDate"
                      data-vv-as="*Η ημερομηνία"
                      v-model="price.dateFrom" 
                      :state="errors.has('date_from') ? false :null" 
                  />
           </b-form-group>
           <b-form-group
              id="dategroupto"
              :invalid-feedback="errors.first('date_to')"   
              label="Ημερομηνία εώς:"
              label-for="date-to"  
              label-cols= 3 
              description="Hint: Πιέστε το βελάκι για ημερολόγιο" > 
                  <b-form-input id="date_to" name="date_to" type="date"
                      v-validate="'required|date_format:YYYY-MM-DD|after:_fromDate,true'"
                      data-vv-as="*Η ημερομηνία"
                      v-model="price.dateTo"
                      :state="errors.has('date_to') ? false :null" 
                   />
            </b-form-group>
            <b-form-group
              id="productgroup"
              :invalid-feedback="errors.first('product_name')"   
              label="Επίλεξε προιόν"
              label-cols=3   >
                   <b-form-select v-model="price.productId"
                      v-validate="'required'"
                      name="product_name"
                      data-vv-as="*Το πεδίο"
                      :state = "errors.has('product_name') ? false :null" >
                   <option   v-for="product in products"
                      v-bind:value="product.id"
                      v-bind:key="product.id" >
                      {{ product.name }}
                    </option>
                  </b-form-select>
            </b-form-group>
            <b-form-group
              id="shopgroup"
              :invalid-feedback="errors.first('price_loc')"
              :state="errors.has('price_loc') ? false :null"
              label="Επίλεξε κατάστημα"
              label-cols =3   >
                 <myMap v-validate="'required'" data-vv-name="price_loc" data-vv-as="*Η Τοποθεσία" :with-location="true" :data="shops" @input="shopSelected"></myMap>
            </b-form-group>
            <div class="spacer"> </div>
            <b-alert variant="success" v-model="err.suc">ΕΠΙΤΥΧΙΑ</b-alert>
            <b-alert variant="danger" v-model="err.error">ΑΠΟΤΥΧΙΑ</b-alert>
            <b-button type="submit" variant="primary">Προσθήκη</b-button>
          </b-form>
       </b-jumbotron>
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
      err:{
        error: null,
        suc: null
      }
    }
  },
  methods:{
      shopSelected: function (shop) {
          this.price.shopId = shop.id;
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
                          this.err.error = false;
                          this.err.suc = true;
                          this.doReset();
                      }).catch(err => {
                          this.err.error = true;
                          this.err.suc = false;
                          alert(err)
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
    max-width: 750px;
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
.spacer {
    padding-top: 40px;
    padding-bottom: 20px;
}
</style>
