<template>
  <header class="bg-[#1f2937] border-b border-gray-700 flex justify-between items-center px-3 py-2">
    <div class="flex items-center gap-2">
      <button class="md:hidden text-white text-2xl px-6" @click="$emit('toggle-sidebar')">☰</button>

      <img
        alt="Logo"
        src="https://www.gpsenchile.com/wp-content/uploads/2023/06/logowebblanco.png"
        class="w-36 h-15"
      />
    </div>
  </header>
</template>

<script setup>
const emit = defineEmits(['toggle-sidebar'])
</script>
