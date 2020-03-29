<template>
  <div>
    <h1>请选择标注的张数</h1>
    <el-select v-model="value" placeholder="请选择">
      <el-option v-for="item in options" :key="item" :label="item" :value="item"></el-option>
    </el-select>
    <el-button type="primary" @click="getNumber">确定</el-button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "",
  data() {
    return {
      options: [1, 3, 5, 10],
      value: ""
    };
  },
  methods: {
    getNumber() {
      if (this.value) {
        axios.post("http://127.0.0.1:5000/post",{'value':this.value}).then(e=>{
          if(e.data){
            console.log(e.data)  
            this.$router.push({name:"Mark",params:e.data})
          }
        })
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