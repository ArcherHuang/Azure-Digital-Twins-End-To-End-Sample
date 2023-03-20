<template>
  <div>
    <SpinnerModal v-if="isLoading" />
    <div class="list" :class="returnCollapsed">
      <div class="tool">
        <InfoModal
          v-if="showModal"
          :infos="infos"
          :from="from"
          @after-submit="handleAfterClose"
        />
        <span
          class="log"
          @click="() => toolClick('log')"
          @keyup.enter="() => toolClick('log')"
        >
          <font-awesome-icon class="icon" icon="fa-solid fa-clock-rotate-left" />
        </span>
        <span
          class="report"
          @click="() => toolClick('report')"
          @keyup.enter="() => toolClick('report')"
        >
          <font-awesome-icon class="icon" icon="fa-solid fa-file-excel" />
        </span>
      </div>
      <div
        id="status"
        @click="handleClick"
        @keyup.enter="handleClick"
        :class="{ mask: isDisable }"
      >
        <div class="title">
          12 吋晶圓膜厚機 - 狀態資訊
        </div>
        <div>
          目前機台
          <span
            v-if="machineStatus == -1"
            class="badge badge-secondary device-status"
            :class="{ mask: isDisable }"
          >
            關機中
          </span>
          <span
            v-else-if="machineStatus == 0"
            class="badge badge-success device-status"
            :class="{ mask: isDisable }"
          >
            閒置中
          </span>
          <span
            v-else-if="machineStatus == 1"
            class="badge badge-warning device-status"
            :class="{ mask: isDisable }"
          >
            運作中
          </span>
          <span
            v-else-if="machineStatus == 2"
            class="badge badge-danger device-status"
            :class="{ mask: isDisable }"
          >
            發生問題
          </span>
        </div>
      </div>
      <div
        id="statistics"
        @click="handleClick"
        @keyup.enter="handleClick"
        :class="{ mask: isDisable }"
      >
        <div class="title">
          12 吋晶圓膜厚機 - 統計資訊
        </div>
        <div class="card" :class="{ mask: isDisable }">
            <span class="card-title">Standard Deviation</span>
            <p class="card-text">{{ standardDeviation }} <span>Å</span></p>
        </div>
        <div class="card" :class="{ mask: isDisable }">
            <span class="card-title">Average</span>
            <p class="card-text">{{ average }} <span>Å</span></p>
        </div>
        <div class="card" :class="{ mask: isDisable }">
            <span class="card-title">Uniformity</span>
            <p class="card-text">{{ uniformity }} <span>Å</span></p>
        </div>
        <div class="card" :class="{ mask: isDisable }">
            <span class="card-title">Max</span>
            <p class="card-text">{{ max }} <span>Å</span></p>
        </div>
        <div class="card" :class="{ mask: isDisable }">
            <span class="card-title">Min</span>
            <p class="card-text">{{ min }} <span>Å</span></p>
        </div>
        <div class="card" :class="{ mask: isDisable }">
            <span class="card-title">Max - Min</span>
            <p class="card-text">{{ maxMin }} <span>Å</span></p>
        </div>
      </div>
    </div>
    <canvas id="renderCanvas" ref="renderCanvas" />
  </div>
</template>

<script>
// https://getbootstrap.com/docs/4.6/components/badge/
import axios from 'axios';
import { mapState } from 'vuex';
import '@babylonjs/loaders';
import {
  Engine, Scene, Color3, ArcRotateCamera, Vector3, SceneLoader, StandardMaterial,
} from '@babylonjs/core';
import InfoModal from '../components/InfoModal.vue';
import SpinnerModal from '../components/SpinnerModal.vue';

export default {
  name: 'BabylonScene',
  data() {
    return {
      isActive: false,
      isDisable: false,
      refScene: null,
      isLoading: false,
      infos: [],
      from: '',
      latestStatus: '',
    };
  },
  components: {
    SpinnerModal,
    InfoModal,
  },
  computed: {
    ...mapState(['machineStatus', 'standardDeviation', 'average', 'uniformity', 'max', 'min', 'maxMin']),
    status() {
      return this.$store.state.machineStatus;
    },
    showModal: {
      get() {
        return this.$store.state.showModal;
      },
      set(value) {
        this.$store.commit('setshowModal', value);
      },
    },
    returnCollapsed() {
      if (!this.isDisable) {
        return { collapsed: this.isActive };
      }
      return {};
    },
  },
  watch: {
    machineStatus: {
      deep: true,
      handler(value) {
        console.log(`The machine status has changed: ${value}`);
        this.setTricolorLight(value);
      },
    },
  },
  mounted() {
    this.getLatestStatusInfo();
    this.getLatestReportInfo();
    // eslint-disable-next-line
    const canvas = this.$refs.renderCanvas;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    if (canvas) {
      const engine = new Engine(canvas);
      const scene = new Scene(engine);
      this.refScene = scene;
      scene.clearColor = new Color3(192, 221, 255);
      // eslint-disable-next-line
      const camera = new ArcRotateCamera('Camera', 0, 0.8, 10, Vector3.Zero(), scene);
      SceneLoader.Append('assets/', 'semi-v1.glb', scene, () => {
        scene.activeCamera = null;
        scene.createDefaultCameraOrLight(true);
        scene.createDefaultEnvironment();
        scene.activeCamera.attachControl(canvas, false);
      });
      engine.runRenderLoop(() => {
        scene.render();
      });
      window.addEventListener('resize', () => {
        engine.resize();
      });
    }
  },
  methods: {
    async handleAfterClose() {
      this.isDisable = !this.isDisable;
    },
    toolClick(from) {
      console.log(`toolClick: ${from}`);
      if (from === 'log') {
        this.from = 'log';
        // const logUrl = 'https://dbops.kindmoss-da2b6540.japaneast.azurecontainerapps.io/logs';
        const logUrl = `https://${process.env.VUE_APP_API_URL}/logs`;
        this.getLogReportInfo(logUrl);
      } else if (from === 'report') {
        this.from = 'report';
        // const reportUrl = 'https://dbops.kindmoss-da2b6540.japaneast.azurecontainerapps.io/reports';
        const reportUrl = `https://${process.env.VUE_APP_API_URL}/reports`;
        this.getLogReportInfo(reportUrl);
      }
    },
    async getLogReportInfo(url) {
      try {
        this.isLoading = true;
        const { data } = await axios.get(url);
        console.log(`getLogExcelInfo: ${JSON.stringify(data)}`);
        this.infos = data.infos;
        console.log(`this.infos: ${JSON.stringify(this.infos)}`);
        this.isLoading = false;
        this.isDisable = !this.isDisable;
        this.showModal = true;
      } catch (err) {
        console.log(err);
        this.isLoading = false;
        this.isDisable = !this.isDisable;
      }
    },
    async getLatestStatusInfo() {
      try {
        this.isLoading = true;
        const { data } = await axios.get(`https://${process.env.VUE_APP_API_URL}/status/latest`);
        console.log(`getLatestStatusInfo: ${JSON.stringify(data)}`);
        this.latestStatus = data.infos.type;
        console.log(`this.infos: ${this.latestStatus}`);
        let value = {
          status: -1,
        };
        if (this.latestStatus === 'Idle') {
          value = {
            status: 0,
          };
        } else if (this.latestStatus === 'inOperation') {
          value = {
            status: 1,
          };
        } else if (this.latestStatus === 'Error') {
          value = {
            status: 2,
          };
        }
        this.$store.commit('setMachineStatus', value);
        this.isLoading = false;
      } catch (err) {
        console.log(err);
        this.isLoading = false;
      }
    },
    async getLatestReportInfo() {
      try {
        this.isLoading = true;
        const { data } = await axios.get(`https://${process.env.VUE_APP_API_URL}/reports/latest`);
        console.log(`getLatestReportInfo: ${JSON.stringify(data)}`);
        this.$store.commit('setMachineStatistics', {
          standardDeviation: data.infos.standard_deviation,
          average: data.infos.average,
          uniformity: data.infos.uniformity,
          max: data.infos.max,
          min: data.infos.min,
          maxMin: data.infos.max_min,
        });
        this.isLoading = false;
      } catch (err) {
        console.log(err);
        this.isLoading = false;
      }
    },
    handleClick() {
      this.isActive = !this.isActive;
    },
    initTricolorLight(meshName = '', r = 1, g = 1, b = 1) {
      console.log(`initTricolorLight__meshName: ${meshName}`);
      console.log(`initTricolorLight__r: ${r}`);
      console.log(`initTricolorLight__g: ${g}`);
      console.log(`initTricolorLight__b: ${b}`);
      const meshArray = ['Cylinder.022', 'Cylinder.020', 'Cylinder.018'];
      meshArray.forEach((element) => {
        const material = new StandardMaterial(this.refScene);
        material.alpha = 1;
        material.diffuseColor = new Color3(1, 1, 1);
        this.refScene.getMeshByName(element).material = material;
      });
      if (meshName !== '') {
        const material = new StandardMaterial(this.refScene);
        material.alpha = 1;
        material.diffuseColor = new Color3(r, g, b);
        this.refScene.getMeshByName(meshName).material = material;
      }
    },
    setTricolorLight(status) {
      console.log(`setTricolorLight__status: ${status}`);
      if (status === 2) {
        // Cylinder.022 紅 2
        this.initTricolorLight('Cylinder.022', 1, 0, 0);
      } else if (status === 1) {
        // Cylinder.020 橘 1
        this.initTricolorLight('Cylinder.020', 1, 0.57, 0);
      } else if (status === 0) {
        // Cylinder.018 綠 0
        this.initTricolorLight('Cylinder.018', 0, 1, 0);
      } else {
        this.initTricolorLight('', 1, 1, 1);
      }
    },
  },
};
</script>
<style scoped>
#renderCanvas {
  touch-action: none;
}

.tool {
  position: fixed;
  top: 5px;
  left: 10px;
  background: #ffffff;
  width: 250px;
  height: 35px;
  border-radius: 10px;
  padding-top: 6px;
}

.report {
  margin-left: 50px;
}

.log:hover::before {
  position: absolute;
  top: 5px;
  left: 9px;
  content: 'Log 資訊';
  background-color: black;
  color: white;
  border-radius: 7px;
  width: 73px;
}

.report:hover::before {
  position: absolute;
  top: 5px;
  left: 170px;
  content: 'Excel 資訊';
  background-color: black;
  color: white;
  border-radius: 7px;
  width: 78px;
}

.icon {
  color: gray;
  /* font-size: 3em; */
}

#status{
  position: fixed;
  top: 50px;
  left: 10px;
  background: #ffffff;
  padding: 10px 20px;
  border-radius: 10px;
  width: 250px;
}

.mask {
  background-color: #646464!important;
  color: #384654;
}
.device-status {
  font-size: 15px;
  margin-left: 3px;
  padding-top: 4px;
  padding-bottom: 2px;
}

.title {
  margin-bottom: 10px;
}

#statistics{
  position: fixed;
  top: 138px;
  left: 10px;
  background: #ffffff;
  padding: 10px 20px;
  border-radius: 10px;
  width: 250px;
}

.align-title span{
  text-align: left;
  display: block;
}

.card {
  height: 45px;
  margin: 8px;
  margin-top: 3px;
  padding: 1px;
  line-height: 1.2;
}
.card-title {
  font-size: 14px;
  margin-top: 5px;
  margin-bottom: 1px;
}

#log{
  position: fixed;
  top: 340px;
  left: 10px;
  background: #ffffff;
  padding: 10px 20px;
  border-radius: 10px;
  width: 250px;
}

.list.collapsed {
  transform: translateX(-235px);
}
</style>
