<template>
  <div>
    <!-- Overlay móvil -->
    <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
      @click="$emit('update:isOpen', false)"></div>

    <aside :class="[
      'fixed md:relative top-0 left-0 h-full bg-[#162d38] text-white border-r flex flex-col transform transition-transform duration-300 z-50',
      isOpen ? 'translate-x-0' : '-translate-x-full',
      'md:translate-x-0 w-64'
    ]">
      <!-- Header -->
      <header class="p-4 flex items-center justify-between border-b border-gray-700">
        <!-- Botón para cerrar sidebar en móvil -->
        <button class="md:hidden text-white w-8 h-8 flex items-center justify-center hover:bg-gray-700 rounded"
          @click="$emit('update:isOpen', false)">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
            stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="text-lg font-semibold text-center flex-1">Menu</div>
        <!-- Espacio para equilibrar el header -->
        <div class="w-8"></div>
      </header>

      <!-- Menú -->
      <nav class="flex-1 overflow-y-auto px-2 py-4">
        <!-- Sección Principal -->
        <div class="mb-4">
          <div class="px-4 py-1 text-xs font-light text-gray-400 uppercase tracking-wide">Principal</div>
          <ul class="space-y-1">
            <li v-for="item in menuPrincipal" :key="item.text">
              <router-link :to="item.route" class="flex items-center gap-x-3 py-2 px-3 rounded hover:bg-[#ff6600]">
                <SvgIcon :name="item.icon" class="w-5 h-5" />
                <span class="truncate">{{ item.text }}</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Sección Mantenimiento -->
        <div class="mb-4">
          <div class="px-4 py-1 text-xs font-light text-gray-400 uppercase tracking-wide">Mantenimiento</div>
          <ul class="space-y-1">
            <li v-for="item in menuMantencion" :key="item.text">
              <router-link :to="item.route" class="flex items-center gap-x-3 py-2 px-3 rounded hover:bg-[#ff6600]">
                <SvgIcon :name="item.icon" class="w-5 h-5" />
                <span class="truncate">{{ item.text }}</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Sección Configuración -->
        <div>
          <div class="px-4 py-1 text-xs font-light text-gray-400 uppercase tracking-wide">Configuración</div>
          <ul class="space-y-1">
            <li v-for="item in menuConfiguracion" :key="item.text">
              <router-link :to="item.route" class="flex items-center gap-x-3 py-2 px-3 rounded hover:bg-[#ff6600]">
                <SvgIcon :name="item.icon" class="w-5 h-5" />
                <span class="truncate">{{ item.text }}</span>
              </router-link>
            </li>
          </ul>
        </div>
      </nav>
    </aside>
  </div>
</template>

<script>
import SvgIcon from '@/components/icons/SvgIcon.vue';

export default {
  name: "AppSidebar",
  components: { SvgIcon },
  props: { isOpen: { type: Boolean, default: false } },
  data() {
    return {
      menuPrincipal: [
        { text: "Dashboard", route: "/", icon: "dashboard" },
        { text: "Dispositivos", route: "/dispositivos", icon: "dispositivos" },
        { text: "Alertas", route: "/alertas", icon: "alertas" },
        { text: "Empresas", route: "/empresas", icon: "empresas" },
        { text: "Copec", route: "/copec", icon: "volumen" },
      ],
      menuMantencion: [
        { text: "Mantenciones", route: "/mantenciones", icon: "mantenciones" },
        { text: "Reportes", route: "/reportes", icon: "reportes" },
      ],
      menuConfiguracion: [
        { text: "Usuarios", route: "/usuarios", icon: "usuarios" },
        { text: "Fuentes de Datos", route: "/fuentes", icon: "fuentes" },
        { text: "Motor de Reglas", route: "/motor", icon: "motor" },
        { text: "Configuración", route: "/configuracion", icon: "configuracion" },
      ]
    };
  }
};
</script>
