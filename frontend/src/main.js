import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import filters from './utilities/filters'

import '@fortawesome/fontawesome-free/css/fontawesome.css'
import '@fortawesome/fontawesome-free/css/solid.css'
import './assets/main.scss'

// import { makeServer } from './mock/server'
// if (import.meta.env.MODE === 'development') {
//   makeServer()
// }

const app = createApp(App)

app.config.globalProperties.$filters = filters

app.use(createPinia())
app.use(router)

app.mount('#app')
