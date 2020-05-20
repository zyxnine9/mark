<template>
  <div>
    <el-row class="block">
      <el-col :span="12">File Name</el-col>
      <el-col :span="12">
        <el-select
          class="option"
          v-model="chosenFile"
          :disabled="disabled"
          placeholder="please choose the file"
        >
          <el-option v-for="(item,index) in fileList" :key="item" :label="item" :value="index"></el-option>
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
            :key="item"
            :label="item"
            :value="index"
          ></el-option>
        </el-select>
      </el-col>
    </el-row>

    <el-row class="block">
      <el-col :span="12">Current Group</el-col>
      <el-col :span="12">
        <el-input
          class="option"
          v-model="user"
          :disabled="disabled"
          placeholder="please input user name"
        ></el-input>
      </el-col>
    </el-row>

    <input style="display: none" type="file" @change="onFileSelected" ref="uploadFile" />
    <el-button type="primary" @click="$refs.uploadFile.click()">Choose own dataset</el-button>
    <span v-if="selectedFile">Current file is {{ selectedFile.name }}</span>
    <el-button type="primary" @click="onUpload">Upload</el-button>
    <el-progress v-if="uploadProgress" :text-inside="true" :stroke-width="26" :percentage="uploadProgress"></el-progress>
    <span v-if="uploadHint">{{ uploadHint }}</span>
    <el-button
      :disabled="disabled"
      type="primary"
      @click="disabled = !disabled"
      v-loading.fullscreen.lock="fullscreenLoading"
    >Pretrain the model</el-button>

    <div v-if="data">
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
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { files, postFile } from "../assets/api";
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
      chosenFile: "",
      chosenImageNumber: "",

      options: ["Active", "Rest", "Noisy", "Unknown"],
      index: 0,
      data: null
    };
  },
  methods: {
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
    onFileSelected(event) {
      this.selectedFile = event.target.files[0];
    },
    onUpload() {
      const fd = new FormData();
      fd.append("dataset", this.selectedFile, this.selectedFile.name);
      console.log(this.selectedFile);
      axios.post(postFile, fd, {
        onUploadProgress : uploadEvent => {
           this.uploadProgress = Math.round(uploadEvent.loaded / uploadEvent.total * 100) 
           if(this.uploadProgress == 100){
             this.uploadHint = "上传完成" 
           }
        }
      }).then(res => {
        console.log(res);
      });
    }
  },
  mounted() {
    this.getFileList();
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