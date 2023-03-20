<template>
  <div>
    <div class="list" :class="{ collapsed: isActive }">
      <div
        id="status"
        @click="handleClick"
        @keyup.enter="handleClick"
      >
        <div class="title">
          12 吋晶圓膜厚機 - 狀態資訊
        </div>
        <div>
          目前機台
          <span v-if="machineStatus == -1" class="badge badge-secondary device-status">
            關機中
          </span>
          <span v-else-if="machineStatus == 0" class="badge badge-success device-status">
            閒置中
          </span>
          <span v-else-if="machineStatus == 1" class="badge badge-warning device-status">
            運作中
          </span>
          <span v-else-if="machineStatus == 2" class="badge badge-danger device-status">
            發生問題
          </span>
        </div>
      </div>
      <div
        id="statistics"
        @click="handleClick"
        @keyup.enter="handleClick"
      >
        <div class="title">
          12 吋晶圓膜厚機 - 統計資訊
        </div>
        <div class="card">
            <span class="card-title">Standard Deviation</span>
            <p class="card-text">769.93 <span>Å</span></p>
        </div>
        <div class="card">
            <span class="card-title">Average</span>
            <p class="card-text">54954.8 <span>Å</span></p>
        </div>
        <div class="card">
            <span class="card-title">Uniformity</span>
            <p class="card-text">98.599 <span>Å</span></p>
        </div>
        <div class="card">
            <span class="card-title">Max</span>
            <p class="card-text">54954.8 <span>Å</span></p>
        </div>
        <div class="card">
            <span class="card-title">Min</span>
            <p class="card-text">54954.8 <span>Å</span></p>
        </div>
        <div class="card">
            <span class="card-title">Max - Min</span>
            <p class="card-text">54954.8 <span>Å</span></p>
        </div>
      </div>
    </div>
    <canvas id="renderCanvas" ref="renderCanvas" />
  </div>
</template>

<script>
// https://getbootstrap.com/docs/4.6/components/badge/
import { mapState } from 'vuex';
import '@babylonjs/loaders';
import {
  Engine, Scene, Color3, ArcRotateCamera, Vector3, SceneLoader, StandardMaterial,
} from '@babylonjs/core';
// import { createScene } from '../scenes/Scene';

export default {
  name: 'BabylonScene',
  data() {
    return {
      isActive: false,
      refScene: null,
    };
  },
  computed: {
    ...mapState(['machineStatus']),
    status() {
      return this.$store.state.machineStatus;
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
    // const renderCanvas = this.$refs.renderCanvas;
    // renderCanvas.width = window.innerWidth;
    // renderCanvas.height = window.innerHeight;
    // if (renderCanvas) {
    //   createScene(renderCanvas);
    // }
    // eslint-disable-next-line
    const canvas = this.$refs.renderCanvas;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    if (canvas) {
      const engine = new Engine(canvas);
      const scene = new Scene(engine);
      this.refScene = scene;
      console.log(`refScene: ${this.refScene}`);

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
    handleClick() {
      console.log('點擊了 div');
      this.isActive = !this.isActive;
    },
    initTricolorLight(meshName = '', r = 0.93, g = 0.93, b = 0.91) {
      console.log(`initTricolorLight__meshName: ${meshName}`);
      console.log(`initTricolorLight__r: ${r}`);
      console.log(`initTricolorLight__g: ${g}`);
      console.log(`initTricolorLight__b: ${b}`);
      const meshArray = ['Cylinder.022', 'Cylinder.020', 'Cylinder.018'];
      meshArray.forEach((element) => {
        const material = new StandardMaterial(this.refScene);
        material.alpha = 1;
        material.diffuseColor = new Color3(0.93, 0.93, 0.91);
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
      }
    },
  },
};
</script>
<style scoped>
#renderCanvas {
  touch-action: none;
}

#status{
  position: fixed;
  top: 10px;
  left: 10px;
  background: #ffffff;
  padding: 10px 20px;
  border-radius: 10px;
  width: 250px;
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
  top: 100px;
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
