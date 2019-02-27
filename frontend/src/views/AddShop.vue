<template>
    <div id="add-shop">
          <form @submit.prevent="post">
              <h2>Προσθήκη Νέου Καταστήματος</h2>
              <label>Όνομα καταστήματος:</label>
              <label>
                  <input name="s_name" type="text"
                      v-validate="'required'"
                      data-vv-as="*Το πεδίο"
                      v-model="shop.name" />
              </label>
              <span>
                  {{ errors.first('s_name') }}
              </span>
              <label>Ετικέτες:</label>
              <vue-tags-input
              v-model="shop.tag"
              placeholder = ""
              :tags="shop.tags"
              @tags-changed="newTags => shop.tags = newTags"
              />
              <label>Πληκτρολόγησε την διεύθυνση του καταστήματος και αν θες μετακίνησε τον δείκτη στον χάρτη για μεγαλύτερη ακρίβεια στην τοποθεσία:</label>
              <myMap @markerChanged="markerChanged" :with-geocoding="true" :with-location="true"></myMap>
              <label v-if="validate_address">*Η διεύθυνση του καταστήματος δεν έχει συμπληρωθεί.</label>
              <p>
                <input type="submit" value="Προσθήκη">
              </p>
          </form>
    </div>
</template>

<script>
import qs from 'qs';
import myMap from '../components/Map.vue'
export default {
  components:{
    'myMap': myMap
  },
  data() {
    return {
      validate_address: false,
      shop:{
        name: '',
        address: '',
        tag: '',
        tags: [],
        lat: null,
        lng: null,
      },
    }
  },
  methods:{
    post: function(){
        this.$validator.validateAll().then(valid => {
          if(this.shop.address){
            this.validate_address = false;
            if (valid) {
                this.$axios.post('/shops',
                    qs.stringify(
                        {
                            name: this.shop.name,
                            address: this.shop.address,
                            tags: this.shop.tags.map((tag) => tag['text']),
                            lat: this.shop.lat,
                            lng: this.shop.lng
                        },
                        {
                            arrayFormat :'repeat'
                        }
                    )
                ).then(() => {
                    alert("Ευχαριστούμε για την προσθήκη ενός νέου καταστήματος!");
                    this.doReset();
                });
            }
          }
          else{
              this.validate_address = true;
          }
        });
  },
      markerChanged : function (data) {
          this.shop.lat = data[0];
          this.shop.lng = data[1];
          this.shop.address = data[2];
          this.validate_address = false;
      },
    doReset: function(){
      this.$validator.reset();
      this.validate_address = false;
      this.shop.name = '';
      this.shop.address = '';
      this.shop.tag = '';
      this.shop.tags = [];
    },
  },
}
</script>

<style scoped>
#add-shop *{
    box-sizing: border-box;
}
#add-shop{
    margin: 20px auto;
    max-width: 500px;
}
label{
    display: block;
    margin: 20px 0 10px;
}
input[type="text"]{
    display: block;
    width: 100%;
    padding: 8px;
}

h3{
    margin-top: 10px;
}

</style>
