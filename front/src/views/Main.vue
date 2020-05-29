<template>
  <div>
    <h1 style="text-align:center">Online Annotation System</h1>
    <el-row>
      <!--基本信息填写-->
      <el-col :span="16">
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
          <el-col :span="12">Current Group</el-col>
          <el-col :span="12">
            <el-select
              class="option"
              v-model="groupName"
              :disabled="disabled || !groupList"
              placeholder="please choose the group"
            >
              <el-option v-for="(item,index) in groupList" :key="index" :label="item" :value="item"></el-option>
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
              :disabled="disabled || (groupName==null)"
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
      </el-col>

      <!--上传文件-->
      <el-col :span="8">
        <el-row class="block">
          <input style="display: none" type="file" @change="onFileSelected" ref="uploadFile" />
          <el-button type="primary" @click="$refs.uploadFile.click()">Upload New Dataset</el-button>
          <span>( .mat format )</span>
        </el-row>
        <el-row class="block">
          <el-button type="primary" v-if="selectedFile != null" @click="onUpload">Upload</el-button>
          <el-row class="block">
            <span v-if="selectedFile">Current file is {{ selectedFile.name }}</span>
          </el-row>
        </el-row>
        <el-row class="block">
          <el-progress
            v-if="uploadProgress"
            :text-inside="true"
            :stroke-width="26"
            :percentage="uploadProgress"
          ></el-progress>
        </el-row>
      </el-col>
    </el-row>

    <!-- 上传信息获取数据-->
    <div style="text-align:center">
      <el-button
        ref="start"
        type="primary"
        @click="detect"
        v-loading.fullscreen.lock="fullscreenLoading"
      >Start Annotation</el-button>
    </div>

    <!--标注模块-->
    <transition name="fade">
      <div v-if="data">
        <!-- EMG图例 -->
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
            <el-row>
              <el-col :span="6">
                <div class="wrap" @click="showIdAndAnnotation = true">
                  <el-link type="primary">click here for machine annotation</el-link>
                </div>
              </el-col>
              <transition name="fade">
                <el-col :span="18" v-show="showIdAndAnnotation">
                  <p>{{data.ids[i]}}</p>
                  <p>{{data.title[i]}}</p>
                </el-col>
              </transition>
            </el-row>

            <LineChart :fftdata="data.fft_datas[i]" :rawdata="data.raw_datas[i]" />
          </el-carousel-item>
        </el-carousel>

        <el-row style="text-align:center" type="flex" justify="center" :gutter="20">
          <el-col v-for="(v, i) in options" :key="i" :span="3">
            <el-button style="width:100%" type="primary" @click="mark(i)">{{ v }}</el-button>
          </el-col>
        </el-row>

        <!-- 下载文件 -->
        <el-row  type="flex" justify="center" :gutter="20" style="text-align:center;margin-top:20px">
          <el-col  :span="8">
            <span style="vertical-align: middle;">Current Annotation Number is {{markedImageNumber}}</span>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="$refs.download.click()">Download Annotation Reuslt</el-button>
          </el-col>
          <el-col :span="8">
            <span style="vertical-align: middle;">(.csv format)</span>
          </el-col>
        </el-row>
        <a
          style="display:none"
          ref="download"
          :href=" 'https://www.jackren.cn/mark/api/download?timeline=' + new Date().valueOf()"
        >file</a>
      </div>
    </transition>

    <div>
      <el-dialog title="Hint" :visible.sync="dialogVisible" width="30%">
        <span>You have finished the annotation work, the result will automatically submit and get into next round, you can choose not do that</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="index = 0;data = null;labels = [];markedImageNumber=markedImageNumber-10">Cancel</el-button>
          <el-button type="primary" @click="retrain">Accept</el-button>
        </span>
      </el-dialog>
    </div>

        <div>
      <el-dialog title="Hint" :visible.sync="allFinishedDialogVisible" width="30%">
        <span>You have finished this part of annotation work, you can choose other group or signal to continue work </span>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="index = 0;data = null;labels = [];">Accept</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { files, postFile, group, postValue, retrain } from "../assets/api";
import { number } from "../assets/api";
import LineChart from "../compoment/LineChart";

export default {
  name: "",
  data() {
    return {
      fullscreenLoading: false,
      disabled: false,
      uploadProgress: null,
      uploadHint: null,
      showIdAndAnnotation: false,

      selectedFile: null,
      fileList: [],
      markImageNumberOption: [0, 1, 2, 3],
      signalNumberOption: [],

      groupName: null,
      chosenFile: undefined,
      chosenSignalChannel: null,
      chosenSignalNumber: null,

      groupList: null,
      options: ["Active", "Rest", "Noisy", "Unknown"],
      index: 0,
      data: null,
      labels: [],
      markedImageNumber: 0,
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
        .get(number + "?groupName=" + this.groupName)
        .then(res => {
          const number = res.data.signalNumber;
          this.signalNumberOption = [...Array(number + 1).keys()];
        })
        .catch(error => {
          console.log(error);
        });
    }
  },

  computed: {
    dialogVisible() {
      if (this.data  && this.data.ids.length == 0){
        return false;
      }
      if (this.index == this.chosenImageNumber) {
        return true;
      } else {
        return false;
      }
    },
    chosenImageNumber(){
      if(this.data){
        return this.data.ids.length
      }
      return 10;
      
    },
    allFinishedDialogVisible(){
      if (this.data != null && this.data.ids.length == 0){
        return true;
      } 
      return false;
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
      let format = this.selectedFile.name.split(".");
      format = format[format.length - 1];
      if (format != "mat") {
        this.selectedFile = null;
        this.$message({
          type: "warning",
          message: "please upload a .mat format file"
        });
      }
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
              // this.uploadHint = "success upload";
              this.$message("success upload");
              this.selectedFile = null;
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
          chosenSignalNumber: this.chosenSignalNumber,
          chosenSignalChannel: this.chosenSignalChannel
        };
        console.log(info);
        this.fullscreenLoading = true;
        // this.data = emg;
        // TODO 网络请求
        axios
          .post(postValue, info)
          .then(res => {
            this.data = res.data;
            // console.log(this.data);
            this.fullscreenLoading = false;
            if (this.data.ids.length == 0 ){//标注完
              this.disabled = false;
            }
          })
          .catch(error => {
            console.log(error);
            this.fullscreenLoading = false;
            this.$message("Network Error");
          });
      } else {
        this.$message("please complete the table");
      }
    },
    // 标记相关功能
    toNext() {
      this.index++;
      this.markedImageNumber++;
      this.$refs.ques.next();
    },
    canToNextPage() {
      return (
        this.labels[this.index] != undefined &&
        // (this.index < this.data.ids.length )
        this.index < this.chosenImageNumber
      );
    },

    mark(i) {
      this.labels[this.index] = i;
      if (this.canToNextPage()) this.toNext();
 
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
          this.index = 0;
          this.data = null;
          this.labels = [];
          this.detect()
        })
        .catch(error => {
          console.log(error)
          this.$message("there are errors");
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
.wrap {
  display: inline-block;
  vertical-align: center;
  margin-top: 10%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>