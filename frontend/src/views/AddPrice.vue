<template>
    <div id="add-price">
        <b-jumbotron lead="Προσθήκη τιμής">  
        <b-form @submit.prevent="post">
          <b-form-group 
             :invalid-feedback="errors.first('price')"
             id="pricegroup" label="Τιμή(€):" label-for="price" 
             label-cols = 5 >
            <b-form-input
                name="price"
                id="price" 
                type="text"
                v-validate="'required|decimal:2|min_value:0.01'"
                data-vv-as="*Το πεδίο"
                v-model="price.cost" 
             />
          </b-form-group>
          <b-form-group
              id="dategroupfrom"
              :invalid-feedback="errors.first('date_from')"
              label="Ημερομηνία  από:"
              label-cols = 5 >
                  <b-form-input name="date_from" type="date"
                      v-validate="'required'"
                      ref="fromDate"
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
              label-cols= 5 
              description="Hint: Πιέστε το βελάκι για ημερολόγιο" > 
                  <b-form-input id="date_to" name="date_to" type="date"
                      v-validate="'required|after:fromDate,true'"
                      data-vv-as="*Η ημερομηνία"
                      v-model="price.dateTo"
                      :state="errors.has('date_to') ? false :null" 
                   />
            </b-form-group>
            <b-form-group
              id="productgroup"
              :invalid-feedback="errors.first('product_name')"   
              label="Επίλεξε προιόν"
              label-cols=5   >
                   <b-form-select v-model="price.productId"
                      v-validate="'required'"
                      name="product_name"
<<<<<<< HEAD
                      data-vv-as="*Το πεδίο"
                      v-for="product in products"
                      :value="product.id"
                      :key="product.id"
                      {{ product.name }}
                  />
            </b-form-group>
            <b-form-group
              id="shopgroup"
              :invalid-feedback="errors.first('shop_name')"   
              label="Επίλεξε κατάστημα"
              label-cols =5   >
                  <myMap :with-location="true" :data="shops" @markerSelected="shopSelected"></myMap>
                  <b-form-select v-model="price.shopId"
                      v-validate="'required'"
                      name="shop__name"
                      data-vv-as="*Το κατάστημα"
                      v-for="shop in shops"
                      :value="shop.id"
                      :key="shop.id"
                      {{ shop.name }}
                  />
            </b-form-group>
            {{ shopData }}
            <b-button type="submit" variante="primary">Προσθήκη</b-button>
          </b-form>
       </b-jumbotron>
=======
>>>>>>> master
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
