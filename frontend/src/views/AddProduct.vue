<template>
    <div id="add-product">
          <form @submit.prevent="post">
              <h2>Προσθήκη Νέου Προϊόντος</h2>
              <label>Όνομα καυσίμου:</label>
              <input name="p_name" type="text"
                  v-validate="'required'"
                  data-vv-as="*Το πεδίο"
                  v-model="product.name" />
              <span
                  v-show="errors.has('p_name')">
                  {{ errors.first('p_name') }}
              </span>
              <label>Περιγραφή:</label>
              <textarea v-model.lazy="product.description"></textarea>
              <label>Κατηγορία:</label>
              <input name="p_category" type="text"
                  v-validate="'required'"
                  data-vv-as="*Το πεδίο"
                  v-model="product.category" />
              <span
                  v-show="errors.has('p_category')">
                  {{ errors.first('p_category') }}
              </span>
              <label>Ετικέτες:</label>
              <vue-tags-input
              v-model="product.tag"
              placeholder = ""
              :tags="product.tags"
              @tags-changed="newTags => product.tags = newTags"
              />
              <p>
                <input type="submit" value="Προσθήκη">
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
      product:{
        name: null,
        description: '',
        category: null,
        tag: '',
        tags: [],
      },
    }
  },
  methods:{
    post: function(){
      this.$validator.validateAll().then(valid => {
                if (valid) {
                  this.$http.post(
                   'https://localhost:8765/observatory/api/products', 
                    {
                    name: this.product.name,
                    description: this.product.description,
                    category: this.product.category,
                    tags: this.product.tags.map(function(tag) {
                      return tag['text'];  }),
                    },
                    {headers: {'X-OBSERVATORY-AUTH': this.$store.getters.token},
                    params,
                    emulateJSON: true}
                    ).then(function(){
                        alert("Ευχαριστούμε για την προσθήκη ενός νέου προϊόντος!");
                        this.doReset();
                        return;
                    });
                }
            });
    },
    doReset: function(){
      this.$validator.reset();
      this.product.name = null;
      this.product.description = '';
      this.product.category = null;
      this.product.tag = '';
      this.product.tags = [];
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
