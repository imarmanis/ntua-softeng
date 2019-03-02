<template>
    <div id="search-price">
        <b-jumbotron lead="Αναζήτηση τιμής">
            <b-form @submit.prevent="post">
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
                        :invalid-feedback="errors.first('dist')"
                        id="distgrop" label="Ακτίνα από σημείο ενδιαφέροντος (Km):" label-for="dist"
                        label-cols = 3 >
                    <b-form-input
                            name="dist"
                            id="dist"
                            type="text"
                            v-validate="'decimal:2|min_value:0.01'"
                            data-vv-as="*Η απόσταση"
                            v-model="dist"
                            :state="errors.has('dist') ? false :null"
                    />
                </b-form-group>
                <b-form-group v-if="dist"
                              id="shopgroup"
                              :invalid-feedback="errors.first('my_loc')"
                              :state="errors.has('my_loc') ? false :null"
                              label="Σημείο ενδιαφέροντος"
                              label-cols =3   >
                    <myMap v-validate="'required'" data-vv-name="my_loc" data-vv-as="*Η Τοποθεσία"
                           :with-rclick="true" :with-location="true" @input="rclick"></myMap>
                </b-form-group>
                <b-button type="submit" variant="primary">Αναζήτηση</b-button>
            </b-form>
        </b-jumbotron>
        <myMap :data="shops"  @input="shopSelected"></myMap>
        <div v-for="price in priceData" :key="price.id">
            {{ price }}
        </div>
    </div>
</template>

<script>
import myMap from '../components/Map.vue'
import { L } from 'vue2-leaflet'
export default {
    components:{
        'myMap': myMap
    },
    data() {
        return {
            dateFrom : null,
            dateTo : null,
            dist : null,
            productId : null,
            products : [],
            shops: [],
            priceData : [],
            rclickedPos : null
        }
    },
    methods: {
        shopSelected : function (shop) {
            this.priceData = shop.prices;
        },
        rclick : function (x) {
            this.rclickedPos = x
        },
        post: function() {
            this.$validator.validateAll().then(valid => {
                if (valid) {
                    let params = {
                        products : this.productId,
                        // no need to stringify, just set products = id instead of [ id ]
                        dateFrom : this.dateFrom,
                        dateTo : this.dateTo
                    }
                    if (this.dist) {
                        params.geoDist = this.dist;
                        params.geoLng = this.rclickedPos.lng;
                        params.geoLat = this.rclickedPos.lat;
                    }
                    this.$axios.get('/prices', {
                            params: params
                        }
                    ).then((resp) => {
                        const prices = resp.data.prices;
                        const shopIds = Array.from(new Set(prices.map((x) => x.shopId)));
                        this.shops = []; // clear possbile previous data
                        shopIds.forEach((v) => {
                                this.$axios.get('/shops/'+v).then((resp) => {
                                    this.shops.push({
                                        id : v,
                                        latlng : L.latLng(resp.data.lat, resp.data.lng),
                                        prices: prices.filter((x) => x.shopId == v),
                                    })
                                })
                            }
                        );
                    });
                }
            });
        }
    },
    mounted(){
        this.$axios.get('/products').then((response) => {
            this.products = response.data.products;
        });
    }
}
</script>

<style scoped>
    #search-price *{
        box-sizing: border-box;
    }
    #search-price{
        margin: 20px auto;
        max-width: 500px;
    }

    h3{
        margin-top: 10px;
    }

</style>
