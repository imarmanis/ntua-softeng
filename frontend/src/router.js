import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import AddShop from "./views/AddShop";
import AddProduct from "./views/AddProduct";
import AddPrice from "./views/AddPrice";
import SearchPrice from "./views/SearchPrice"
import SearchShop from "./views/SearchShop"
import Register from "./views/Register";
import Login from "./views/Login";
import Logout from "./views/Logout";
import Stats from "./views/Stats";


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
    },
    {
      path: '/searchPrice',
      name: 'searchPrice',
      component: SearchPrice
    },
    {
      path: '/searchShop',
      name: 'searchShop',
      component: SearchShop
    },
    {
      path: '/stats',
      name: 'stats',
      component: Stats
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },    
    {
      path: '/logout',
      name: 'logout',
      component: Logout
    }
  ]
})
