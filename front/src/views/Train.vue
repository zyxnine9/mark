<template>
    <div>
        <el-button type="primary" @click="train">训练</el-button>
        
    </div>
</template>

<script>
    export default {
        name: '',
        data() {
            return {
                
            }
        },
        methods:{
            train(){
                this.$router.push('/home')
            }
        }
    }
</script>

<style lang="less" scoped>
    
</style>