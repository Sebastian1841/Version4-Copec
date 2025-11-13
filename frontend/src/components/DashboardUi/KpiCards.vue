<template>
  <div class="bg-white rounded-3xl shadow-xl p-6 border border-[#E7E7E9]">

    <div
      class="grid gap-4"
      style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));"
    >

      <div
        v-for="kpi in kpis"
        :key="kpi.label"
        class="flex items-center justify-between p-4 border border-[#E7E7E9] bg-[#F9FAFB] rounded-xl hover:shadow transition cursor-default">

        <div class="flex flex-col">
          <p class="text-[10px] uppercase tracking-wide font-semibold text-[#54595F]">
            {{ kpi.label }}
          </p>

          <p class="text-lg font-extrabold mt-1 text-[#1D292F]">
            {{ kpi.value }}
            <span v-if="kpi.unit" class="text-xs font-bold ml-0.5 text-[#54595F]">
              {{ kpi.unit }}
            </span>
          </p>
        </div>

        <div
          class="p-2 rounded-lg flex items-center justify-center"
          :style="{ backgroundColor: kpi.bg, color: kpi.cl }">
          <SvgIcon :name="kpi.icon" class="w-4 h-4" />
        </div>

      </div>

    </div>

  </div>
</template>

<script>
import SvgIcon from "@/components/icons/SvgIcon.vue";

export default {
  name: "KpiCards",
  components: { SvgIcon },

  props: {
    data: { type: Array, required: true }
  },

  computed: {
    kpis() {
      return [
        {
          label: "Litros",
          value: this.totalLitros.toLocaleString(),
          unit: "L",
          icon: "volumen",
          cl: "#102372",
          bg: "#6EC1E422"
        },
        {
          label: "Gasto",
          value: "$" + this.totalMonto.toLocaleString(),
          icon: "gasto",
          cl: "#1D292F",
          bg: "#61CE7022"
        },
        {
          label: "Precio/L",
          value: "$" + this.precioPromedio,
          icon: "precioL",
          cl: "#102372",
          bg: "#E7E7E9"
        },
        {
          label: "N° de Cargas",
          value: this.data.length,
          icon: "eventos",
          cl: "#FF6600",
          bg: "#FF660022"
        }
      ];
    },

    // ✅ ahora usa Litros correctamente
    totalLitros() {
      return this.data.reduce((s, r) => s + Number(r.Litros || 0), 0);
    },

    totalMonto() {
      return this.data.reduce((s, r) => s + Number(r.Monto || 0), 0);
    },

    // ✅ promedio sin decimales
    precioPromedio() {
      return this.totalLitros > 0
        ? Math.round(this.totalMonto / this.totalLitros)
        : 0;
    }
  }
};
</script>
