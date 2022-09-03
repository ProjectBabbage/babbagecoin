<template>
<div id="menu">
        <MenuBox :class="{shadowed: currentBox=='wallet'}" @click="$emit('menuBoxClicked', 'wallet')" title="Wallet" />
        <MenuBox :class="{shadowed: currentBox=='faucet'}" @click="$emit('menuBoxClicked', 'faucet')" title="Faucet" />
        <MenuBox :class="{shadowed: currentBox=='transactions'}" @click="$emit('menuBoxClicked', 'transactions')" title="Transactions" />
</div>
</template>

<script>
import MenuBox from './atomic/MenuBox.vue';
export default {
    name: 'Menu',
    props: {
        currentBox: String,
    },
    components: {MenuBox}
}
</script>

<style lang="scss" scoped>
#menu {
    display: flex;
    flex-flow: row;
    gap: 10px;
    margin-bottom: 10px;
}

.shadowed {
    box-shadow:5px 5px 5px rgb(51, 51, 51);
}
</style>
