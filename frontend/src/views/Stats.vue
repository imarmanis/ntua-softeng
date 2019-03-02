<template>
    <div id="add-price">
        <b-jumbotron lead="Στατιστικά προϊόντος">
        <b-form @submit.prevent="post">
          <b-form-group
              id="dategroupfrom"
              :invalid-feedback="errors.first('date_from')"
              label="Ημερομηνία  από:"
              label-cols = 3 >
                  <b-form-input name="date_from" type="date"
                      v-validate="'required|date_format:YYYY-MM-DD'"
                      ref="_fromDate"
                      data-vv-as="*Η ημερομηνία"
                      v-model="dateFrom"
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
                      v-model="dateTo"
                      :state="errors.has('date_to') ? false :null" 
                   />
            </b-form-group>
            <b-form-group
              id="productgroup"
              :invalid-feedback="errors.first('product_name')"   
              label="Επίλεξε προιόν"
              label-cols=3   >
                   <b-form-select v-model="productId"
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
            <b-button type="submit" variant="primary">Αναζήτηση</b-button>
          </b-form>
       </b-jumbotron>
        <plot v-if="data" :chart-data="data"></plot>
    </div>
</template>

<script>
import Plot from "../plugins/plot.js"
export default {
    components: {
        Plot
    },
  data() {
      return {
          data :  null,
          dateFrom: null,
          dateTo: null,
          productId: null,
          products: [],
      }
  },
  methods:{
      post: function(){
          this.$validator.validateAll().then(valid => {
              if (valid) {
                  this.$axios.get('/prices', {
                      params: {
                          dateFrom: this.dateFrom,
                          dateTo: this.dateTo,
                          products: this.productId,
                          sort: 'date|ASC'
                      }
                  }).then((resp) => {
                      const prices = resp.data.prices;
                      var dates = Array.from(new Set(prices.map((x) => x.date)));
                      var mins = [];
                      var maxs = [];
                      dates.forEach((d) => {
                          var prs = prices.filter((x) => x.date == d);
                          mins.push(Math.min(...prs.map(a => a.price)));
                          maxs.push(Math.max(...prs.map(a => a.price)));
                          // yes, the dots are important ...
                      });
                      this.data = {
                          labels: dates,
                          datasets: [
                              {
                                  label: 'Ελάχιστη τιμή',
                                  backgroundColor: '#5bf8bf',
                                  data: mins
                              },
                              {
                                  label: 'Μέγιστη τιμή',
                                  backgroundColor: '#f87979',
                                  data: maxs
                              },
                          ]
                      };
                      this.doReset();
                  });
              }
          });
      },
      doReset: function(){
          this.$validator.reset();
          this.dateFrom = null;
          this.dateTo = null;
          this.productId = null;
    }
  },
  mounted(){
    this.$axios.get('/products').then((response) => {
         this.products = response.data.products;
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

</style>
