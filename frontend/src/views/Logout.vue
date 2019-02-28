<template>
<p> Logging you out...</p>
</template>

<script>
export default {
  components:{

  },
  data() {
    return {
      user:{
        name: null,
        password: null
      },
    }
  },
  methods:{
    logout: function(){
         this.$store.dispatch('logout').then(()=>{
                       this.$router.push('/')
                    });
                }
    },
  beforeMount(){ this.logout() },
}
</script>

<style scoped>
#login *{
    box-sizing: border-box;
}
#login{
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

</style>
