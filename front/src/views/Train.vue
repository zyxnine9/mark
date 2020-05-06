<template>
  <div>
    <el-button type="primary" @click="train">训练</el-button>
    <LineChart :data="data"/>
  </div>
</template>

<script>
import axios from "axios";
import { train } from "../assets/api";
import LineChart from '../compoment/LineChart'

export default {
  name: "",
  data() {
    return {
        data:[1,2,3,7,8,9,100]
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
    }
  },
  components:{
      LineChart,
  }
};
</script>

<style lang="less" scoped>
</style>