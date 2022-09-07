<template>
<div id="menu">
        <Box :class="{shadowed: currentBox=='wallet'}" @click="$emit('menuBoxClicked', 'wallet')" title="Wallet" subtitle="Where to put some"/>
        <Box :class="{shadowed: currentBox=='faucet'}" @click="$emit('menuBoxClicked', 'faucet')" title="Faucet" subtitle="Ask for some :)"/>
        <Box :class="{shadowed: currentBox=='transactions'}" @click="$emit('menuBoxClicked', 'transactions')" title="Transactions" subtitle="Send some"/>
</div>
</template>

<script>
import Box from './atomic/Box.vue';
export default {
    name: 'Menu',
    props: {
        currentBox: String,
    },
    components: {Box}
}
</script>

<style lang="scss" scoped>
#menu {
    display: flex;
    flex-flow: row;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
}

@media (max-width: 500px) {
  #menu{
    flex-flow: column;
  }
  
}
.shadowed {
    box-shadow:5px 5px 5px rgb(51, 51, 51);
}
</style>
