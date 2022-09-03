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
      const master_url = import.meta.env.VITE_MASTER_BASE_URL;
      const url = `${master_url}greetings`;
      this.axios.get(url).then(response => console.log(response.data))
    }
  }
}

</script>

<style lang="scss" scoped>
</style>
