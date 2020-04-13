<template>
    <div>
        <el-button type="primary" @click="train">训练</el-button>
        
    </div>
</template>

<script>
    import axios from "axios";
    import { train } from '../assets/api'

    export default {
        name: '',
        data() {
            return {
            }
        },
        methods:{
            train() {
                axios
                    .post(train, {})
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