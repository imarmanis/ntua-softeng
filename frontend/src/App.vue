<template>
  <div id="app" :class="[{'collapsed' : collapsed}]">
   <div class="container">
    <router-view/>
  </div>
  <app-sidebar @collapse="onCollapse" />
  </div>
</template>

<script>
  import Sidebar from './components/Sidebar';

  export default {
    data () {
      return {
         collapsed: false
      }

    },
    components: {
      'app-sidebar': Sidebar
    },
    methods: {
       onCollapse (collapsed) {
          this.collapsed = collapsed

       }

    }
  }
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-left: 250px;
}
#app.collapsed {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-left: 50px;
}


</style>
