import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MaintenanceView from '../views/MaintenanceView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/maintenance',
      name: 'maintenance',
      component: MaintenanceView
    }
  ],
})

export default router
