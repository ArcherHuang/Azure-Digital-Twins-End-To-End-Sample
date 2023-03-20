import { createStore } from 'vuex';

export default createStore({
  state: {
    machineStatus: -1,
    standardDeviation: 0,
    average: 0,
    uniformity: 0,
    max: 0,
    min: 0,
    maxMin: 0,
    showModal: false,
  },
  getters: {
  },
  mutations: {
    setMachineStatus(state, machine) {
      state.machineStatus = machine.status;
      console.log(`machine.status: ${machine.status}`);
    },
    setMachineStatistics(state, machine) {
      state.standardDeviation = machine.standardDeviation;
      state.average = machine.average;
      state.uniformity = machine.uniformity;
      state.max = machine.max;
      state.min = machine.min;
      state.maxMin = machine.maxMin;
      console.log(`machine.standardDeviation: ${machine.standardDeviation}`);
      console.log(`machine.average: ${machine.average}`);
      console.log(`machine.uniformity: ${machine.uniformity}`);
      console.log(`machine.max: ${machine.max}`);
      console.log(`machine.min: ${machine.min}`);
      console.log(`machine.maxMin: ${machine.maxMin}`);
    },
    setshowModal(state, payload) {
      state.showModal = payload;
    },
  },
  actions: {
  },
  modules: {
  },
});
