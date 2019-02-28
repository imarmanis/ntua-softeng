<template>
  <div  id="add-product" >
    <b-jumbotron lead="Προσθήκη προιόντος" >
    <b-form @submit.prevent="post" @reset="doReset" >
      <b-form-group 
        :invalid-feedback="errors.first('p_name')"
        id="p_namegroup" label="Όνομα καυσίμου:" label-for="p_name" 
        label-cols=3>
        <b-form-input 
          id="p_name" 
          data-vv-as="*Το πεδίο"
          v-model="product.name"
          name="p_name" 
          type="text"
          v-validate="'required'"
          :state="errors.has('p_name') ? false : null"
          placeholder="πχ Αμόλυβδη"
        />
      </b-form-group>

      <b-form-group id="desc" label="Περιγραφή:" label-for="desc"
        label-cols=3>
        <b-form-textarea
          id="desc"
          type="text"
          v-model.lazy="product.description"
          placeholder="Πείτε μας κάτι για το προιόν" />
      </b-form-group>
      
      <b-form-group 
        :invalid-feedback="errors.first('p_category')"
        id="p_categroup" label="Κατηγορία:" label-for="p_category" label-cols=3 >
        <b-form-input 
          id="p_category" 
          data-vv-as="*Το πεδίο"
          v-model="product.category"
          name="p_category" 
          type="text"
          v-validate="'required'"
          :state="errors.has('p_category') ? false : null"
          placeholder="πχ Αμόλυβδη"
        />
      </b-form-group>

      <b-form-group id="tags" label="Ετικέτες:" label-for="p_tags" label-cols=3>
         <vue-tags-input
              id="p_tags"
              v-model="product.tag"
              placeholder = ""
              :tags="product.tags"
              @tags-changed="newTags => product.tags = newTags"
              />
      </b-form-group>
      <b-alert variant="success" v-model="err.suc">ΕΠΙΤΥΧΙΑ</b-alert>
      <b-alert variant="danger" v-model="err.error">ΑΠΟΤΥΧΙΑ</b-alert>

      <b-button type="submit" variant="primary">Προσθήκη</b-button>
      <b-button type="reset" variant="danger">Καθαρισμός</b-button>
    </b-form>
   </b-jumbotron>
  </div>
</template>

<script>
import qs from 'qs'
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
                this.$axios.post(
                    '/products',
                    qs.stringify(
                        {
                            name: this.product.name,
                            description: this.product.description,
                            category: this.product.category,
                            tags: this.product.tags.map((tag) => tag['text'])
                        },
                        {
                            arrayFormat :'repeat'
                        }
                    )
                ).then(()=>{
                    alert("Ευχαριστούμε για την προσθήκη ενός νέου προϊόντος!");
                    this.err.error=false;this.err.suc=true;
                    this.doReset();
                }).catch(err=>{this.err.error=true;this.err.suc=false;alert(err)});
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
    max-width: 750px;
}
</style>
