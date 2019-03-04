<template>
    <div id="search-price">
        <b-container fluid>
            <b-row>
                <b-col>
                    <b-jumbotron lead="Αναζήτηση τιμών">
                        <b-form @submit.prevent="post">
                            <b-form-group
                                    id="products_group"
                                    label="Προϊόντα :"
                                    label-for="pid_input"
                                    description="Προαιρετικά επιλέξτε επιθυμητά προϊόντα (Ctr για επιλογή πολλών)"
                            >
                                <b-form-select
                                        multiple
                                        id="pid_input"
                                        v-model="productIds"
                                >
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
                                    id="shopgroup"
                                    :invalid-feedback="errors.first('price_loc')"
                                    :state="errors.has('price_loc') ? false :null"
                                    label="Επίλεξε κατάστημα"
                                    label-cols =3   >
                                <myMap v-validate="'required'" data-vv-name="price_loc" data-vv-as="*Η Τοποθεσία" :with-location="true" :data="shops" @input="shopSelected"></myMap>
                            </b-form-group>
                            <div class="spacer"> </div>
                            <b-button type="submit" variant="primary">Αναζήτηση</b-button>
                        </b-form>
                    </b-jumbotron>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-jumbotron v-if="prices" lead="Αποτελέσματα"
                                 class="search-price">
                        <template v-if="prices.length > 0">
                            <b-row>
                                <p>Βρέθηκαν {{ prices.length }} σχετικές καταγραφές.</p>
                            </b-row>
                            <b-row>
                                <b-pagination size="md" v-model="curpage" :total-rows="this.total_count" @change="post" :per-page="10" />
                                <b-table striped hover :items="tdata" />
                            </b-row>
                        </template>
                        <template v-else>
                            <b-row>
                                <p>
                                    Δεν βρέθηκαν σχετικές καταγραφές.
                                </p>
                            </b-row>

                        </template>
                    </b-jumbotron>

                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import myMap from '../components/Map.vue'
    import { L } from 'vue2-leaflet'
    import * as qs from "qs";
    export default {
        components:{
            'myMap': myMap
        },
        data() {
            return {
                products : [],
                productIds : [],
                dateFrom : null,
                dateTo : null,
                selectedShop : null,
                shops: [],

                prices : null,
                total_count: 0,
                curpage: 1
            }
        },
        computed : {
            tdata: function () {
                return this.prices.map((p) => {
                    return {
                        'Προϊόν' : p.productName,
                        'Τιμή' : p.price,
                        'Ημερομηνία' : p.date,
                    }
                })
            }
        },
        methods: {
            shopSelected: function (shop) {
                this.selectedShop = shop.id;
            },
            post: function(s) {
                if (!(Number.isInteger(s))) {s=1; this.curpage=1}
                this.$validator.validateAll().then(valid => {
                    if (valid) {
                        let params = qs.stringify(
                            {
                                start : 10*(s - 1),
                                count : 10,
                                products: this.productIds,
                                dateFrom : this.dateFrom,
                                dateTo : this.dateTo,
                                shops : this.selectedShop
                            },
                            {
                                arrayFormat :'repeat'
                            }
                        );
                        this.$axios.get('/prices?' + params
                            // because of products[] we need custom query string
                        ).then((resp) => {
                            this.prices = resp.data.prices;
                            this.total_count = resp.data.total;
                        });
                    }
                });
            }
        },
        mounted(){
            this.$axios.get('/products').then((response) => {
                this.products = response.data.products;
            });
            this.$axios.get('/shops').then((response) => {
                this.shops = response.data.shops.map((s) => {
                    return {
                        id : s.id,
                        latlng : L.latLng(s.lat, s.lng),
                        name : s.name
                    }
                });
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
