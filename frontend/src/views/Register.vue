<template>
    <div id="add-product">
          <form @submit.prevent="post">
              <h2>Εγγραφή νέου χρήστη</h2>
              <label>Όνομα</label>
              <input name="u_name" type="text"
                  v-validate="'required'"
                  data-vv-as="*Το πεδίο"
                  v-model="user.name" />
              <span
                  style="color:red"
                  v-show="errors.has('u_name')">
                  {{ errors.first('u_name') }}
              </span>
              <label>Κωδικός</label>
              <input name="u_password" type="text"
                  v-validate="'required'"
                  data-vv-as="*Το πεδίο"
                  v-model="user.password" />
              <span
                  style="color:red"
                  v-show="errors.has('u_password')">
                  {{ errors.first('u_password') }}
              </span>
              <p>
                <input type="submit" value="Εγγραφή">
              </p>
          </form>
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
#add-product *{
    box-sizing: border-box;
}
#add-product{
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
