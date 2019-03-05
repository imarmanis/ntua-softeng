<template>
   <sidebar-menu :menu="menu" :collapsed="collapsed"  :width="width"/>
</template>

<script>
    export default {
        computed: {
                menu: function(){
                if (this.$store.getters.LoggedIn) {
                return [ 
                {
                    title: this.$store.getters.user,
                    icon: 'fa fa-user',
                    child:                           
                           [{
                               href: '/logout',
                               icon: 'fas fa-sign-out-alt',
                               title: 'Αποσύνδεση'
                           }]
                
                },
                   {
                      title: "Αναζήτηση",
                      icon: 'fa fa-eye',
                      child:
                              [
                                 {
                                    href: '/searchPrice',
                                    icon: 'fas fa-dollar-sign',
                                    title: 'Αναζήτηση τιμής'
                                 },
                                 {
                                    title: 'Αναζήτηση καταστήματος',
                                    icon: 'fa fa-gas-pump',
                                    href: '/searchShop'
                                 },
                              ]
                   },
                {
                    title: "Προσθήκη",
                    icon: 'fas fa-plus',
                    child:
                           [
                              {
                                 href: '/addprice',
                                 title: 'Νέα τιμή',
                                 icon: 'fas fa-dollar-sign'
                              },
                           {
                               href: '/addshop',
                               title: 'Νέο κατάστημα',
                               icon: 'fa fa-gas-pump',
                           },
                           {
                               href: '/addproduct',
                               icon: 'fab fa-product-hunt',
                               title: 'Νέο προϊόν'
                           },
                           ]
                }, 
                {
                      title: "Στατιστικά",
                      icon: 'fa fa-chart-area',
                      child:
                              [{
                                 href: '/stats',
                                 icon: 'fa fa-gas-pump',
                                 title: 'Στατιστικά προϊόντος',
                              },]
                },
                ]}
                else {return [
                {

    
                    title: "Επισκέπτης",
                    icon: 'fa fa-user',
                    child:                      
                           [{
                               href: '/register',
                               title: 'Εγγραφή',
                               icon: 'fa fa-user-plus'
                           },
                           {
                               href: '/login',
                               title: 'Σύνδεση',
                               icon: 'fas fa-sign-in-alt'
                           }]
                },
                   {
                      title: "Αναζήτηση",
                      icon: 'fa fa-eye',
                      child:
                              [
                                 {
                                    href: '/searchPrice',
                                    icon: 'fas fa-dollar-sign',
                                    title: 'Αναζήτηση τιμής'
                                 },
                                 {
                                    title: 'Αναζήτηση καταστήματος',
                                    href: '/searchShop',
                                    icon: 'fa fa-gas-pump'
                                 },
                              ]
                   },
                ]}}
            
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
.v-sidebar-menu {
  padding-top: 50px;
}
.v-sidebar-menu .collapse-btn {
  top: 0px;
  display: block;
}
.v-sidebar-menu .vsm-collapsed{
  width: 0;
}
</style>
