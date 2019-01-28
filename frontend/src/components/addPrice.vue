<template>
    <div id="add-price">
          <form @submit.prevent="post">
              <h2>Προσθήκη τιμής</h2>
              <label>Τιμή(€):</label>
              <input name="price" type="text"
                  v-validate="'required|decimal:2|min_value:0.01'"
                  data-vv-as="*Το πεδίο"
                  v-model="price.cost" />
              <span
                  v-show="errors.has('price')">
                  {{ errors.first('price') }}
              </span>
              <h4>Χρονικό διάστημα που το προϊόν έχει την παραπάνω τιμή:</h4>
              <label>Ημερομηνία  από:</label>
              <input name="date_from" type="text"
                  v-validate="'required|date_format:YYYY/MM/DD'"
                  ref="fromDate"
                  data-vv-as="*Η ημερομηνία"
                  v-model="price.dateFrom" />
              <span
                  v-show="errors.has('date_from')">
                  {{ errors.first('date_from') }}
              </span>
              <label>Ημερομηνία εώς:</label>
              <input name="date_to" type="text"
                  v-validate="'required|date_format:YYYY/MM/DD|after:fromDate,true'"
                  data-vv-as="*Η ημερομηνία"
                  v-model="price.dateTo" />
              <span
                  v-show="errors.has('date_to')">
                  {{ errors.first('date_to') }}
              </span>
              <label>Επέλεξε το προϊόν:</label>
              <select v-model="price.productName"
                  v-validate="'required'"
                  name="product_name"
                  data-vv-as="*Το πεδίο">
                <option v-for="product in productNames">{{ product }}</option>
              </select>
              <p
                  v-show="errors.has('product_name')">
                  {{ errors.first('product_name') }}
              </p>
              <label>Επέλεξε το κατάστημα:</label>
              <select v-model="price.shopName"
                  v-validate="'required'"
                  name="shop_name"
                  data-vv-as="*Το πεδίο">
                <option v-for="shop in shopNames">{{ shop }}</option>
              </select>
              <p
                  v-show="errors.has('shop_name')">
                  {{ errors.first('shop_name') }}
              </p>
              <p>
                <input type="submit" value="Προσθήκη"></input>
              </p>
          </form>
    </div>
</template>

<script>
export default {
  components:{

  },
  data() {
    return {
      price:{
        cost: null,
        dateFrom: null,
        dateTo: null,
        productName: '',
        shopName: '',
        productId: null,
        shopId: null,
      },
      shops: [],
      products: [],
      shopIds: [],
      productIds: [],
      productNames: [],
      shopNames: [],
    }
  },
  methods:{
    post: function(){
      this.$validator.validateAll().then(valid => {
                if (valid) {
                  this.price.productId = this.search(this.price.productName, this.products);
                  this.price.shopId = this.search(this.price.shopName, this.shops);
                  this.$http.post('https://localhost:8765/observatory/api/prices', {
                    price: this.price.cost,
                    dateFrom: this.price.dateFrom,
                    dateTo: this.price.dateTo,
                    productId: this.price.productId,
                    shopId: this.price.shopId,
                    }).then(function(data){
                        alert("Ευχαριστούμε για την προσθήκη μιας νέας τιμής!");
                        this.doReset();
                        return;
                    });
                }
            });
    },
    doReset: function(){
      this.$validator.reset();
      this.price.cost = null;
      this.price.dateFrom = null;
      this.price.dateTo = null;
      this.price.productName = '';
      this.price.shopName = [];
      this.price.productId = null;
      this.price.shopId = null;

      this.shops = [];
      this.products = [];
      this.shopIds = [];
      this.productIds = [],
      this.productNames = [];
      this.shopNames = [];
    },
    search: function(nameKey, myArray){
      for (var i=0; i < myArray.length; i++) {
          if (myArray[i].name === nameKey) {
              return myArray[i].id;
          }
      }
    },
  },
  created(){

    this.$http.get('https://localhost:8765/observatory/api/products').then(function(data){
          //products list
         this.products = data.products;
         if(this.products){
            this.productIds = this.products.map(function(temp) {
                return temp['id'];  });
            this.productNames = this.products.map(function(temp) {
                return temp['name'];  });
         }
      });
     this.$http.get('https://localhost:8765/observatory/api/shops').then(function(data){
          //shops list
         this.shops = data.shops;
         if(this.shops){
            this.shopIds = this.shops.map(function(temp) {
                return temp['id'];  });
            this.shopNames = this.shops.map(function(temp) {
                return temp['name'];  });
         }
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
