<template>
  <div>
    <h1>请选择标注的类型</h1>
    <el-select v-model="value" placeholder="请选择">
      <el-option v-for="(item,index) in options" :key="item" :label="item" :value="index"></el-option>
    </el-select>
    {{value}}
    <el-button type="primary" @click="getNumber">确定</el-button>
  </div>
</template>

<script>
import axios from "axios";
import {postValue} from '../assets/api'
export default {
  name: "",
  data() {
    return {
      options: ['Active','Rest'],
      value: undefined,
    };
  },
  methods: {
    getNumber() {
      if (this.value != undefined) {
        axios
          .post(postValue, { value : this.value })
          .then(e => {
            if (e.data) {
              console.log(e.data);
              // this.$store.dispatch('setData',e.data)
              this.$router.push({ name: "Mark", params: e.data });
            }
          });
      } else {
        this.$message({
          message: "请选择标注张数",
          type: "warning"
        });
      }
    }
  }
};
</script>

<style lang="less" scoped>
</style>