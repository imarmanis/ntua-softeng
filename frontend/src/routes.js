import addShop from './components/addShop.vue';
import addProduct from './components/addProduct.vue';
import addPrice from './components/addPrice.vue';
import homepage from './components/home.vue';

export default [
    { path: '/', component: homepage},
    { path: '/addshop', component: addShop},
    { path: '/addproduct', component: addProduct},
    { path: '/addprice', component: addPrice},
]
