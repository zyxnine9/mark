<template>
<div>
  <el-row>
    <el-col :span="12"><div ref="line_chart1" style="height:60vh;width:100vh"></div></el-col>
    <el-col :span="12"><div ref="line_chart2" style="height:60vh;width:100vh"></div></el-col>
  </el-row>
</div>
 
</template>

<script>
import echarts from "echarts";
export default {
  props: {
    fftdata: Array,
    rawdata: Array
  },
  data() {
    return {};
  },
  computed: {
    FFTData() {
      if (this.fftdata) {
        let data = this.fftdata;
        for (let i = 0; i < data.length; i++) {
          data[i] = [i, data[i]];
        }
        return data;
      } else {
        return [
          [1, 2],
          [2, 4],
          [3, 9],
          [4, 550]
        ];
      }
    },
    RAWData() {
      if (this.rawdata) {
        let data = this.rawdata;
        for (let i = 0; i < data.length; i++) {
          data[i] = [i, data[i]];
        }
        return data;
      } else {
        return [
          [1, 2],
          [2, 4],
          [3, 9],
          [4, 550]
        ];
      }
    }
  },
  methods: {
    drawLineChart() {
      let option1 = {
        title: {
          text: "EMG FFT"
        },
        tooltip: {
          trigger: "axis",
          formatter: function(params) {
            params = params[0];
            return params.value[1];
          },
          axisPointer: {
            animation: false
          }
        },
        xAxis: {
          type: "value",
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: "value",
        //   boundaryGap: [0, ],
          splitLine: {
            show: false
          }
        },
        series: [
          {
            type: "line",
            showSymbol: false,
            hoverAnimation: false,
            data: this.FFTData
          }
        ]
      };
       let option2 = {
        title: {
          text: "EMG RAW"
        },
        tooltip: {
          trigger: "axis",
          formatter: function(params) {
            params = params[0];
            return params.value[1];
          },
          axisPointer: {
            animation: false
          }
        },
        xAxis: {
          type: "value",
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: "value",
        //   boundaryGap: [0, ],
          splitLine: {
            show: false
          }
        },
        series: [
          {
            type: "line",
            showSymbol: false,
            hoverAnimation: false,
            data: this.RAWData,
          }
        ]
      };
      let lineChart1 = echarts.init(this.$refs.line_chart1);
      let lineChart2 = echarts.init(this.$refs.line_chart2);
      lineChart1.setOption(option1);
      lineChart2.setOption(option2);
    }
  },
  mounted(){
      this.drawLineChart()
  },
  updated(){
      this.drawLineChart()
  }
};
</script>

<style lang="less" scoped>
</style>