
<template>
  <div id="content">
    <div id="currentWallet" v-if="wallet.address">
      <b>Address: </b> {{wallet.address}}<br>
      <b>Balance: </b> {{wallet.balance}}
    </div>
    <component
      :is="currentBox"
      :master-url="master_url"
      :wallet="wallet"
      @update-wallet="updateWallet"
    >
    </component>
  </div>
</template>

<script>
import Wallet from "./content/Wallet.vue";
import Faucet from "./content/Faucet.vue";
import Transactions from "./content/Transactions.vue";
export default {
  name: "Content",
  props: {
    currentBox: String,
  },
  data() {
    return {
      master_url: import.meta.env.VITE_MASTER_BASE_URL,
      wallet: {
        privateKey: null,
        address: null,
        balance: null,
      },
      balanceRefreshTimer: null,
    };
  },
  watch: {
    wallet(newWallet, oldWallet) {
        this.retrieveBalance(newWallet);
    },
  },
  components: {
    Wallet,
    Faucet,
    Transactions,
  },
  methods: {
    updateWallet(wallet){
      this.wallet = wallet;
      clearInterval(this.balanceRefreshTimer);
      this.balanceRefreshTimer = setInterval(this.retrieveBalance, 3000);
    },
    retrieveBalance() {
      this.axios
        .get(`${this.master_url}addresses/${this.wallet.address}/balance`)
        .then(
          (response) => (this.wallet.balance = response.data.balance)
        );
    },
  },
};
</script>

<style scoped>
#content {
  border: 2px solid black;
  padding: 10px;
}
#currentWallet {
  border: 1px solid black;
  padding: 5px;
  margin-bottom: 10px;
}
</style>
