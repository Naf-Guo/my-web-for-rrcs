<template>
  <div class="container">
    <p class="title">Introduction goes there</p>
    <div class="main">
      <div class="aside">
        <label class="upload">
          <el-button icon="el-icon-upload">click upload file</el-button>
          <p>{{ file.name }}</p>
          <input type="file" id="file" ref="file" @change="handleFileUpload()"/>
        </label>
        <el-input type="text" v-model="selected_chain" required placeholder="chain name"/>
        <el-input type="text" v-model="gpcrdb_id" required placeholder="gpcrdb id"/>
        <el-row>
        <el-col :span=4><el-button v-on:click="submitFile()">Submit</el-button></el-col>
        <el-col :span=16>{{jobtype}}</el-col>
        <el-col :span=8>{{message}}</el-col>
        </el-row>
      </div>
      <div class="content">
        <div class="topbar">
          <el-input type="text" v-model="BW_f" required placeholder="BW filter"/>
          <el-input type="text" v-model="res_f" required placeholder="res filter"/>
          <el-input type="text" v-model="resn_f" required placeholder="res num filter"/>
          <el-input type="text" v-model="helix1" required placeholder="helix num, eg: 1"/>
          <el-input type="text" v-model="helix2" required placeholder="if chosen, contact bewteen 2 helix" style="width: 260px;"/>
          <el-button v-on:click="filter()">Filter</el-button>
        </div>
        <el-table
          :data="rrcs_filtered"
          height="250"
          border
          :default-sort="{prop: 'score', order: 'descending'}"
        >
          <el-table-column prop="BW1" label="res1 BW num"></el-table-column>
          <el-table-column prop="res1" label="res1 type"></el-table-column>
          <el-table-column prop="res1n" label="res1 num"></el-table-column>
          <el-table-column prop="BW2" label="res2 BW num"></el-table-column>
          <el-table-column prop="res2" label="res2 type"></el-table-column>
          <el-table-column prop="res2n" label="res2 num"></el-table-column>
          <el-table-column prop="score" label="RRCS score"></el-table-column>
        </el-table>
      <div id='chart' ref='chart' style="width: 100%; height: 800px;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import echarts from 'echarts';

export default {
  data() {
    return {
      file: {},
      message: "",
      jobtype: "",
      selected_chain: "",
      gpcrdb_id: "",
      BW_f: '',
      res_f: '',
      resn_f: '',
      helix1: '',
      helix2: '',
      rrcs: [],
      rrcs_filtered: []
    };
  },
  methods: {
    plot_chart(){
        var chart = echarts.init(document.getElementById('chart'));
        var mynodes = [];
        var mylinks = [];
        for (var k = 0; k < this.rrcs_filtered.length; k++){
            var node1 = this.rrcs_filtered[k]['BW1'];
            var node2 = this.rrcs_filtered[k]['BW2'];
            mynodes.push(node1);
            mynodes.push(node2);
            var myscore = parseFloat(this.rrcs_filtered[k]['score']);
            mylinks.push({source:node1, target:node2, value:15.0/myscore, lineStyle: {width: myscore}});
        }
        mynodes = Array.from(new Set(mynodes));
        var node_list = [];
        for (var l = 0; l < mynodes.length; l++){
            var cols = ['magenta','red','orange','brown','green','blue','indigo','purple','violet'];
            for (var m = 0; m < mynodes[l].length; m++){
                if (mynodes[l][m] == '.'){
                    break;
                }
            }
            var mark = mynodes[l].slice(0,m);
            var col;
            if (mark=='1'){col = cols[1]}
            else if (mark=='2'){col = cols[2]}
            else if (mark=='3'){col = cols[3]}
            else if (mark=='4'){col = cols[4]}
            else if (mark=='5'){col = cols[5]}
            else if (mark=='6'){col = cols[6]}
            else if (mark=='7'){col = cols[7]}
            else if (mark=='8'){col = cols[8]}
            else {col = cols[0]}
            node_list.push({name:mynodes[l],draggable:true,itemStyle:{color:col}});
        }
        var option = {
            series:[
                {
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 10,
                    roam: true,
                    data: node_list,
                    links: mylinks,
                    force: {repulsion: 100},
                }
            ]
        }
        chart.setOption(option);
    },
    filter(){
        this.rrcs_filtered = [];
        for (var j = 0; j < this.rrcs.length; j++) {
            var tmp = this.rrcs[j];
            if (this.BW_f != '' && tmp['BW1'] != this.BW_f && tmp['BW2'] != this.BW_f){continue;}
            if (this.res_f != '' && tmp['res1'] != this.res_f && tmp['res2'] != this.res_f){continue;}
            if (this.resn_f != '' && tmp['res1n'] != this.resn_f && tmp['res2n'] != this.resn_f){continue;}
            for (var m = 0; m < tmp['BW1'].length; m++){
                if (tmp['BW1'][m] == '.'){
                    break;
                }
            }
            var mark1 = tmp['BW1'].slice(0,m);
             for (m = 0; m < tmp['BW2'].length; m++){
                if (tmp['BW2'][m] == '.'){
                    break;
                }
            }
            var mark2 = tmp['BW2'].slice(0,m);
            if (this.helix1 != '' && this.helix2 == ''){
                if (mark1 != this.helix1 && mark2 != this.helix1){continue;}
            }
            if (this.helix1 != '' && this.helix2 != ''){
                if (!((mark1 == this.helix1 && mark2 == this.helix2)||(mark1 == this.helix2 && mark2 == this.helix1))){continue;}
            }
            this.rrcs_filtered.push(tmp);
        }
      this.BW_f = '';
      this.res_f = '';
      this.resn_f = '';
      this.plot_chart();
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    submitFile() {
      this.rrcs=[];
      this.message = "";
      let formData = new FormData();
      formData.append("file", this.file);
      formData.append("gpcrdb_id", this.gpcrdb_id);
      formData.append("chain", this.selected_chain);
      let self = this;
      self.jobtype = "calcutating! Please wait for 1-2 minutes.";
      axios
        .post("http://localhost:5000/rrcs-cal", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        })
        .then(function(response) {
          self.jobtype = "Done";
          for (var i = 0; i < response.data["rrcs_result"].length; i++) {
            var line = response.data["rrcs_result"][i];
            self.rrcs.push({
              BW1: line[0],
              res1: line[1],
              res1n: line[2],
              BW2: line[3],
              res2: line[4],
              res2n: line[5],
              score: line[6]
            });
          }
          self.rrcs_filtered = self.rrcs;
          self.plot_chart();
        })
        .catch(function() {
          self.message = "something wrong";
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.title {
  text-align: center;
  margin-bottom: 10px;
}

.main {
  display: flex;
}

.aside {
  width: 360px;
  margin-right: 10px;
  flex: none;
  .el-button {
    height: 40px;
  }
  .el-input {
    margin-bottom: 10px;
  }
}

.upload {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  p {
    margin-left: 8px;
  }
  input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
  }
}

.content {
  flex: auto;
}

.topbar {
  display: flex;
  align-items: flex-start;
  .el-input {
    width: 200px;
    margin-right: 10px;
    margin-bottom: 10px;
  }
}
</style>

