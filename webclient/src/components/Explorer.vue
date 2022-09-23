<template>
    <div id="block-explorer" v-html="blocks">
    </div>
</template>
<script>
export default {
    props: {
        masterUrl: String,
    },
    data(){
        return {
            blocks: `<span>Fetching the 3 last blocks .. </span>`,
            blocksRefreshTimer: null,
        }
    },
    methods: {
        updateBlocks(){
            this.axios
                .get(`${this.masterUrl}/3`)
                .then(response => {
                    this.blocks = response.data;
                });
        }
    },
    created(){
        clearInterval(this.blocksRefreshTimer);
        this.blocksRefreshTimer = setInterval(this.updateBlocks, 1500);
    }
}
</script>
<style scoped>
#block-explorer{
    margin-top: 10px;
    border: 2px solid black;
}
</style>
