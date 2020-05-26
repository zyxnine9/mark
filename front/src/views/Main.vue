<template>
  <div>
    <h1 style="text-align:center">Online Annotation System</h1>
    <!--基本信息填写-->
    <el-row class="block">
      <el-col :span="12">File Name</el-col>
      <el-col :span="12">
        <el-select
          class="option"
          v-model="chosenFile"
          :disabled="disabled"
          placeholder="please choose the file"
        >
          <el-option v-for="(item,index) in fileList" :key="index" :label="item" :value="item"></el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row class="block">
      <el-col :span="12">Signal Channel</el-col>
      <el-col :span="12">
        <el-select
          class="option"
          v-model="chosenSignalChannel"
          :disabled="disabled"
          placeholder="please choose the number"
        >
          <el-option
            v-for="(item,index) in markImageNumberOption"
            :key="index"
            :label="item"
            :value="item"
          ></el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row class="block">
      <el-col :span="12">Signal Number</el-col>
      <el-col :span="12">
        <el-select
          class="option"
          v-model="chosenSignalNumber"
          :disabled="disabled"
          placeholder="please choose the number"
        >
          <el-option
            v-for="(item,index) in signalNumberOption"
            :key="index"
            :label="item"
            :value="item"
          ></el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row class="block">
      <el-col :span="12">Current Group</el-col>
      <el-col :span="12">
        <el-select
          class="option"
          v-model="groupName"
          :disabled="disabled"
          placeholder="please choose the group"
        >
          <el-option v-for="(item,index) in groupList" :key="index" :label="item" :value="item"></el-option>
        </el-select>
      </el-col>
    </el-row>

    <!--上传文件-->
    <div style="text-align:center">
      <input style="display: none" type="file" @change="onFileSelected" ref="uploadFile" />
      <el-button type="primary" @click="$refs.uploadFile.click()">Choose own dataset</el-button>
      <el-button type="primary" v-if="selectedFile != null" @click="onUpload">Upload</el-button>
      <el-row>
        <span v-if="selectedFile">Current file is {{ selectedFile.name }}</span>
      </el-row>
      <el-progress
        v-if="uploadProgress"
        :text-inside="true"
        :stroke-width="26"
        :percentage="uploadProgress"
      ></el-progress>
      <span v-if="uploadHint">{{ uploadHint }}</span>
    </div>
    <br />

    <div style="text-align:center">
      <!-- 上传信息获取数据-->
      <el-button type="primary" @click="detect" v-loading.fullscreen.lock="fullscreenLoading">Start</el-button>

      <!-- 下载文件 -->
      <el-button type="primary" @click="$refs.download.click()">Download</el-button>
      <a style="display:none" ref="download" href="https://www.jackren.cn/mark/api/download">file</a>
    </div>

    <!--标注模块-->
    <div v-if="data">
      <el-carousel
        :autoplay="false"
        :loop="false"
        arrow="never"
        indicator-position="none"
        height="80vh"
        ref="ques"
      >
        <el-carousel-item v-for="(item,i) in data.ids.slice(0,chosenImageNumber)" :key="i">
          <!-- <img v-bind:src="'data:image/jpeg;base64,'+img" /> -->
          <p>{{data.ids[i]}}</p>
          <p>{{data.title[i]}}</p>
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
    </div>

    <div>
      <el-dialog title="Hint" :visible.sync="dialogVisible" width="30%">
        <span>You have finished the annotation work, please sumbit the result</span>
        <span slot="footer" class="dialog-footer">
          <!-- <el-button @click="dialogVisible = false">Cancel</el-button> -->
          <el-button type="primary" @click="retrain">Accept</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { files, postFile, group, postValue, retrain } from "../assets/api";
import { number } from '../assets/api'
import LineChart from "../compoment/LineChart";

export default {
  name: "",
  data() {
    return {
      fullscreenLoading: false,
      disabled: false,
      uploadProgress: null,
      uploadHint: null,

      selectedFile: null,
      fileList: [1, 2, 3],
      markImageNumberOption: [0,1,2,3],
      signalNumberOption:[],

      groupName: "",
      chosenFile: undefined,
      chosenImageNumber: 10,
      chosenSignalChannel: null,
      chosenSignalNumber: null,

      groupList: null,
      options: ["Active", "Rest", "Noisy", "Unknown"],
      index: 0,
      data: null,
      labels: []
    };
  },

  watch: {
    chosenFile: function() {
      axios
        .post(group, { dataset_name: this.chosenFile })
        .then(res => {
          this.groupList = res.data.group_name;
          console.log(this.groupList);
        })
        .catch(error => {
          console.log(error);
        });
    },
    groupName: function() {
      axios
      .get(number + '?groupName='+this.groupName)
      .then(res=>{
        const number = res.data.signalNumber
        this.signalNumberOption = [...Array(number+1).keys()]
      })
      .catch(error=>{
        console.log(error)
      })
    }

  },

  computed: {
    dialogVisible() {
      if (this.index == this.chosenImageNumber) {
        return true;
      } else {
        return false;
      }
    }
  },
  methods: {
    // 获取数据集列表
    getFileList() {
      axios
        .get(files)
        .then(res => {
          this.fileList = res.data.files;
        })
        .catch(error => {
          console.log(error);
        });
    },
    // 获取选择上传的数据集名
    onFileSelected(event) {
      this.selectedFile = event.target.files[0];
    },
    // 上传自己的数据集到服务器
    onUpload() {
      const fd = new FormData();
      fd.append("dataset", this.selectedFile, this.selectedFile.name);
      console.log(this.selectedFile);
      axios
        .post(postFile, fd, {
          onUploadProgress: uploadEvent => {
            this.uploadProgress = Math.round(
              (uploadEvent.loaded / uploadEvent.total) * 100
            );
            if (this.uploadProgress == 100) {
              this.uploadHint = "上传完成";
            }
          }
        })
        .then(res => {
          console.log(res);
        });
    },
    // 训练模型,获取fft数据
    detect() {
      if (
        this.chosenSignalChannel != null &&
        this.chosenSignalNumber != null &&
        this.chosenFile &&
        this.groupName
      ) {
        this.disabled = true;
        const info = {
          groupName: this.groupName,
          chosenFile: this.chosenFile,
          chosenSignalNumber: 1,
          chosenSignalChannel: 2,
        };
        console.log(info);
        this.fullscreenLoading = true;
        // this.data = emg;
        // TODO 网络请求
        axios
          .post(postValue, info)
          .then(res => {
            this.data = res.data;
            console.log(this.data);
            this.fullscreenLoading = false;
          })
          .catch(error => {
            console.log(error);
            this.fullscreenLoading = false;
            this.$message("网络错误");
          });
      } else {
        this.$message("please complete the table");
      }
    },
    // 标记相关功能
    toNext() {
      this.index++;
      this.$refs.ques.next();
    },
    canToNextPage() {
      return (
        this.labels[this.index] != undefined &&
        // (this.index < this.data.ids.length )
        this.index < this.chosenImageNumber
      );
    },
    canPost() {
      return (
        this.labels[this.index] != undefined &&
        // (this.index == this.data.ids.length)
        this.index == this.chosenImageNumber
      );
    },
    mark(i) {
      this.labels[this.index] = i;
      if (this.canToNextPage()) this.toNext();
      if (this.canPost()) {
        this.$message("标注完了");
      }
    },
    // 上传label
    retrain() {
      const info = {
        ids: this.data.ids.slice(0, this.chosenImageNumber),
        titles: this.data.title.slice(0, this.chosenImageNumber),
        labels: this.labels
      };
      axios
        .post(retrain, info)
        .then(res => {
          this.$message("finished");
          this.index = 0;
          this.data = null;
          this.labels = [];
        })
        .catch(error => {
          this.$message("error");
        });
    }
  },
  mounted() {
    this.getFileList();
  },
  components: {
    LineChart
  }
};
</script>

<style scoped>
.option {
  width: 80%;
}
.block {
  margin: 8px;
  text-align: center;
}
</style>