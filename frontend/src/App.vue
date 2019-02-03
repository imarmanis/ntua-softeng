<template>
  <div>
  <div id="app">
    <app-sidebar/>
  </div>    
  <div id="app"> 
  <router-view/>
  </div>
  </div>
</template>

<script>
  import Sidebar from './components/Sidebar';

  export default {
    components: {
      'app-sidebar': Sidebar
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
}

</style>
