<template>
  <div>
    <Input label="Receiver:" placeholder="Specify its public key" />
    <Input label="Amount:" placeholder="X BBC" />
    <Button title="Sign and send" @click="makeTransaction" />
  </div>
</template>

<script>
import Button from '../atomic/Button.vue'
import Input from '../atomic/Input.vue'
export default {
  name: 'Transaction',
  components: {Button, Input},
  methods: {
    makeTransaction() {
      this.axios.get("http://localhost:5000/").then(response => console.log(response))
    }
  }
}

</script>

<style lang="scss" scoped>
</style>
