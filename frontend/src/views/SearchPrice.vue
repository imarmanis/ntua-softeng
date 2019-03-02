<template>
    <div id="search-price">
        <b-container fluid >
           <b-row>
                <b-col>
                   <div id="search-price-in">
                    <b-jumbotron lead="Αναζήτηση τιμής">
                        <b-form @submit.prevent="post">
                            <b-form-group
                                    id="productgroup"
                                    :invalid-feedback="errors.first('product_name')"
                                    label="Επίλεξε προιόν"
                                    label-cols=4
                                    >
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
                                    label-cols=4
                                    >
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
                                    label-cols=4
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
                                    label-cols=4
                                    >
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
                                             >
                                <myMap v-validate="'required'" data-vv-name="my_loc" data-vv-as="*Η Τοποθεσία"
                                       :with-rclick="true" :with-location="true" @input="rclick"></myMap>
                            </b-form-group>
                            <b-button type="submit" variant="primary">Αναζήτηση</b-button>
                        </b-form>
                    </b-jumbotron>
                   </div>
                </b-col>
                <b-col v-if="showRes" class="map">
                    <b-row>
                        Βρέθηκαν {{ shops.length }} σχετικά καταστήματα :
                    </b-row>                
                    <b-row>       
                      <myMap :data="shops"  @input="shopSelected"></myMap>
                    </b-row>
                    <b-row>
                        <b-table striped hover :items="tdata" />
                    </b-row>   
                </b-col>
            </b-row>
        </b-container>
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
            selectedShop: null,
            rclickedPos : null,
            showRes : false
        }
    },
    computed: {
        tdata: function () {
            let res = [];
            this.shops.forEach((sp) => {
                sp.prices.forEach((pr) => {
                    res.push({
                        'price': pr.price,
                        'date' : pr.date,
                        'shopName': pr.shopName,
                        '_rowVariant': this.selectedShop == pr.shopId ? 'success' : null
                    })
                })
            })

            return res;
        }

    },
    methods: {
        shopSelected : function (shop) {
            this.selectedShop = shop.prices[0].shopId;
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
                        this.showRes = true;
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
        margin-top: 20px;
        margin: 20px auto;
        margin-left: 250px;
    }
    #search-price-in{
        margin-top: 0px;
        margin: 0px auto;
        max-width: 750px;
        margin-left: 0px;
    }


    h3{
        margin-top: 10px;
    }
    #mapsearch{
        margin-right: 0px;
        margin-bottom: 0px;
    }


</style>
