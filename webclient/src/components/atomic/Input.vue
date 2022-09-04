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
    },
    data(){
        return {
            value: null
        }
    },
}
</script>

<style lang="scss" scoped>
label {
    font-weight: 600;
}
input {
    margin: 5px;
    padding: 5px;
    height: 20px;
    font-size: 1em;
}
</style>
