import '@babylonjs/loaders';
import {
  Engine, Scene, Color3, ArcRotateCamera, Vector3, SceneLoader,
} from '@babylonjs/core';

const createScene = (canvas) => {
  const engine = new Engine(canvas);
  const scene = new Scene(engine);

  scene.clearColor = new Color3(192, 221, 255);
  // eslint-disable-next-line
  const camera = new ArcRotateCamera('Camera', 0, 0.8, 10, Vector3.Zero(), scene);
  SceneLoader.Append('assets/', 'semi-v1.glb', scene, () => {
    scene.activeCamera = null;
    scene.createDefaultCameraOrLight(true);
    // scene.createDefaultCameraOrLight(true, true, true);
    scene.createDefaultEnvironment();
    scene.activeCamera.attachControl(canvas, false);
  });
  // SceneLoader.ImportMeshAsync('', '../assets/', 'semi-v1.glb', scene);
  // scene.activeCamera = null;
  // scene.createDefaultCameraOrLight(true);
  // scene.createDefaultEnvironment();
  // scene.activeCamera.attachControl(canvas, true);
  engine.runRenderLoop(() => {
    scene.render();
  });
  window.addEventListener('resize', () => {
    engine.resize();
  });
};
// eslint-disable-next-line
export { createScene };
