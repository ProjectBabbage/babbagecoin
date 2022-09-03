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
    max-width: 100px;
    margin: 10px;
    border: 2px solid black;
    border-radius: 5px;    
    font-weight: 700;

    &:hover {
        background-color: grey;
    }
    &:focus {
        outline: 4px auto -webkit-focus-ring-color;
    }
    // &:active {
    //     background-color: orange;

    // }
    
}
</style>
