<template>
  <div id="Faucet">
    <Input label="How much money do you want ?:" placeholder="100 BBC" />
    <Button title="Request" />
  </div>
</template>

<script>
import Button from '../atomic/Button.vue';
import Input from '../atomic/Input.vue';
export default {
  name: 'Faucet',
  components: {Button, Input}
}
</script>

<style lang="scss" scoped>
</style>
