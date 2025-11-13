<template>
  <div class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-2 sm:p-4">
    <div
      class="relative bg-white w-full max-w-lg p-4 sm:p-6 rounded-2xl shadow-xl border border-[#E7E7E9] space-y-6
             max-h-[88vh] overflow-y-auto animate-scale-in
             scale-[0.9] sm:scale-100"
    >
      <!-- Botón cerrar -->
      <button
        @click="$emit('close')"
        class="absolute right-3 top-3 sm:right-4 sm:top-4 text-lg sm:text-xl text-[#1D292F] hover:text-[#FF6600] transition"
      >
        ✕
      </button>

      <!-- Título -->
      <h2 class="text-center text-base sm:text-lg font-semibold text-[#102372]">Agregar Datos</h2>
      <hr class="border-[#E7E7E9]" />

      <!-- Fecha + Litros -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        <div class="flex flex-col">
          <label class="text-[10px] sm:text-xs text-[#1D292F] font-medium mb-1">Fecha</label>
          <div class="flex items-center gap-2">
            <input v-model="form.fecha" type="date" class="input flex-1" />
            <SvgIcon name="calendar" class="w-4 h-4 sm:w-5 sm:h-5 text-[#1D292F]" />
          </div>
        </div>

        <div class="flex flex-col">
          <label class="text-[10px] sm:text-xs text-[#1D292F] font-medium mb-1">Litros</label>
          <input v-model.number="form.litros" type="number" step="0.01" class="input" />
        </div>
      </div>

      <!-- Tipo -->
      <div class="flex flex-col">
        <label class="text-[10px] sm:text-xs text-[#1D292F] font-medium mb-1">Tipo de descarga</label>
        <input v-model="form.tipo_descarga" type="text" class="input" />
      </div>

      <!-- Encargado + Dispositivo -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        <div class="flex flex-col">
          <label class="text-[10px] sm:text-xs text-[#1D292F] font-medium mb-1">Encargado</label>
          <input v-model="form.encargado" type="text" class="input" />
        </div>

        <div class="flex flex-col">
          <label class="text-[10px] sm:text-xs text-[#1D292F] font-medium mb-1">Dispositivo</label>
          <select v-model="form.dispositivo" class="input cursor-pointer">
            <option disabled value="">Seleccionar...</option>
            <option>Dispositivo 1</option>
            <option>Dispositivo 2</option>
            <option>Dispositivo 3</option>
          </select>
        </div>
      </div>

      <!-- Botones -->
      <div class="flex flex-col sm:flex-row justify-between gap-3 pt-1 sm:pt-2">
        <button
          @click="$emit('close')"
          class="w-full px-6 py-2 text-[11px] sm:text-xs bg-gray-200 hover:bg-gray-300 rounded-lg font-medium transition"
        >
          Cancelar
        </button>

        <button
          @click="guardar"
          class="w-full px-6 py-2 text-[11px] sm:text-xs bg-[#FF6600] text-white rounded-lg font-medium hover:bg-[#d95400] transition"
        >
          Guardar
        </button>
      </div>

    </div>
  </div>
</template>

<script>
import SvgIcon from "@/components/icons/SvgIcon.vue";

export default {
  components: { SvgIcon },
  emits: ["close", "saved"],
  data() {
    return {
      form: {
        fecha: "",
        litros: "",
        tipo_descarga: "",
        encargado: "",
        dispositivo: "",
      },
    };
  },
  methods: {
    async guardar() {
      if (!this.form.fecha || !this.form.litros) {
        alert("Fecha y litros son obligatorios");
        return;
      }

      try {
        const res = await fetch(`${import.meta.env.VITE_API}/descarga/manual`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form),
        });

        if (!res.ok) {
          alert("❌ Error al guardar el registro");
          return;
        }

        this.$emit("saved");
        this.$emit("close");

      } catch (err) {
        alert("❌ Error de conexión con el servidor");
      }
    }
  }
};
</script>

<style scoped>
.input {
  width: 100%;
  border: 1px solid #E7E7E9;
  border-radius: 8px;
  background: #F7F7F8;
  padding: 6px 8px;
  font-size: 11px; /* más pequeño en móvil */
  transition: 0.2s;
}
.input:focus {
  outline: none;
  border-color: #102372;
  box-shadow: 0 0 0 2px #10237233;
}
.animate-scale-in {
  animation: scaleIn 0.18s ease-out;
}
@keyframes scaleIn {
  from { transform: scale(0.92); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}
</style>
