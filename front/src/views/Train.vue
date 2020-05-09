<template>
  <div>
    <!-- <el-button type="primary" @click="train">训练</el-button> -->
    <el-select v-model="labels" placeholder="请选择">
      <el-option v-for="(item, index) in options" :key="item" :value="index" :label="item">{{item}}</el-option>
    </el-select>
    <el-button type="primary" @click="select">选择</el-button>
    
  </div>
</template>

<script>
import axios from "axios";
import { train } from "../assets/api";
export default {
  name: "",
  data() {
    return {
      options: ["Active", "Rest"],
      labels:'',
    };
  },
  methods: {
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
    },
    select(){
      this.$message("1");
      this.$router.push("/mark")
    }
  }
};
</script>

<style lang="less" scoped>
</style>