<template>
   <sidebar-menu :menu="menu" :collapsed="collapsed" :width="width"/>
</template>

<script>
    export default {
        computed: {
                menu: function(){
                if (this.$store.getters.LoggedIn) {
                return [
                {
                    title: this.$store.getters.user,
                    child:                           
                           [{
                               href: '/logout',
                               title: 'Αποσύνδεση'
                           }]
                
                },
                {
                    title: "Προσθήκη",
                    child:
                           [{
                               href: '/addshop',
                               title: 'Νέο κατάστημα'
                           },
                           {
                               href: '/addproduct',
                               title: 'Νέο προϊόν'
                           },
                           {
                               href: '/addprice',
                               title: 'Νέα τιμή'
                           }]
                },
                {
                    title: "Αναζήτηση",
                    child:
                           [{
                               title: 'Αναζήτηση καταστήματος',
                               disabled: true
                           },
                           {
                               title: 'Αναζήτηση προϊόντος',
                               disabled: true
                           },
                           {
                               href: '/searchPrice',
                               title: 'Αναζήτηση τιμής'
                           }]
                }]}
                else {return [
                {    
                    title: "Επισκέπτης",
                    child:                      
                           [{
                               href: '/register',
                               title: 'Εγγραφή'
                           },
                           {
                               href: '/login',
                               title: 'Σύνδεση'
                           }]
                },
                {
                    title: "Προσθήκη",
                    child:
                           [{
                               href: '/addshop',
                               title: 'Νέο κατάστημα',
                               disabled: true
                           },
                           {
                               href: '/addproduct',
                               title: 'Νέο προϊόν',
                               disabled: true
                           },
                           {
                               href: '/addprice',
                               title: 'Νέα τιμή'
                           }]
                },
                   {
                      title: "Στατιστικά",
                      child:
                              [{
                                 href: '/stats',
                                 title: 'Στατιστικά προϊόντος',
                              },]
                   },
                {
                    title: "Αναζήτηση",
                    child:
                          [{
                             title: 'Αναζήτηση καταστήματος',
                             disabled :true
                           },
                           {
                               title: 'Αναζήτηση προϊόντος',
                               disabled: true
                           },
                           {
                               href: '/searchPrice',
                               title: 'Αναζήτηση τιμής'
                           }]
                }]}}
            
       },
       data : function(){return {
                collapsed: false,
                width: '250px',
        }},
        methods: {
             onCollapse(val){
                 this.collapsed = val
             },
             resolveStatus(){
                 if (this.$store.getters.user=="") {return "Επισκέπτης"}
                 else return this.$store.getters.user
             }
        }
    }
</script>
<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600');
body,
html {
  margin: 0;
  padding: 0;
}
body {
  font-family: 'Source Sans Pro', sans-serif;
  background-color: #f2f4f7;
}
#demo {
  padding-left: 50px;
}
#demo.collapsed {
  padding-left: 50px;
}
.demo {
  padding: 50px;
}
.badge-danger {
  background-color: #ff2a2a;
  color: #fff;
}
.v-sidebar-menu .collapse-btn {
   display:none;
}
</style>
