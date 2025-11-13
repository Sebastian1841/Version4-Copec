import { createApp } from 'vue'
import App from './App.vue'
import router from './router'   // ✅ importa el router
import './style.css'

const app = createApp(App)

app.use(router)                 // ✅ registra el router
app.mount('#app')
