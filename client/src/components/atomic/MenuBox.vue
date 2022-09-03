<template>
    <div class="menubox">
        {{title}}
    </div>
</template>

<script>
export default {
    name: 'MenuBox',
    props: {
        title: String,
    }    
}
</script>

<style lang="scss" scoped>
.menubox {
    border: 2px solid black;
    padding: 10px;
    min-width: 100px;
    font-size: 1.3em;
    font-weight: 500;
}
</style>
