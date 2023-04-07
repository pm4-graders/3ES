import { createRouter, createWebHistory } from 'vue-router'
import OptionsView from '../views/OptionsView.vue'
import ScannerView from '../views/ScannerView.vue'
import ListView from '../views/ListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: OptionsView
    },
    {
      path: '/scanner',
      name: 'Scanner',
      component: ScannerView
    },
    {
      path: '/list',
      name: 'List',
      component: ListView
    },
    {
      path: '/settings',
      name: 'Settings',
      component: OptionsView
    }
  ]
})

export default router
