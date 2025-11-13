<template>
  <div class="fixed inset-0 flex flex-col bg-gray-50 overflow-hidden font-sans">

    <AppHeader @toggle-sidebar="toggleSidebar" />

    <div class="flex flex-1 overflow-hidden">
      <AppSidebar :isOpen="showSidebar" @update:isOpen="val => showSidebar = val" />

      <!-- ✅ Solo el main hace scroll -->
      <main class="flex-1 p-6 overflow-auto bg-[#f3f3f3]">
        <router-view />
      </main>
    </div>

  </div>
</template>

<script>
import AppHeader from './components/Layout/AppHeader.vue'
import AppSidebar from './components/Layout/AppSidebar.vue'

export default {
  name: 'App',
  components: { AppHeader, AppSidebar },
  data() {
    return {
      showSidebar: false
    }
  },
  methods: {
    toggleSidebar() {
      this.showSidebar = !this.showSidebar
    }
  }
}
</script>
