<template>
  <div class="button">
    {{title}}
  </div>
</template>

<script>
export default {
    props: {
        title: String,
    }
}
</script>

<style lang="scss" scoped>
.button {
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
    
}
</style>
