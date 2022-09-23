<template>
  <div id="Faucet">
    <label>How much money do you want ?:</label>
    <input v-model="amount" placeholder="10 BBC" />
    <p>{{message}}</p>
    <Button @click="request" title="Request" />
  </div>
</template>

<script>
import Button from '../atomic/Button.vue';
import Input from '../atomic/Input.vue';
export default {
  name: 'Faucet',
  components: {Button, Input},
  props: {
    masterUrl: String,
    wallet: Object,
  },
  data() {
    return {
      amount: null,
      message: ""
    }    
  },
  methods: {
    request(){
      this.message = "";
      if(this.address) {
        this.message = "Set up a Wallet first.";
        return;
      }
      if(!this.amount) {
        this.message = "Set a non-zero amount."
        return;
      }
      this.axios
          .post(
            `${this.masterUrl}webclient/faucet/request`,
            {
              "amount": this.amount,
              "address": this.wallet.address
            }
          )
          .then(response => {
            console.log(response.data);
            this.message = response.data?.message ? response.data.message : `You successfully requested ${response.data.amount_requested}BBC.`;
            this.amount = null;
          });
    }
  } 
}
</script>

<style lang="scss" scoped>
label {
    font-weight: 600;
}
input {
    margin: 5px;
    padding: 5px;
    height: 20px;
    font-size: 1em;
}
</style>
