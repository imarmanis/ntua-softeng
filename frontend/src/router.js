import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import AddShop from "./views/AddShop";
import AddProduct from "./views/AddProduct";
import AddPrice from "./views/AddPrice";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    },
    {
      path: '/addShop',
      name: 'addShop',
      component: AddShop
    },
    {
      path: '/addProduct',
      name: 'addProduct',
      component: AddProduct
    },
    {
      path: '/addPrice',
      name: 'addPrice',
      component: AddPrice
    }
  ]
})
