<template>
  <div id="wallet">
    <div id="wallet-menu">
      <Button title="New One" />
      <Button title="Import" />
    </div>
  </div>
</template>

<script>
import Input from '../atomic/Input.vue'
import Button from '../atomic/Button.vue'
export default {
  components: {Button, Input}
}
</script>

<style lang="scss" scoped>
#wallet-menu {
  display: flex;
  flex-direction: row;
}

#wallet-content {
  
}
</style>
