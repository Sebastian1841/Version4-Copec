<template>
  <div class="p-4 bg-white rounded-xl shadow border border-[#E7E7E9]">

    <!-- BUSCADOR + CONTROLES -->
    <div class="flex flex-col sm:flex-row justify-between items-center mb-3 gap-3">

      <div class="flex w-full sm:w-2/3 gap-2">
        <div class="flex flex-1 border border-[#E7E7E9] rounded-lg overflow-hidden bg-white shadow-sm">
          <div class="flex items-center justify-center px-3 bg-[#E7E7E9] text-[#1D292F]">
            <SvgIcon name="search" class="w-4 h-4" />
          </div>
          <input v-model="searchTerm" placeholder="Buscar..."
            class="flex-1 p-2 text-sm text-[#1D292F] placeholder-gray-400 focus:outline-none" />
          <button v-if="searchTerm" @click="searchTerm = ''"
            class="px-3 bg-[#FF6600] hover:bg-[#d95400] text-white text-xs transition">
            Limpiar
          </button>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <button @click="$emit('open-uploader')"
          class="flex items-center gap-2 bg-[#102372] hover:bg-[#FF6600] text-white text-xs px-4 py-2 rounded-lg shadow transition">
          <SvgIcon name="upload" class="w-4 h-4" />
          Subir Excel
        </button>

        <div class="flex items-center gap-2 text-xs text-[#54595F]">
          <span class="font-semibold">Filas:</span>
          <select v-model.number="rowsPerPage" class="border border-[#E7E7E9] bg-white rounded px-2 py-1 text-xs
                   focus:ring-1 focus:ring-[#6EC1E4] focus:border-[#6EC1E4]">
            <option v-for="n in rowsPerPageOptions" :key="n" :value="n">{{ n }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- CONTADOR -->
    <div class="flex justify-end mb-2">
      <div class="text-xs font-semibold text-[#102372] bg-[#6EC1E4]/20 p-1.5 rounded-md">
        Mostrando <span class="font-bold">{{ paginatedData.length }}</span> de
        <span class="font-bold">{{ filteredData.length }}</span> registros
      </div>
    </div>

    <!-- TABLA DESKTOP -->
    <div class="hidden sm:block overflow-x-auto max-h-[50vh] border border-[#E7E7E9] rounded-lg shadow-sm">
      <table class="min-w-full text-sm">
        <thead class="bg-[#172F3F] text-white uppercase text-xs sticky top-0 z-20">
          <tr>
            <th v-for="col in columns" :key="col"
              class="px-4 py-3 text-left cursor-pointer hover:bg-[#1D292F] transition bg-[#172F3F]"
              @click="toggleSort(col)">
              <div class="flex items-center gap-1">
                {{ col }}
                <span v-if="sortBy === col">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span>
              </div>
            </th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(row, idx) in paginatedData" :key="idx"
            class="border-b border-[#E7E7E9] hover:bg-[#E7E7E9] transition">

            <td v-for="col in columns" :key="col + idx"
              class="px-4 py-2 whitespace-nowrap text-[#1D292F] cursor-pointer"
              @dblclick="isOdometro(col) && startEditing(idx, col)">

              <!-- ✅ INPUT EDITABLE -->
              <template v-if="editingField && editingField.rowIndex === idx && editingField.col === col">
                <input v-model="tempValue" @input="validateNumeric" @keyup.enter="finishEdit"
                  class="border px-1 py-0.5 rounded w-24 text-xs" autofocus />
              </template>

              <!-- ✅ LECTURA -->
              <template v-else>
                {{ row[col] }}
              </template>

            </td>
          </tr>

          <tr v-if="paginatedData.length === 0">
            <td :colspan="columns.length" class="text-center py-6 text-[#54595F]">
              No hay registros para mostrar
            </td>
          </tr>

        </tbody>
      </table>
    </div>

    <!-- MOBIL CARDS -->
    <div class="sm:hidden max-h-[50vh] overflow-y-auto space-y-4 p-1">
      <div v-for="(row, idx) in paginatedData" :key="idx"
        class="border border-[#E7E7E9] rounded-2xl p-4 shadow-sm bg-white hover:shadow-lg hover:-translate-y-1 transition-all">

        <div class="flex justify-between items-center mb-3">
          <div class="text-xs font-bold text-[#102372]">
            Registro #{{ (currentPage - 1) * rowsPerPage + idx + 1 }}
          </div>
          <span class="px-2 py-0.5 text-[10px] rounded-full bg-[#6EC1E4]/25 text-[#102372] font-semibold">
            {{ columns.length }} campos
          </span>
        </div>

        <div class="space-y-2">
          <div v-for="col in columns" :key="col"
            class="flex justify-between text-[12px] py-1 border-b border-[#E7E7E9] last:border-b-0 cursor-pointer"
            @dblclick="isOdometro(col) && startEditing(idx, col)">
            <span class="text-[#54595F] font-medium">{{ col }}:</span>

            <span class="text-[#1D292F] font-semibold text-right ml-2">

              <template v-if="editingField && editingField.rowIndex === idx && editingField.col === col">
                <input v-model="tempValue" @input="validateNumeric" @keyup.enter="finishEdit"
                  class="border px-1 py-0.5 rounded w-20 text-[11px]" autofocus />
              </template>

              <template v-else>
                {{ row[col] || '-' }}
              </template>

            </span>
          </div>
        </div>

      </div>

      <p v-if="paginatedData.length === 0" class="text-center text-[#54595F] text-xs py-4">
        No hay registros para mostrar
      </p>
    </div>

    <!-- PAGINACIÓN -->
    <div
      class="flex justify-between items-center mt-3 text-xs bg-white p-3 rounded-lg shadow-inner border border-[#E7E7E9]">

      <button @click="prevPage" :disabled="currentPage === 1" class="px-2 py-1 border border-[#E7E7E9] rounded bg-[#F3F3F3] disabled:opacity-50
               hover:bg-[#102372] hover:text-white transition">
        <SvgIcon name="chevron-left" class="w-3 h-3" />
      </button>

      <span class="text-[#1D292F]">
        Pág. <span class="text-[#102372] font-bold">{{ currentPage }}</span> / {{ totalPages }}
      </span>

      <button @click="nextPage" :disabled="currentPage === totalPages" class="px-2 py-1 border border-[#E7E7E9] rounded bg-[#F3F3F3] disabled:opacity-50
               hover:bg-[#102372] hover:text-white transition">
        <SvgIcon name="chevron-right" class="w-3 h-3" />
      </button>

    </div>

    <!-- ✅ MODAL CONFIRMACIÓN -->
    <transition name="fade-zoom">
      <div v-if="showConfirmModal"
        class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-xl shadow-xl text-center space-y-4 w-72 animate-scale-in">

          <h3 class="text-sm font-semibold text-[#102372]">
            ¿Guardar cambio del odómetro?
          </h3>

          <p class="text-xs text-[#54595F]">
            Valor nuevo: <strong class="text-[#FF6600]">{{ tempValue }}</strong>
          </p>

          <div class="flex justify-center gap-3 mt-3">
            <button @click="cancelEdit" class="px-3 py-1 text-xs bg-gray-300 rounded hover:bg-gray-400">
              Cancelar
            </button>

            <button @click="confirmSave" class="px-3 py-1 text-xs bg-[#FF6600] text-white rounded hover:bg-[#d95400]">
              Guardar
            </button>
          </div>

        </div>
      </div>
    </transition>

  </div>
</template>


<script>
import SvgIcon from "@/components/icons/SvgIcon.vue";

export default {
  name: "DataTable",
  components: { SvgIcon },

  props: {
    data: { type: Array, default: () => [] },
    showUploader: false,
    columns: { type: Array, default: () => [] }
  },

  data() {
    return {
      searchTerm: "",
      sortBy: null,
      sortOrder: "asc",
      rowsPerPage: 5,
      currentPage: 1,
      rowsPerPageOptions: [5, 10, 25, 50, 100],

      editingField: null,
      tempValue: "",
      showConfirmModal: false,
    };
  },

  computed: {
    filteredData() {
      if (!this.searchTerm) return this.data;

      const term = this.searchTerm.toLowerCase();
      return this.data.filter(row =>
        this.columns.some(col =>
          String(row[col]).toLowerCase().includes(term)
        )
      );
    },

    sortedData() {
      if (!this.sortBy) return this.filteredData;
      return [...this.filteredData].sort((a, b) => {
        const va = a[this.sortBy] ?? "";
        const vb = b[this.sortBy] ?? "";
        return this.sortOrder === "asc"
          ? String(va).localeCompare(String(vb))
          : String(vb).localeCompare(String(va));
      });
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.rowsPerPage;
      return this.sortedData.slice(start, start + this.rowsPerPage);
    },

    totalPages() {
      return Math.max(1, Math.ceil(this.filteredData.length / this.rowsPerPage));
    }
  },

  methods: {
    toggleSort(col) {
      if (this.sortBy === col) {
        this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc";
      } else {
        this.sortBy = col;
        this.sortOrder = "asc";
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },

    normalizar(text) {
      return text
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, ""); // quita acentos
    },

    isOdometro(col) {
      return this.normalizar(col) === "odometro";
    },

    startEditing(rowIndex, col) {
      this.editingField = { rowIndex, col };
      this.tempValue = this.paginatedData[rowIndex][col];
    },

    validateNumeric() {
      this.tempValue = this.tempValue.replace(/[^0-9.]/g, "");
    },

    finishEdit() {
      this.showConfirmModal = true;
    },

    cancelEdit() {
      this.editingField = null;
      this.tempValue = "";
      this.showConfirmModal = false;
    },

    confirmSave() {
      const { rowIndex, col } = this.editingField;

      this.$emit("update-odometro", {
        row: this.paginatedData[rowIndex],
        field: col,
        newValue: this.tempValue
      });

      this.paginatedData[rowIndex][col] = this.tempValue;

      this.showConfirmModal = false;
      this.editingField = null;
    },
  }
};
</script>


<style>
.fade-zoom-enter-active,
.fade-zoom-leave-active {
  transition: all 0.2s ease;
}

.fade-zoom-enter-from,
.fade-zoom-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.animate-scale-in {
  animation: scaleIn 0.18s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0.85);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
