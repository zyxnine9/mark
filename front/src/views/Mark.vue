<template>
  <div>
    <el-carousel
      :autoplay="false"
      :loop="false"
      arrow="never"
      indicator-position="none"
      height="80vh"
      ref="ques"
    >
      <el-carousel-item v-for="img in images" :key="img">
        <img v-bind:src="'data:image/jpeg;base64,'+img" />
      </el-carousel-item>
    </el-carousel>
    <el-select v-model="labels[index]" placeholder="请选择">
      <el-option v-for="(item, index) in options" :key="item" :value="index" :label="item">{{item}}</el-option>
    </el-select>
    <el-row>
      <el-col :span="12">
        <el-button v-if="index" type="primary" @click="toPrev">上一个</el-button>
      </el-col>
      <el-col :span="12">
        <el-button type="primary" @click="submit">{{nextButton}}</el-button>
      </el-col>
    </el-row>

    <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
      <span>跳转至首页</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="postData">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";
<<<<<<< HEAD
=======
import { retrain } from "../assets/api"
>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
export default {
  name: "",
  data() {
    return {
      images: [],
      labels: [],
      ids: [],
      options: ["Active", "Rest", "Noisy", "Unknown"],
      index: 0,
<<<<<<< HEAD
      nextButton: "下一个",
=======
      // nextButton: "下一个",
>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
      dialogVisible: false
    };
  },
  computed: {
<<<<<<< HEAD
    imgs() {
      console.log(this.images);
      return this.images.map(e => "http://localhost:5000/image/" + e);
=======
    // imgs() {
    //   console.log(this.images);
    //   return this.images.map(e => "http://localhost:5000/image/" + e);
    // },
    nextButton() {
      if (this.index != this.images.length - 1) {
        return "下一个";
      }
      if (this.index == this.images.length - 1) {
        return "提交";
      }
      return "下一个";
>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
    }
  },
  methods: {
    toNext() {
      this.index++;
<<<<<<< HEAD
      console.log(this.index);
      console.log(this.images.length - 1);
      if (this.index == this.images.length - 1) {
        this.nextButton = "提交";
      }
=======

>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
      this.$refs.ques.next();
    },
    toPrev() {
      this.index--;
<<<<<<< HEAD
      if (!this.index == this.images.length - 1) {
        this.nextButton = "下一个";
      }
      this.$refs.ques.prev();
    },
    canToNextPage() {
      return (this.labels[this.index] != undefined) && this.index < this.images.length - 1;
    },
    canPost() {
      return (this.labels[this.index] != undefined) && this.index == this.images.length - 1;
    },
    submit() {
      console.log("canToNextPage  " + this.canToNextPage());
      
=======
    
      this.$refs.ques.prev();
    },

    canToNextPage() {
      return (
        this.labels[this.index] != undefined &&
        this.index < this.images.length - 1
      );
    },
    canPost() {
      return (
        this.labels[this.index] != undefined &&
        this.index == this.images.length - 1
      );
    },
    submit() {
      console.log("canToNextPage  " + this.canToNextPage());

>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
      if (this.canToNextPage()) {
        this.toNext();
      } else if (this.canPost()) {
        this.dialogVisible = true;
        // this.postData();
      } else {
        this.$message({
          message: "请标注",
          type: "warning"
        });
      }
    },
    postData() {
      axios
<<<<<<< HEAD
        .post("http://127.0.0.1:5000/retrain", {
=======
        .post(retrain, {
>>>>>>> 93601844cc75e63326eea7bb55903a8a9e654468
          ids: this.ids,
          labels: this.labels
        })
        .then(res => {
          console.log(res);
          this.$router.push("/");
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.ids = this.$route.params.ids;
    this.images = this.$route.params.images;
  }
};
</script>

<style lang="less" scoped>
</style>