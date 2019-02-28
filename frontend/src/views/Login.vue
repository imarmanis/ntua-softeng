<template>
    <div id="login">
       <b-jumbotron lead="Login χρήστη">
          <b-form @submit.prevent="login" >
            <b-form-group
              :invalid-feedback="errors.first('u_name')"
              id="u_namegroup" label="Όνομα" label-for="u_name" >
              <b-form-input
                id="u_name"
                data-vv-as="*Το πεδίο"
                v-model="user.name"
                name="u_name"
                type="text"
                v-validate="'required'"
                :state="errors.has('u_name') ? false :null"
                placeholder="Όνομα"
              /> 
           </b-form-group>               
          <b-form-group
              :invalid-feedback="errors.first('u_pass')"
              id="u_passgroup" label="Κωδικός" label-for="u_pass" >
              <b-form-input
                id="u_pass"
                data-vv-as="*Το πεδίο"
                v-model="user.password"
                name="u_pass"
                type="password"
                v-validate="'required'"
                :state="errors.has('u_pass') ? false :null"
                placeholder="Κωδικός"
              /> 
           </b-form-group>
           <b-alert variant="danger" v-model="err.error" >ΑΠΟΤΥΧΙΑ (ελέγξε τον κωδικό)</b-alert> 
           <b-button type="submit" variant="primary">Login</b-button>
          </b-form>
        </b-jumbotron>
    </div>
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
      err :{
        error: null
      }
    }
  },
  methods:{
    login: function(){
      this.$validator.validateAll().then(valid => {
                if (valid) {
                  this.$store.dispatch('login', {
                    username: this.user.name,
                    password: this.user.password,
                  }).then(()=>{
                       alert("Κάνατε login επιτυχώς!"+this.$store.getters.token);
                       this.doReset();
                       this.$router.push('/')
                    }).catch(err=>{alert(err); this.err.error=true}) ;
                }
            });
    },
    doReset: function(){
      this.$validator.reset();
      this.user.name = null;
      this.user.password = '';
    },
  },
}
</script>

<style scoped>
#login *{
    box-sizing: border-box;
}
#login{
    margin: 20px auto;
    max-width: 500px;
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
