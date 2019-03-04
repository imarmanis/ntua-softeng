import {L} from "vue2-leaflet";
<template>
    <div id="search-price">
        <b-container fluid >
           <b-row>
                <b-col>
                    <b-jumbotron lead="Αναζήτηση καταστήματος σε αύξουσα απόσταση">
                        <b-form @submit.prevent="post">
                            <b-form-group
                                    :invalid-feedback="errors.first('dist')"
                                    id="distgrop" label="Ακτίνα από σημείο ενδιαφέροντος (Km):" label-for="dist"
                                    label-cols=4
                                    >
                                <b-form-input
                                        name="dist"
                                        id="dist"
                                        type="text"
                                        v-validate="'required|decimal:3|min_value:0.01'"
                                        data-vv-as="*Η απόσταση"
                                        v-model="dist"
                                        :state="errors.has('dist') ? false :null"
                                />
                            </b-form-group>
                            <b-form-group
                                          id="shopgroup"
                                          :invalid-feedback="errors.first('my_loc')"
                                          :state="errors.has('my_loc') ? false :null"
                                          label="Σημείο ενδιαφέροντος"
                                             >
                                <myMap v-validate="'required'" data-vv-name="my_loc" data-vv-as="*Η Τοποθεσία"
                                       :with-rclick="true" :with-location="true" @input="rclick"></myMap>
                            </b-form-group>
                            <b-form-group
                                    :invalid-feedback="errors.first('scount')"
                                    id="scountgroup" label="Μέγιστο πλήθος καταστημάτων προς εμφάνιση:" label-for="scount"
                                    label-cols=4
                            >
                                <b-form-input
                                        name="scount"
                                        id="scount"
                                        type="text"
                                        v-validate="'required|integer'"
                                        data-vv-as="*Το πλήθος καταστημάτων"
                                        v-model="scount"
                                        :state="errors.has('scount') ? false :null"
                                />
                            </b-form-group>
                            <b-button type="submit" variant="primary">Αναζήτηση</b-button>
                        </b-form>
                    </b-jumbotron>
                </b-col>
           </b-row>
            <b-row>
                <b-col>
                    <b-jumbotron v-if="this.shops" lead="Αποτελέσματα"
                                 class="search-price">
                            <b-row>
                                <myMap :with-location="true" :data="shops"  @input="shopSelected"></myMap>
                            </b-row>
                        <b-row v-if="this.selectedShop">
                            <br>Όνομα καταστήματος : {{ this.selectedShop.sname }}
                            <br>Διεύθυνση καταστήματος : {{ this.selectedShop.address }}
                            <br>Απόσταση από σημείο ενδιαφέροντος (Km) : {{ this.selectedShop.dist.toFixed(3) }}
                        </b-row>
                    </b-jumbotron>

                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import myMap from '../components/Map.vue'
    import {L} from 'vue2-leaflet'

    export default {
    components:{
        'myMap': myMap
    },
    data() {
        return {
            dist : null,
            scount: 5,
            showRes : false,
            shops: null,
            selectedShop: null,
            rclickedPos : null,
        }
    },
    methods: {
        shopSelected : function (shop) {
            this.selectedShop = shop;
        },
        rclick : function (x) {
            this.rclickedPos = x;
        },
        post: function() {
            this.$validator.validateAll().then(valid => {
                if (valid) {
                    this.$axios.get('/shops/dist', {
                            params: {
                                lng: this.rclickedPos.lng,
                                lat: this.rclickedPos.lat,
                                dist: this.dist,
                                count: this.scount
                            }
                        }
                    ).then((resp) => {
                        this.selectedShop = null;
                        this.shops = resp.data.map((s) => {
                            return {
                                'sname': s.name,
                                'address': s.address,
                                'latlng': L.latLng(s.lat, s.lng),
                                'dist': s.dist
                            }
                        })
                    });
                }
            });
        }
    },
    mounted(){
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
    h3{
        margin-top: 10px;
    }

</style>
