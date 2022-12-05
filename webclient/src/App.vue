<template>
  <div id="main">
    <Menu
      id="menu"
      :currentBox="currentBox"
      :masterUrl="masterUrl"
      @menuBoxClicked="changeCurrentBox"
    />
    <Content :currentBox="currentBox" :master-url="masterUrl" />
    <br />
    <span>Last blocks:</span>
    <Explorer :master-url="masterUrl" />
  </div>
</template>

<script>
import Menu from "./components/Menu.vue";
import Content from "./components/Content.vue";
import Explorer from "./components/Explorer.vue";

export default {
  components: { Menu, Content, Explorer },
  data() {
    return {
      currentBox: "wallet",
      masterUrl: import.meta.env.VITE_MASTER_BASE_URL,
    };
  },
  methods: {
    changeCurrentBox(menuBox) {
      this.currentBox = menuBox;
    },
  },
};
</script>

<style lang="scss" scoped>
a {
  color: inherit;
}

#main {
  margin-top: 10px;
}

h1 {
  font-size: 2.8em;
  line-height: 1.1;
  margin: 10px;
}

menu {
  margin-bottom: 50px;
  overflow: hidden;
  padding: 5px;
}
</style>

