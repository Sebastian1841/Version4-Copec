# Backend - API Flask para cargas y descargas

Servicio Flask que procesa archivos Excel de combustibles, normaliza los datos y los expone como una API REST. Tambien permite registrar descargas manuales y consultarlas por rango de fechas.

## Stack y dependencias
- Python 3.10+ recomendado.
- Flask + Flask-CORS (`app.py`) para la API.
- python-dotenv para variables de entorno.
- openpyxl para leer archivos `.xlsx`.
- Persistencia en archivos JSON (carpeta `data/`).

Instalacion:
```
cd backend
python -m venv .venv          # opcional pero recomendado
.venv\Scripts\activate        # en PowerShell
pip install -r requirements.txt
```

## Variables de entorno
Archivo `.env` (ya incluido):

| Variable | Uso                       | Valor por defecto |
|----------|---------------------------|-------------------|
| `PORT`   | Puerto donde corre Flask  | `3001`            |

`app.py` lee este valor y no activa el reloader.

## Estructura destacada
```
backend/
 +- app.py                   # registro de rutas y configuracion base
 +- controllers/
    +- upload_controller.py # logica de carga/normalizacion de Excel
    +- manual_controller.py # CRUD basico para descargas manuales
 +- services/
    +- excel_processor.py   # lectura generica de hojas Excel
 +- data/                    # JSON persistentes (admindb, descargas)
 +- uploads/                 # archivos originales subidos
 +- utils/comunasRegionesChile.json
```

## Flujo de procesamiento
1. `POST /upload` recibe uno o mas `.xlsx`, valida la extension y guarda una copia en `uploads/`.
2. Cada archivo se convierte a objetos Python con `services/excel_processor.py`, detectando cabeceras y estandarizando nombres de columnas.
3. `upload_controller.py` normaliza campos (fechas/horas Excel, region segun comuna, precio por litro, patente sin guiones), etiqueta el origen (Shell/Copec) y deduplica usando una firma JSON.
4. Los registros se almacenan en `data/admindb.json`, el cual persiste entre reinicios (el `docker-compose` monta esta carpeta como volumen).

## Endpoints principales
| Metodo | Ruta               | Descripcion |
|--------|--------------------|-------------|
| POST   | `/upload`          | Sube uno o varios Excel (`form-data` con campo `files`). Devuelve total de registros guardados. |
| GET    | `/buscar`          | Requiere `desde` y `hasta` (formato `YYYY-MM-DD`). Filtra por `Fecha` o `Fecha Transaccion`. |
| GET    | `/data/<filename>` | Entrega los datos crudos guardados en `data/admindb.json` (el parametro se ignora por ahora). |
| POST   | `/descarga/manual` | Guarda un registro manual (fecha, litros, tipo, encargado, dispositivo). |
| GET    | `/descarga/manual` | Lista descargas manuales, opcionalmente filtradas por fecha. |

## Datos persistentes
- `data/admindb.json`: registros provenientes de Excel.
- `data/descargas_manual.json`: registros creados con el formulario manual.
- `uploads/`: respaldo de los archivos origen. Se crean automaticamente si no existen.

## Ejecucion local
```
set FLASK_ENV=development   # opcional
python app.py               # escucha en http://localhost:3001
```

Con Docker (junto al frontend):
```
docker compose up --build backend
```
- Expone el puerto `3001`.
- Monta `backend/uploads` y `backend/data` como volumenes para no perder archivos.

## Notas
- El servicio depende de `comunasRegionesChile.json` para inferir la region a partir de la comuna.
- Si se corrompen los JSON de `data/`, basta con borrarlos (se regeneran vacios), pero respalda la informacion si la necesitas.
