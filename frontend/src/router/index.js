import { createRouter, createWebHistory } from 'vue-router'
import OptionsView from '../views/OptionsView.vue'
import ScannerView from '../views/ScannerView.vue'
import ListView from '../views/ListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'options',
      component: OptionsView
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
