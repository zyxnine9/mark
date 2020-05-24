<template>
  <div>
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
      <el-col :span="12">Number Of Image</el-col>
      <el-col :span="12">
        <el-select
          class="option"
          v-model="chosenImageNumber"
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
      <el-col :span="12">Current Group</el-col>
      <el-col :span="12">
        <el-select
          class="option"
          v-model="user"
          :disabled="disabled"
          placeholder="please choose the group"
        >
          <el-option v-for="(item,index) in groupList" :key="index" :label="item" :value="item"></el-option>
        </el-select>
      </el-col>
    </el-row>

    <!--上传文件-->
    <div>
      <input style="display: none" type="file" @change="onFileSelected" ref="uploadFile" />
      <el-button type="primary" @click="$refs.uploadFile.click()">Choose own dataset</el-button>
      <span v-if="selectedFile">Current file is {{ selectedFile.name }}</span>
      <el-button type="primary" @click="onUpload">Upload</el-button>
      <el-progress
        v-if="uploadProgress"
        :text-inside="true"
        :stroke-width="26"
        :percentage="uploadProgress"
      ></el-progress>
      <span v-if="uploadHint">{{ uploadHint }}</span>
    </div>

    <el-button
      :disabled="disabled"
      type="primary"
      @click="detect"
      v-loading.fullscreen.lock="fullscreenLoading"
    >Detect</el-button>

    <div v-if="data">
      <el-carousel
        :autoplay="false"
        :loop="false"
        arrow="never"
        indicator-position="none"
        height="80vh"
        ref="ques"
      >
        <el-carousel-item v-for="(item,i) in data.ids" :key="i">
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
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { files, postFile, group,postValue } from "../assets/api";
import { emg } from "../assets/emg";
import LineChart from "../compoment/LineChart";

export default {
  name: "",
  data() {
    return {
      fullscreenLoading: false,
      disabled: false,
      selectedFile: null,
      fileList: [1, 2, 3],
      markImageNumberOption: [1, 3, 5, 10],
      uploadProgress: null,
      uploadHint: null,

      user: "",
      chosenFile: undefined,
      chosenImageNumber: null,
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
      this.disabled = false;
      const info = {
        user: this.user,
        chosenFile: this.chosenFile,
        chosenImageNumber: this.chosenImageNumber
      };
      console.log(info);
      this.data = emg;
      // TODO 网络请求
      axios.post(postValue,info).then(
        res=>{
          this.data = res.data
        }
      ).catch(error=>{
        console.log(error)
      })
    },
    toNext() {
      console.log('next')
      this.index++;
      this.$refs.ques.next();
    },

    canToNextPage() {
      return (
        this.labels[this.index] != undefined &&
        (this.index < this.data.ids.length )
      );
    },
    canPost() {
      return (
        this.labels[this.index] != undefined &&
        (this.index == this.data.ids.length)
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
      this.labels[this.index] = i;
      if (this.canToNextPage()) this.toNext();
      console.log(this.index)
      console.log(this.data.ids.length)
      if (this.canPost()) {
        this.$message("标注完了");
      }
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