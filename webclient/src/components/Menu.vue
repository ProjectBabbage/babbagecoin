<template>
  <div id="menu">
    <a :href="masterUrl">
      <Box class="explorer" title="Explorer" subtitle="See it aall" />
    </a>

    <Box
      :class="{ shadowed: currentBox == 'wallet' }"
      @click="$emit('menuBoxClicked', 'wallet')"
      title="Wallet"
      subtitle="Where to put some"
    />
    <Box
      :class="{ shadowed: currentBox == 'faucet' }"
      @click="$emit('menuBoxClicked', 'faucet')"
      title="Faucet"
      subtitle="Ask for some :)"
    />
    <Box
      :class="{ shadowed: currentBox == 'transactions' }"
      @click="$emit('menuBoxClicked', 'transactions')"
      title="Transactions"
      subtitle="Send some"
    />
  </div>
</template>

<script>
import Box from "./atomic/Box.vue";
export default {
  name: "Menu",
  props: {
    currentBox: String,
    masterUrl: String,
  },
  components: { Box },
};
</script>

<style lang="scss" scoped>
#menu {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 10px;

  a {
    text-decoration: none;
    color: black;

    .explorer {
      border-style: dashed;
    }
  }
}

@media (max-width: 500px) {
  #menu {
    padding: 10px 0 20px 0;
  }
}

.shadowed {
  box-shadow: 5px 5px 5px rgb(51, 51, 51);
}
</style>
