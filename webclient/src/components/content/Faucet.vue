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
import State from '../state';
export default {
  name: 'Faucet',
  components: {Button, Input},
  data() {
    return {
      amount: null,
      message: ""
    }    
  },
  methods: {
    request(){
      this.message = "";
      if(!State.address) {
        this.message = "Set up a Wallet first.";
        return;
      }
      if(!this.amount) {
        this.message = "Set a non-zero amount."
        return;
      }
      this.axios
          .post(
            `${State.master_url}webclient/faucet/request`,
            {
              "amount": this.amount,
              "address": State.address
            }
          )
          .then(response => {
            console.log(response.data);
            this.message = `You requested ${response.data.amount_requested}BBC`;
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
