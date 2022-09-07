<template>
<div>
  <h1>Babbagecoin</h1>
  <h3> Interact with the blockchain </h3>
  <br>
  <Menu id="menu" :currentBox="currentBox" @menuBoxClicked="changeCurrentBox"/>
  <Content :currentBox="currentBox" />
</div>
</template>

<script>
import Menu from './components/Menu.vue';
import Content from './components/Content.vue';

export default {
  components: { Menu, Content },
  data(){
    return {
      currentBox: 'wallet'
    }
  },
  methods: {
    changeCurrentBox(menuBox){
      this.currentBox = menuBox;
    }
  }
}
</script>

<style lang="scss" scoped>
h1 {
  font-size: 2.8em;
  line-height: 1.1;
}

menu {
  margin-bottom: 50px;
}

</style>

