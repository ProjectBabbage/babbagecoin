<template>
  <div>
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
export default {
  name: 'Transaction',
  components: {Button, Input},
  props: {
    masterUrl: String,
    wallet: Object,
  },
  data() {
    return {
      receiver: "",
      amount: null,
      message: ""
    }
  },
  methods: {
    makeTransaction() {
      this.message = "";
      if (!this.amount || !this.receiver) {
        this.message = "Fill the fields above."
        return;
      }
      const url = `${this.masterUrl}webclient/tx`;
      this.axios
          .post(url, {
            amount: this.amount,
            address: this.receiver,
            private_key: this.wallet.private_key
          })
          .then(response => {
            this.message = response.data.message;
            this.amount = null;            
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
