import { createRouter, createWebHashHistory } from 'vue-router';
import IndoorView from '../views/IndoorView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: IndoorView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
