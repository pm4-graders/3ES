import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ScannerView from '../views/ScannerView.vue'
import ListView from '../views/ListView.vue'
import CorrectionsView from '../views/CorrectionsView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
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
      path: '/corrections',
      name: 'Korrigieren',
      component: CorrectionsView
    }
  ]
})

export default router
