<template>
  <div ref="line_chart" style="height:60vh;width:100vh"></div>
</template>

<script>
import echarts from "echarts";
export default {
  props: {
    data: Array
  },
  data() {
    return {};
  },
  computed: {
    lineData() {
      if (this.data) {
        let data = this.data;
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
      let option = {
        title: {
          text: "EMG数据"
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
            data: this.lineData
          }
        ]
      };
      let lineChart = echarts.init(this.$refs.line_chart);
      lineChart.setOption(option);
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