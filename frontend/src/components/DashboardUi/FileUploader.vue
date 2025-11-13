<template>
  <div class="fixed inset-0 bg-[#1D292FC7] backdrop-blur-sm flex items-center justify-center z-50"
    @click.self="$emit('close')">

    <transition name="fade-scale">

      <!-- ✅ PANTALLA PRINCIPAL -->
      <div v-if="!completed"
        class="bg-white rounded-3xl shadow-2xl p-8 space-y-6 w-full max-w-lg border border-[#E7E7E9] animate-fadeIn">

        <!-- HEADER -->
        <div class="flex justify-between items-center border-b pb-2">
          <h2 class="text-xl font-semibold text-[#1D292F] flex items-center gap-2">
            <SvgIcon name="upload" class="w-5 h-5 text-[#102372]" />
            Subir Archivos Excel
          </h2>

          <button @click="$emit('close')" class="text-[#54595F] hover:text-[#FF6600] text-xl font-bold">
            ✕
          </button>
        </div>

        <!-- FORMULARIO -->
        <form @submit.prevent="subirArchivos" class="space-y-4">
          <label
            class="w-full border-2 border-dashed border-[#E7E7E9] hover:border-[#102372] bg-[#F3F3F3] rounded-xl p-6 flex flex-col items-center justify-center cursor-pointer transition">
            <SvgIcon name="file" class="w-10 h-10 text-[#54595F]" />
            <p class="text-[#54595F] text-sm mt-2">Haz clic para seleccionar archivos</p>

            <input ref="fileInput" type="file" multiple accept=".xlsx" @change="handleFileChange" class="hidden" />
          </label>

          <!-- ✅ LISTA PREVIA -->
          <div v-if="selectedFiles.length" class="space-y-2 max-h-40 overflow-auto pr-1">
            <div v-for="(file, i) in selectedFiles" :key="i"
              class="flex justify-between items-center bg-[#6EC1E4]/20 text-[#102372] p-2 rounded-lg text-sm">
              <span class="font-medium truncate">{{ file.name }}</span>
              <span class="text-xs">{{ (file.size / 1024).toFixed(1) }} KB</span>
            </div>
          </div>

          <!-- ✅ BOTÓN SUBIR -->
          <button type="submit" :disabled="!selectedFiles.length || uploading"
            class="w-full bg-[#102372] hover:bg-[#FF6600] text-white font-semibold py-3 rounded-lg disabled:opacity-50 shadow-md transition">
            {{ uploading ? 'Subiendo...' : 'Subir Archivos' }}
          </button>
        </form>

        <!-- ✅ BARRA DE PROGRESO -->
        <div v-if="uploading" class="w-full mt-3">
          <div class="h-2 bg-[#E7E7E9] rounded-full overflow-hidden">
            <div :style="{ width: progreso + '%' }" class="h-full bg-[#102372] transition-all duration-150"></div>
          </div>
          <p class="text-xs text-center mt-1 text-[#54595F]">
            Subiendo {{ progreso.toFixed(0) }}%
          </p>
        </div>

        <!-- ✅ ERROR -->
        <p v-if="uploadError" class="text-red-600 font-medium text-sm text-center">
          {{ uploadError }}
        </p>
      </div>

      <!-- ✅ PANTALLA DE ÉXITO -->
      <div v-else
        class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-lg text-center border border-[#E7E7E9] space-y-4 animate-fadeIn">

        <div class="flex justify-center">
          <div class="bg-[#6EC1E4]/30 text-[#102372] rounded-full p-4 text-3xl font-bold">
            ✅
          </div>
        </div>

        <h2 class="text-xl font-bold text-[#1D292F]">¡Archivos subidos correctamente!</h2>
        <p class="text-[#54595F] text-sm">Los datos han sido procesados y agregados.</p>

        <button @click="cerrarConExito"
          class="bg-[#102372] hover:bg-[#FF6600] text-white py-2 px-6 rounded-lg shadow-sm transition">
          Cerrar
        </button>
      </div>

    </transition>
  </div>
</template>


<script>
import SvgIcon from "@/components/icons/SvgIcon.vue";

export default {
  name: "FileUploader",
  components: { SvgIcon },

  emits: ["uploaded", "close"],

  data() {
    return {
      selectedFiles: [],
      uploading: false,
      progreso: 0,
      completed: false,
      uploadError: ""
    };
  },

  methods: {
    handleFileChange(e) {
      this.selectedFiles = Array.from(e.target.files);
      this.uploadError = "";
    },

    async subirArchivos() {
      if (!this.selectedFiles.length) {
        console.log("⚠️ No hay archivos seleccionados.");
        return;
      }

      this.uploading = true;
      this.progreso = 0;
      this.uploadError = "";

      const formData = new FormData();
      this.selectedFiles.forEach(f => formData.append("files", f));

      console.log("📦 Archivos listos para enviar:", this.selectedFiles.map(f => f.name));
      console.log("🌍 URL destino:", import.meta.env.VITE_API + "/upload");

      try {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", `${import.meta.env.VITE_API}/upload`);

        xhr.upload.onprogress = (e) => {
          if (e.lengthComputable) {
            this.progreso = (e.loaded / e.total) * 100;
            console.log(`📤 Progreso: ${this.progreso.toFixed(1)}%`);
          }
        };

        xhr.onload = () => {
          console.log("📥 Respuesta del servidor:", xhr.status, xhr.responseText);

          this.uploading = false;
          if (xhr.status >= 200 && xhr.status < 300) {
            this.completed = true;
            this.$emit("uploaded");
            console.log("✅ Subida completada con éxito.");
          } else {
            this.uploadError = `❌ Error al subir los archivos (${xhr.status})`;
            console.error("❌ Respuesta con error:", xhr.responseText);
          }
        };

        xhr.onerror = (err) => {
          console.error("🚨 Error en la conexión:", err);
          this.uploading = false;
          this.uploadError = "❌ Error en la conexión";
        };

        xhr.send(formData);
        console.log("🚀 Enviando petición al backend...");

      } catch (e) {
        console.error("💥 Error inesperado:", e);
        this.uploadError = "❌ Error inesperado";
        this.uploading = false;
      }
    },

    cerrarConExito() {
      this.completed = false;
      this.selectedFiles = [];
      this.$emit("close");
    }
  }
};
</script>


<style scoped>
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all .25s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.92);
}

.animate-fadeIn {
  animation: fadeIn .25s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
