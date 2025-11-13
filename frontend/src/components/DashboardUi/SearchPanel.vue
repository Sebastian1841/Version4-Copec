<template>
  <div class="bg-white rounded-2xl shadow-xl p-6 space-y-6 border border-[#E7E7E9]">

    <!-- Filtros -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

      <div class="flex flex-col">
        <label class="text-xs font-medium text-[#1D292F]">Desde</label>
        <input v-model="desde" type="date"
          class="border border-[#E7E7E9] text-sm p-2 rounded-md bg-[#F3F3F3] focus:ring-2 focus:ring-[#102372]" />
      </div>

      <div class="flex flex-col">
        <label class="text-xs font-medium text-[#1D292F]">Hasta</label>
        <input v-model="hasta" type="date"
          class="border border-[#E7E7E9] text-sm p-2 rounded-md bg-[#F3F3F3] focus:ring-2 focus:ring-[#102372]" />
      </div>

      <div class="flex flex-col">
        <label class="text-xs font-medium text-[#1D292F]">Tipo</label>
        <select v-model="tipo" @change="cambiarTipo"
          class="border border-[#E7E7E9] bg-[#F3F3F3] text-sm p-2 rounded-md focus:ring-2 focus:ring-[#102372]">
          <option value="carga">Carga (Excel)</option>
          <option value="descarga">Descarga (Manual)</option>
        </select>
      </div>

      <div class="flex items-end">
        <button @click="buscar"
          class="w-full text-sm font-semibold bg-[#102372] hover:bg-[#FF6600] text-white px-4 py-2 rounded-md shadow">
          Buscar
        </button>
      </div>
    </div>

    <!-- ✅ ETIQUETAS PARA AMBOS TIPOS -->
    <div class="space-y-2">
      <label class="block text-sm font-semibold text-[#1D292F]">Campos a mostrar:</label>

      <div class="flex flex-wrap gap-2">
        <button v-for="col in columnasBase" :key="col" @click="toggleCol(col)"
          class="text-xs px-3 py-1 rounded-full border transition shadow-sm" :class="columnasVisibles.includes(col)
            ? 'bg-[#6EC1E4]/20 text-[#102372] border-[#6EC1E4]'
            : 'bg-[#E7E7E9] text-[#54595F] border-[#D0D0D0] hover:bg-[#DADADA]'">
          {{ col }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center text-sm text-[#102372] py-3">
      Cargando datos...
    </div>

  </div>
</template>

<script>
const API_URL = import.meta.env.VITE_API || "http://localhost:3001";

export default {
  name: 'SearchPanel',
  emits: ['loaded-data', 'update-columns', 'tipo-changed'],

  data() {
    return {
      data: [],
      loading: false,
      desde: '',
      hasta: '',
      tipo: 'carga',

      columnasCarga: [
        'Fecha', 'Hora', 'Zona', 'Patente', 'Región',
        'Comuna', 'Estación de Servicio', 'Litros', 'Precio', 'Monto', 'Odómetro', 'Proveedor'
      ],

      columnasDescarga: [
        'Fecha', 'Tipo de Descarga', 'Litros', 'Dispositivo', 'Encargado'
      ],

      columnasVisibles: []
    };
  },

  mounted() {
    this.columnasVisibles = [...this.columnasCarga];
    this.$emit('update-columns', [...this.columnasVisibles]);
  },

  computed: {
    columnasBase() {
      return this.tipo === 'carga'
        ? this.columnasCarga
        : this.columnasDescarga;
    }
  },

  methods: {
    cambiarTipo() {
      this.data = [];
      this.desde = '';
      this.hasta = '';

      this.columnasVisibles = this.tipo === 'carga'
        ? [...this.columnasCarga]
        : [...this.columnasDescarga];

      this.$emit('tipo-changed', this.tipo);
      this.$emit('update-columns', [...this.columnasVisibles]);
      this.$emit('loaded-data', []);
    },

    toggleCol(col) {
      if (this.columnasVisibles.includes(col)) {
        this.columnasVisibles = this.columnasVisibles.filter(c => c !== col);
      } else {
        const base = this.columnasBase;
        this.columnasVisibles = base.filter(c => [...this.columnasVisibles, col].includes(c));
      }

      this.$emit('update-columns', [...this.columnasVisibles]);
    },

    async buscar() {
      // Evita ejecutar búsqueda automática sin fechas
      if (!this.desde || !this.hasta) {
        console.warn("⏭️ Buscar cancelado: faltan fechas");
        return;
      }

      this.loading = true;

      try {
        let url = this.tipo === 'carga'
          ? `${API_URL}/buscar?desde=${this.desde}&hasta=${this.hasta}`
          : `${API_URL}/descarga/manual?desde=${this.desde}&hasta=${this.hasta}`;

        const res = await fetch(url);
        const arr = await res.json();
        if (!Array.isArray(arr)) return;

        this.$emit('tipo-changed', this.tipo);

        if (this.tipo === 'carga') {
          this.data = arr.map(i => ({
            Fecha: i['Fecha'] || i['Fecha Transacción'] || '',
            Hora: i['Hora'] || i['Hora Transacción'] || '',
            Zona: i['Zona'] || i['Departamento'] || '',
            Patente: i['Patente'] || '',
            Región: i['Región'] || '',
            Comuna: i['Comuna'] || '',
            'Estación de Servicio': i['Estación de Servicio'] || i['Estación'] || '',
            Litros: Number(i['Litros']) || Number(i['Volumen']) || 0,
            Precio: Number(i['Precio']) || 0,
            Monto: Number(i['Monto']) || 0,
            Odómetro: i['Odómetro (Kms.)'] || i['Odometro'] || '',
            Proveedor: i['Proveedor'] || i['proveedor'] || ''
          }));
        } else {
          this.data = arr.map(i => ({
            Fecha: i.Fecha || '',
            'Tipo de Descarga': i.TipoDescarga || '',
            Litros: i.Litros || 0,
            Dispositivo: i.Dispositivo || '',
            Encargado: i.Encargado || ''
          }));
        }

        this.$emit('loaded-data', this.data);
      } finally {
        this.loading = false;
      }
    }

  }
};
</script>
