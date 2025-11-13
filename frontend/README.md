# Frontend - Panel de cargas y descargas

Aplicacion SPA en Vue 3 que centraliza la carga de archivos Excel y la consulta de descargas manuales. El dashboard muestra KPI, tablas filtrables/paginadas y modales para subir archivos o registrar informacion manual.

## Stack principal
- Vue 3 + Vite + `<script setup>` (SPA con router)
- Vue Router para la navegacion (`src/router/index.js`)
- TailwindCSS + PostCSS para los estilos globales
- Componentes propios para layout (header/sidebar) y dashboard (`src/Views/Dashboard.vue`)
- Integraciones opcionales ya instaladas: Pinia, Chart.js, vue-chartjs y vuedraggable.

## Requisitos
- Node.js 18+ (se recomienda la version LTS actual).
- npm (el proyecto incluye `package-lock.json`).

## Instalacion y scripts
```
cd frontend
npm install          # instala dependencias
npm run dev          # levanta Vite en modo desarrollo
npm run build        # genera build estatica en dist/
npm run preview      # sirve el build generado
```

## Variables de entorno
Configura un archivo `.env` (ya existe un ejemplo):

| Variable | Uso                           | Valor por defecto |
|----------|-------------------------------|-------------------|
| `VITE_API` | URL base del backend Flask | `http://localhost:3001` |

Para despliegues en Docker se usa `.env.production` con `http://backend:3001`.

## Estructura relevante
```
src/
 +- main.js                # bootstrap de la app y registro del router
 +- App.vue                # layout principal con header + sidebar
 +- Views/Dashboard.vue    # vista unica: KPI + filtros + tablas
 +- components/
    +- Layout/            # AppHeader/AppSidebar
    +- DashboardUi/       # SearchPanel, FileUploader, ManualForm, etc.
 +- router/index.js        # rutas publicas (por ahora solo dashboard)
```

## Flujo funcional (resumen)
1. `SearchPanel` dispara busquedas al backend (`/buscar` o `/descarga/manual`) segun el tipo seleccionado y expone filtros de fecha y visibilidad de columnas.
2. `KpiCards` calcula totales de litros, monto, precio promedio y numero de registros.
3. `DataTable` permite buscar, ordenar, paginar y editar puntualmente el odometro en modo "Carga". Puede abrir el modal `FileUploader` que sube archivos `.xlsx` al endpoint `/upload`.
4. `DataTableDescarga` muestra las descargas manuales y abre `ManualForm` para crear registros (POST `/descarga/manual`).
5. Los modales se comunican con el backend usando `fetch` y la URL definida en `VITE_API`.

## Consumo del backend
- `POST /upload` - carga de uno o mas archivos Excel (`form-data` con campo `files`).
- `GET /buscar?desde=YYYY-MM-DD&hasta=YYYY-MM-DD` - retorna cargas procesadas desde `admindb.json`.
- `POST /descarga/manual` - guarda una descarga cargada manualmente.
- `GET /descarga/manual?desde=YYYY-MM-DD&hasta=YYYY-MM-DD` - lista descargas manuales (o todas si no hay filtros).

## Docker / despliegue
Si usas el `docker-compose.yml` de la raiz del proyecto:

```
docker compose up --build frontend
```

- El contenedor expone el frontend en el puerto 80.
- Asegurate de que el servicio `backend` este levantado y que la variable `VITE_API` apunte a `http://backend:3001`.
