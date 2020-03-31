<template>
    <div>
        <el-button type="primary" @click="train">训练</el-button>
        
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: '',
        data() {
            return {
            }
        },
        methods:{
            train() {
                axios
                    .post("http://127.0.0.1:5000/train", {})
                    .then(res => {
                        console.log(res);
                        this.$router.push("/home");
                    })
                    .catch(error => {
                        console.log(error);
                    });
            }
        }
    }
</script>

<style lang="less" scoped>
    
</style>