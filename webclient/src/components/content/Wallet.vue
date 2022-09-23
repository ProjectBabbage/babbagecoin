<template>
  <div id="wallet">
    <div id="wallet-menu">
      <Button @click="newWallet" title="New One" />
      <label for="file-upload" class="custom-file-upload">Import</label>
      <input
        type="file"
        accept=".txt"
        id="file-upload"
        name="importfile"
        @change="importWallet"
      />
    </div>
  </div>
</template>

<script>
import Input from "../atomic/Input.vue";
import Button from "../atomic/Button.vue";
export default {
  name: "Wallet",
  components: { Button, Input },
  props: {
    masterUrl: String,
  },
  data() {
    return {
      wallet: {
        private_key: null,
        address: null,
        balance: null,
      }
    };
  },

  methods: {
    resetWallet() {
      this.wallet = {
        private_key: null,
        address: null,
        balance: null,
      }
    },
    newWallet() {
      this.resetWallet();

      const url = `${this.masterUrl}webclient/wallet/new`;
      this.axios.get(url).then((response) => {
        const { _, private_key, address } = response.data;
        this.wallet.private_key = private_key;
        this.wallet.address = address;
        this.$emit("update-wallet", this.wallet);

        // download the private key as a file
        const link = document.createElement("a");
        link.download = "private.key.txt";
        link.href =
          "data:text/plain;charset=utf-8," +
          encodeURIComponent(this.wallet.private_key);
        link.click();
      });
    },
    importWallet(event) {
      this.resetWallet();
      // load private.key file from device
      // and send to server to retrieve the address:
      if (event.target.files) {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (event) => {

          // private key:
          this.wallet.private_key = reader.result;
          // address:
          const url = `${this.masterUrl}webclient/wallet/import`;
          this.axios
            .post(url, {
              private_key: this.wallet.private_key,
            })
            .then((response) => {
              const { _, address } = response.data;
              this.wallet.address = address;
              this.$emit("update-wallet", this.wallet);
            });

        };
        reader.readAsText(file);
      }
    },
  },
};
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
#wallet-content {
  #private {
    word-wrap: break-word;
  }
}
</style>
