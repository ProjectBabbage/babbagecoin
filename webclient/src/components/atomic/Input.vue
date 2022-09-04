<template>
    <div>
        <label for="label">{{label}}</label>
        <input :name="label" :placeholder="placeholder" />
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
