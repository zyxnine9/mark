<template>
  <div>
    this is mark
    {{imgs}}
    <el-carousel 
    :autoplay="false"
    :loop="false"  
    indicator-position="none" 
    ref="ques">
      <el-carousel-item v-for="img in imgs" :key="img">
        <img :src=img alt="">
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  name: "",
  data() {
    return {
      images: []
    };
  },
  computed:{
    imgs(){
      console.log(this.images)
      return this.images.map(e=>"http://localhost:5000/image/"+e)
    }
  },
  created() {
    this.images = this.$route.params.images;
  }
};
</script>

<style lang="less" scoped>
</style>