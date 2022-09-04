<template>
  <div id="wallet">
    <div id="wallet-menu">
      <Button @click="newWallet" title="New One" />
      <input type="file" accept=".txt" id="file-upload" name="importfile" @change="readPrivateKey">
    </div>
    <div id="wallet-content" v-if="private_key && address">
      <p>Your address: {{address}} </p>
      <p>Your balance: {{balance}} </p>
    </div>
  </div>
</template>

<script>
import Input from '../atomic/Input.vue'
import Button from '../atomic/Button.vue'
import State from '../state';
export default {
  name: "Wallet",
  components: {Button, Input},
  data() {
    return {
      private_key: State.private_key,
      public_key: State.public_key,
      address: State.address,
      balance: State.balance,
    }
  },
  watch: {
    address(newAddress, oldAddress) {
      if(newAddress && !oldAddress){
        this.axios
            .get(`${State.master_url}addresses/${newAddress}/balance`)
            .then(response => this.balance = State.balance = response.data.balance);
      }
    }
  },
  methods: {
    newWallet(){
      const url = `${State.master_url}webclient/wallet/new`
      this.axios.get(url).then((response) => {
        const { public_key, private_key, address } = response.data;
        this.public_key = State.public_key = public_key;
        this.private_key = State.private_key =  private_key;
        this.address = State.address = address;
      });
    },
    readPrivateKey(event){
      // load private.key file from device
      // and send to server to convert to retrieve public key (and address):
      if(event.target.files){
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = event => {
          this.private_key = State.private_key = reader.result;
          console.log(`Imported : ${State.private_key}`);
          this.importWallet();
        };
        reader.readAsText(file);
      }
    },
    importWallet(){
      const url = `${State.master_url}webclient/wallet/import`
      this.axios.post(
          url,
          {
            private_key: this.private_key
          }
        ).then(response => {
          console.log(response.data);
          const {public_key, address } = response.data;
          this.public_key = State.public_key = public_key;
          this.address = State.address = address;
      });
    }
  }
}
</script>

<style lang="scss" scoped>
#wallet-menu {
  display: flex;
  flex-direction: row;
  justify-content: center;

  input[type="file"] {
    padding: 5px;
    background: black;
    color: white;
  }
  .custom-file-upload {
      border: 1px solid #ccc;
      display: inline-block;
      padding: 6px 12px;
      cursor: pointer;
  }
}

#wallet-content {
  overflow: scroll;
}
</style>
