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
      amount: 0,
      message: ""
    }    
  },
  methods: {
    request(){
      if(!this.amount || !State.address) return;
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
            this.message = response.data.message;
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
