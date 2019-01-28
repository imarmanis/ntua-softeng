<template>
  <div>
     <app-header></app-header>
     <router-view></router-view>
  </div>
</template>

<script>
// Imports
import homepage from './components/home.vue';
import addShop from './components/addShop.vue';
import addProduct from './components/addProduct.vue';
import addPrice from './components/addPrice.vue';
import header from './components/header.vue';

export default {
  components:{
      'app-header': header,
  },
}
</script>

<style>

</style>
