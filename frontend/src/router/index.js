import { createRouter, createWebHistory } from 'vue-router'

import Copec from '@/Views/Dashboard.vue'

const routes = [
  { path: '/', name: 'copec', component: Copec },       // ✅ default
  { path: '/copec', redirect: '/' },                    // ✅ opcional
  { path: '/:pathMatch(.*)*', redirect: '/' }           
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ Eliminamos guard de login
export default router
