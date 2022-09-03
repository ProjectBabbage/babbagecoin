<template>
    <div class="box">
        {{title}}
    </div>
</template>

<script>
export default {
    name: 'Box',
    props: {
        title: String,
    }    
}
</script>

<style lang="scss" scoped>
.box {
    border: 2px solid black;
    padding: 10px;
    min-width: 150px;
    font-size: 1.2em;
    font-weight: 500;

    &:hover {
        cursor: pointer;
    }
}
</style>
