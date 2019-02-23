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
                               title: 'Logout'
                           }]
                
                },
                {
                    title: "Add",
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
                    title: "Delete", 
                    child:
                           [{
                               title: 'Διαγραφή καταστήματος',
                               disabled: true
                           },
                           {
                               title: 'Διαγραφή προϊόντος',
                               disabled: true
                           },
                           {
                               title: 'Διαγραφή τιμής',
                               disabled: true
                           }]
                },
                {
                    title: "Search", 
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
                               title: 'Αναζήτηση τιμής',
                               disabled: true
                           }]
                }]}
                else {return [
                {    
                    title: "Guest",
                    child:                      
                           [{
                               href: '/register',
                               title: 'Εγγραφή'
                           },
                           {
                               href: '/login',
                               title: 'Login'
                           }]
                },
                {
                    title: "Add",
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
                    title: "Delete", 
                    child:
                           [{
                               title: 'Διαγραφή καταστήματος',
                               disabled: true
                           },
                           {
                               title: 'Διαγραφή προϊόντος',
                               disabled: true
                           },
                           {
                               title: 'Διαγραφή τιμής',
                               disabled: true
                           }]
                },
                {
                    title: "Search", 
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
                               title: 'Αναζήτηση τιμής',
                               disabled: true
                           }]
                }]}}
            
       },
       data : function(){return {
                collapsed: true,
                width: '250px',
        }},
        methods: {
             onCollapse(val){
                 this.collapsed = val
             },
             resolveStatus(){
                 if (this.$store.getters.user=="") {return "Guest"}
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
</style>
