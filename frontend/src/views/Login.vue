<template>
    <div id="login">
          <form @submit.prevent="login" >
              <h2>Login χρήστη</h2>
              <label>Όνομα</label>
              <label>
                  <input name="u_name" type="text"
                      v-validate="'required'"
                      data-vv-as="*Το πεδίο"
                      v-model="user.name" />
              </label>
              <span
                  style="color:red">
                  {{ errors.first('u_name') }}
              </span>
              <label>Κωδικός</label>
              <label>
                  <input name="u_password" type="text"
                      v-validate="'required'"
                      data-vv-as="*Το πεδίο"
                      v-model="user.password" />
              </label>
              <span
                  style="color:red">
                  {{ errors.first('u_password') }}
              </span>
              <p>
                <input type="submit" value="Login">
              </p>
          </form>
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
                    });
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
