<template>
  <div id="wallet">
    <div id="wallet-menu">
      <Button @click="newWallet" title="New One" />
      <label for="file-upload" class="custom-file-upload">Import</label>
      <input type="file" accept=".txt" id="file-upload" name="importfile" @change="readPrivateKey">
    </div>
    <div id="wallet-content" v-if="private_key && address">
      <p>Your balance: {{balance}} </p>
      <p>Your address: {{address}} </p>
      <p id="private">Your private key: {{private_key}} </p>
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
        this.retrieveBalance(newAddress);
      }
    }
  },
  methods: {
    retrieveBalance(address){
        this.axios
            .get(`${State.master_url}addresses/${address}/balance`)
            .then(response => this.balance = State.balance = response.data.balance);
    },
    newWallet(){
      this.resetWallet();
      const url = `${State.master_url}webclient/wallet/new`
      this.axios.get(url).then((response) => {
        const { public_key, private_key, address } = response.data;
        this.public_key = State.public_key = public_key;
        this.private_key = State.private_key =  private_key;
        this.address = State.address = address;
      });
    },
    resetWallet(){
      this.public_key = State.private_key = 0;
      this.private_key = State.private_key = 0;
      this.address = State.address = 0;
      this.balance = 0;
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
    display: none;
  }
  .custom-file-upload {
    margin: 10px;
    padding: 2px;
    border: 2px solid black;
    background-color: black;
    color: white;
    border-radius: 5px;    
    font-weight: 600;
    box-shadow: 10px 5px 5px green($color: #000000);

    &:hover {
        cursor: pointer;
        background-color: grey;
    }
    &:active {
        background-color: orange;

    }
    cursor: pointer;
  }
}
#wallet-content{
  #private {
    word-wrap: break-word;
  }
}
</style>
