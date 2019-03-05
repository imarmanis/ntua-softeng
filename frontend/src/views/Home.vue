<template>
  <div class="home">
    <div class="text-center" style="height: 100px; background-color: rgb(192,192,192);">
      <div class="spacer_center"></div>
      <h3>Παρατηρητήριο Τιμών Καυσίμων</h3>
    </div>
    <div class="spacer"></div>
    <h6>Καλώς ήλθατε στο Παρατηρητήριο Τιμών Καυσίμων,</h6>
    <img  class="image" src="../../public/fuel.png"/>
    <div class="spacer"></div>
    <div class="spacer"></div>
    <label class="Helpdesk" style="color: red;">Γραμμή Εξυπηρέτησης (Helpdesk): 210-4815717 (Ώρες λειτουργίας: 7:00 - 15:00)</label>
    <label>Για τεχνικά ζητήματα και προτάσεις σχετικά με τη λειτουργία της ιστοσελίδας μπορείτε να στείλετε e-mail στο foobar@fuelprices.gr</label>
  </div>
</template>

<script>
export default {
        components:{
        }
}
</script>

<style scoped>
.spacer {
    padding-top: 40px;
    padding-bottom: 20px;
}
.spacer_center {
    padding-top: 20px;
    padding-bottom: 10px;
}
h3{
  font-weight: bold;
}
h6{
  margin-right: 365px;
}
label.Helpdesk{
  margin-right: 315px;
  font-size: 15px;
}
label{
  font-size: 15px;
}
image{
  margin-right: 365px;
}
</style>
