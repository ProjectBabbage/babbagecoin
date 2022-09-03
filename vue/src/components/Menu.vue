<template>
<div id="menu">
        <Box :class="{shadowed: currentBox=='wallet'}" @click="$emit('menuBoxClicked', 'wallet')" title="Wallet" />
        <Box :class="{shadowed: currentBox=='faucet'}" @click="$emit('menuBoxClicked', 'faucet')" title="Faucet" />
        <Box :class="{shadowed: currentBox=='transactions'}" @click="$emit('menuBoxClicked', 'transactions')" title="Transactions" />
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
.shadowed {
    box-shadow:5px 5px 5px rgb(51, 51, 51);
}
</style>
