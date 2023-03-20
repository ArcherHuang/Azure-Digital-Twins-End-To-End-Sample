// import FloatingVue from 'floating-vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faClockRotateLeft, faFileExcel, faCloudArrowDown } from '@fortawesome/free-solid-svg-icons';
import VTooltip from 'v-tooltip';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

// createApp(App).use(FloatingVue);
// createApp(App).use(VTooltip);
library.add(faClockRotateLeft, faFileExcel, faCloudArrowDown);
// createApp(App)
//   .component('font-awesome-icon', FontAwesomeIcon)
//   .mount('#app');

createApp(App)
  .use(store)
  .use(router)
  .use(VTooltip)
  .component('font-awesome-icon', FontAwesomeIcon)
  .mount('#app');
