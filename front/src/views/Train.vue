<template>
  <div>
    <el-button type="primary" @click="train"
    v-loading.fullscreen.lock="fullscreenLoading"
    >训练</el-button>
   
  </div>
</template>

<script>
import axios from "axios";
import { train, postValue } from "../assets/api";
import storage from '../storage'
export default {
  name: "",
  data() {
    return {
      options: ["Active", "Rest"],
      labels:'',
      fullscreenLoading: false
    };
  },
  methods: {
    train() {
      this.fullscreenLoading = true;
      axios
        .get(train)
        .then(res => {
          this.fullscreenLoading = false
          this.$router.push("/home");
        })
        .catch(error => {
          this.fullscreenLoading = false;
          this.$message("网络错误")
        });
    },
  },
  mounted(){
    storage.setItem('data',{id:12,fft_datas:[12,3,4,5,9]})
    console.log(storage.getItem('data'))
  }
};
</script>

<style lang="less" scoped>
</style>