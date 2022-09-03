<template>
    <div>
        <label>{{label}}</label>
        <input :placeholder="placeholder" />
    </div>
</template>

<script>
export default {
    name: "Input",
    props: {
        label: String,
        placeholder: String,
    }
}
</script>

<style lang="scss" scoped>
</style>
