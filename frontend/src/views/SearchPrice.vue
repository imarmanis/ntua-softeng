<template>
    <div id="search-price">
        <form @submit.prevent="post">
            <myMap :with-rclick="true" :with-location="true" :data="shops" @markerSelected="shopSelected" @rclickedPos="rclick"></myMap>
            <p>
                <input type="submit" value="Αναζήτηση">
            </p>
        </form>
        <div v-if="rclickedPos">
            User right-clicked position : {{ rclickedPos }} (maybe useful for search query)
        </div>
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
            this.$axios.get('/prices', {
                    params: {
                        dateFrom : "2000-01-10",
                        dateTo : "3000-12-12"
                    }
                }
            ).then((resp) => {
                const prices = resp.data.prices;
                const shopIds = Array.from(new Set(prices.map((x) => x.shopId)));
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
    },
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
