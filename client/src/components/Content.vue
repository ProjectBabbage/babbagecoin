
<template>
<component id="content" :is="currentBox">
</component>
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
}
</style>
