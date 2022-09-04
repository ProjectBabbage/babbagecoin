<template>
  <div>
    <h3>Your balance: {{balance}}</h3>
    <label>Receiver: </label>
    <input v-model="receiver" placeholder="Specify its address" />
    <br>
    <label for="amount">Amount: </label>
    <input v-model="amount" placeholder="X BBC" id="amount" />
    <p>{{message}}</p>
    <Button title="Sign and send" @click="makeTransaction" />
  </div>
</template>

<script>
import Button from '../atomic/Button.vue'
import Input from '../atomic/Input.vue'
import State from '../state';
export default {
  name: 'Transaction',
  components: {Button, Input},
  data() {
    return {
      receiver: "",
      amount: 0,
      balance: State.balance,
      message: ""
    }
  },
  methods: {
    makeTransaction() {
      if (!this.amount || !this.receiver) return;
      const url = `${State.master_url}webclient/tx`;
      this.axios
          .post(url, {
            amount: this.amount,
            address: this.receiver,
            private_key: State.private_key
          })
          .then(response => {
            this.message = response.data.message;
            console.log(response.data);
          })
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
