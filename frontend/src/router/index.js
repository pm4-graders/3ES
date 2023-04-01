import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ScannerView from '../views/ScannerView.vue'
import ListView from '../views/ListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/scanner',
      name: 'scanner',
      component: ScannerView 
    },
    {
      path: '/list',
      name: 'List',
      component: ListView 
    },
  ]
})

export default router
