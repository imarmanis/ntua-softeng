<template>
    <nav>
        <ul>
            <li><router-link to="/" exact>Κεντρική Σελίδα</router-link></li>
            <li><router-link to="/addshop" exact>Νέο Κατάστημα</router-link></li>
            <li><router-link to="/addproduct" exact>Νέο προϊόν</router-link></li>
            <li><router-link to="/addprice" exact>Νέα τιμή</router-link></li>
            <li><router-link to="/register" exact>Εγγραφή</router-link></li>
            <li><router-link to="/login" exact>Login</router-link></li>
      </ul>
    </nav>
</template>

<style scoped>
ul{
    list-style-type: none;
    text-align: center;
    margin: 0;
}
li{
    display: inline-block;
    margin: 0 10px;
}
a{
    color: #fff;
    text-decoration: none;
    padding: 6px 8px;
    border-radius: 10px;
}
nav{
    background: #444;
    padding: 14px 0;
    margin-bottom: 40px;
}
.router-link-active{
    background: #eee;
    color: #444;
}
</style>
