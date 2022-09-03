
<template>
<div id="content">
    <component :is="currentBox">
    </component>
</div>
</template>

<script>
import Wallet from './content/Wallet.vue'
import Faucet from './content/Faucet.vue';
import Transactions from './content/Transactions.vue';
export default {
    name: 'Content',
    props: {
        currentBox: String,
    },
    components: {
        Wallet, Faucet, Transactions
    }
}
</script>

<style scoped>
#content {
    border: 2px solid black;
    padding: 10px;
}
</style>
