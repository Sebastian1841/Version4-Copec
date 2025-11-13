<template>
  <div class="space-y-12">

    <div class="bg-white rounded-3xl shadow-xl p-8 border border-gray-200 space-y-10">
      <KpiCards :data="data" />

      <!-- ✅ Escuchamos tipo y actualizamos columnas -->
      <SearchPanel ref="searchPanel" @loaded-data="onDataLoaded" @update-columns="columns = $event"
        @tipo-changed="cambiarModo" />

      <!-- ✅ Tabla de CARGA -->
      <DataTable v-if="modo === 'carga'" :data="data" :columns="columns" @open-uploader="showUploader = true" />

      <!-- ✅ Tabla de DESCARGA -->
      <DataTableDescarga v-if="modo === 'descarga'" :data="data" :columns="columns"
        @open-manual-form="showManualForm = true" />
    </div>

    <!-- ✅ Modal para subir Excel -->
    <FileUploader v-if="showUploader" @uploaded="onFilesUploaded" @close="showUploader = false" />

    <!-- ✅ Modal para registro manual -->
    <ManualForm v-if="showManualForm" @close="showManualForm = false" @saved="recargarManual" />

  </div>
</template>

<script>
import FileUploader from '../components/DashboardUi/FileUploader.vue'
import ManualForm from '../components/DashboardUi/ManualForm.vue'
import SearchPanel from '../components/DashboardUi/SearchPanel.vue'
import KpiCards from '../components/DashboardUi/KpiCards.vue'
import DataTable from '../components/DashboardUi/DataTable.vue'
import DataTableDescarga from '../components/DashboardUi/DataTableDescarga.vue'

export default {
  name: 'Dashboard',
  components: {
    FileUploader,
    ManualForm,
    SearchPanel,
    KpiCards,
    DataTable,
    DataTableDescarga
  },

  data() {
    return {
      data: [],
      modo: 'carga', // ✅ modo inicial
      columns: [
        'Fecha', 'Hora', 'Zona', 'Patente', 'Región',
        'Comuna', 'Estación de Servicio', 'Litros', 'Precio', 'Monto', 'Odómetro', 'Proveedor'
      ],
      showUploader: false,
      showManualForm: false
    }
  },

  methods: {
    cambiarModo(nuevoModo) {
      this.modo = nuevoModo

      // ✅ Cambiar columnas cuando es DESCARGA manual
      if (nuevoModo === 'descarga') {
        this.columns = ['Fecha', 'Tipo de Descarga', 'Litros', 'Dispositivo', 'Encargado']
      }

      // ✅ Volver a columnas de carga cuando cambia de vuelta
      if (nuevoModo === 'carga') {
        this.columns = [
          'Fecha', 'Hora', 'Zona', 'Patente', 'Región',
          'Comuna', 'Estación de Servicio', 'Litros', 'Precio', 'Monto', 'Odómetro', 'Proveedor'
        ]
      }
    },

    onDataLoaded(filteredRows) {
      this.data = filteredRows
    },

    onFilesUploaded() {
      // Excel subido → buscar de nuevo lo que esté seleccionado
      this.$refs.searchPanel.buscar()
    },

    recargarManual() {
      // Después de guardar manual: recargar la misma búsqueda de descargas
      this.$refs.searchPanel.buscar()
    }
  }
}
</script>
