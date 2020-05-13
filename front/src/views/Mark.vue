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
      <el-carousel-item v-for="(array,i) in groupNumber" :key="i">
        <!-- <img v-bind:src="'data:image/jpeg;base64,'+img" /> -->
        <LineChart :fftdata="data.fft_datas[i]" :rawdata="data.raw_datas[i]" />
      </el-carousel-item>
    </el-carousel>
    <el-row>
      <el-col v-for="(v, i) in options" :key="i" :span="6">
        <el-button type="primary" @click="mark(i)">{{ v }}</el-button>
      </el-col>
    </el-row>
    <p>{{labels}}</p>
    <p>{{index}}</p>

    <!-- <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
      <span>跳转至首页</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="postData">确 定</el-button>
      </span>
    </el-dialog> -->
  </div>
</template>

<script>
import axios from "axios";
import storage from "../storage";
import { mapState } from "vuex";
import { retrain } from "../assets/api";
import LineChart from "../compoment/LineChart";
export default {
  name: "",
  data() {
    return {
      images: [],
      labels: [],
      ids: [],
      options: ["Active", "Rest", "Noisy", "Unknown"],
      index: 0,
      baseNumber: 0,
      groupNumber: 6,
      dialogVisible: false,
      data: undefined
    };
  },
  computed: {
    // imgs() {
    //   console.log(this.images);
    //   return this.images.map(e => "http://localhost:5000/image/" + e);
    // },
    ...mapState({
      data_: state => state.data
    }),
    nextButton() {
      if (this.index != this.groupNumber - 1) {
        return "下一个";
      }
      if (this.index == this.groupNumber - 1) {
        return "提交";
      }
      return "下一个";
    }
  },
  methods: {
    toNext() {
      this.index++;
      this.$refs.ques.next();
    },
    toPrev() {
      this.index--;

      this.$refs.ques.prev();
    },

    canToNextPage() {
      return (
        this.labels[this.index] != undefined &&
        this.index < this.groupNumber - 1
      );
    },
    canPost() {
      return (
        this.labels[this.index] != undefined &&
        this.index == this.groupNumber - 1
      );
    },
    submit() {
      console.log("canToNextPage  " + this.canToNextPage());
      console.log("can Post" + this.canPost());

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
    mark(i) {
      console.log('mark')
      this.labels[this.index] = i;
      if (this.canToNextPage()) this.toNext();
      if (this.canPost()){
        this.$message("标注完")
      }
    }
  },
  created() {
    const STORAGE_DATA = storage.getItem("data");
    console.log(STORAGE_DATA);
    console.log(this.data_);
    if (this.data_ == undefined && STORAGE_DATA) {
      this.data = STORAGE_DATA;
    }else{
      this.data = this.data_;
    }
  },
  components: {
    LineChart
  }
};
</script>

<style lang="less" scoped>
</style>