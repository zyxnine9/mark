<template>
  <div>
    <h1>请选择标注的类型</h1>
    <el-select v-model="value" placeholder="请选择">
      <el-option v-for="(item,index) in options" :key="item" :label="item" :value="index"></el-option>
    </el-select>
    {{value}}
    <el-button type="primary" @click="getNumber" v-loading.fullscreen.lock="fullscreenLoading">确定</el-button>
  </div>
</template>

<script>
import axios from "axios";
import {postValue} from '../assets/api'
import storage from '../storage'
export default {
  name: "",
  data() {
    return {
      options: ['Active','Rest'],
      value: undefined,
      fullscreenLoading: false
    };
  },
  methods: {
    getNumber() {
      
      if (this.value != undefined) {
        this.fullscreenLoading = true;
        axios
          .post(postValue, { value : this.value })
          .then(e => {
            if (e.data) {
              this.$store.dispatch('setData',e.data)
              const temp = {
                ids:e.data.ids.slice(0,10),
                title:e.data.title.slice(0,10),
                raw_datas:e.data.raw_datas.slice(0,10),
                fft_datas:e.data.fft_datas.slice(0,10),
              }
              storage.setItem('data',temp)
              // this.$router.push({ name: "Mark", params: e.data })
              this.$router.push('mark')
              ;
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