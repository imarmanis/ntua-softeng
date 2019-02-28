<template>
    <div id="register">
       <b-jumbotron lead="Εγγραφή νέου χρήστη">
          <b-form @submit.prevent="post" >
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
                :invalid-feedback="errors.first('u_pass_conf')"
                id="u_passgroup" label="Κωδικός" label-for="u_pass" >
              <b-form-input
                id="u_pass"
                ref="_u_pass"
                data-vv-as="την επιβεβαίωση"
                v-model="user.password"
                name="u_pass"
                type="password"
                v-validate="'required'"
                :state="errors.has('u_pass') ? false :null"
                placeholder="Κωδικός"
              />
              <b-form-input
                id="u_pass_conf"
                data-vv-as="*Το πεδίο"
                v-model="user.confpass"
                name="u_pass_conf"
                type="password"
                class="form-control"
                v-validate="'required|confirmed:_u_pass'"
                :state="errors.has('u_pass_conf') ? false :null"
                placeholder="Επιβεβαιώστε τον κωδικό"
              /> 
           </b-form-group> 
           <b-alert variant="success" v-model="err.suc" >ΕΠΙΤΥΧΙΑ</b-alert>
           <b-alert variant="danger" v-model="err.error">ΑΠΟΤΥΧΙΑ (όνομα υπό χρηση) </b-alert>
           <b-button type="submit" variant="primary">Εγγραφή</b-button>
          </b-form>
        </b-jumbotron>
    </div>
</template>

<script>
import qs from 'qs';
export default {
  components:{

  },
  data() {
    return {
      user:{
        name: null,
        password: null
      },
      err:{
        error: null,
        suc: null
      }
    }
  },
  methods:{
      post: function(){
          this.$validator.validateAll().then(valid => {
              if (valid) {
                  this.$axios.post('/register',
                      qs.stringify({
                          username: this.user.name,
                          password: this.user.password,
                      })
                  ).then(() => {
                      alert("Ευχαριστούμε για την προσθήκη ενός νέου χρήστη!");
                      this.doReset();
                      this.err.suc=true;
                      this.err.error=false;
                  }).catch(err=>{alert(err);
                                 this.err.error=true;
                                 this.err.suc=false});
              }
          });
      },
    doReset: function(){
      this.$validator.reset();
      this.user.name = null;
      this.user.password = '';
      this.user.confpass='';
    },
  },
}
</script>

<style scoped>
#register *{
    box-sizing: border-box;
}
#register{
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
