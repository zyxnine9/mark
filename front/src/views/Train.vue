<template>
    <div>
        <el-button type="primary" @click="train">训练</el-button>
        
    </div>
</template>

<script>
    import axios from "axios";
<<<<<<< HEAD
=======
    import { train } from '../assets/api'
>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468

    export default {
        name: '',
        data() {
            return {
            }
        },
        methods:{
            train() {
                axios
<<<<<<< HEAD
                    .post("http://127.0.0.1:5000/train", {})
=======
                    .post(train, {})
>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
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