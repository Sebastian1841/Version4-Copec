import os
import json
import time
from datetime import datetime, date, time as timeobj
from flask import jsonify
from werkzeug.utils import secure_filename
from services.excel_processor import process_excel

# === Configuración base ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(os.path.dirname(BASE_DIR), "uploads")
DATA_FOLDER = os.path.join(os.path.dirname(BASE_DIR), "data")
COMUNAS_PATH = os.path.join(BASE_DIR, "..", "utils", "comunasRegionesChile.json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# === Cargar comunas → regiones ===
try:
    with open(COMUNAS_PATH, "r", encoding="utf8") as f:
        comunas_regiones = json.load(f)
except Exception as e:
    print("❌ Error cargando comunasRegionesChile.json:", e)
    comunas_regiones = []


# === Utilidades (mismo comportamiento que en JS) ===
def excel_date_to_js(serial_num: float) -> str:
    try:
        excel_epoch = 25569  # 1899-12-30 a 1970-01-01
        seconds = (float(serial_num) - excel_epoch) * 86400
        d = datetime.utcfromtimestamp(seconds)
        return d.strftime("%d-%m-%Y")
    except Exception:
        return ""


def excel_time_to_js(serial_num: float) -> str:
    try:
        total_seconds = round(float(serial_num) * 24 * 3600)
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
    except Exception:
        return ""


def separar_fecha_hora(valor: str):
    if not valor or not isinstance(valor, str):
        return "", ""
    limpio = valor.replace("/", "-")
    partes = limpio.split(" ")
    fecha = partes[0] if partes else ""
    hora = partes[1] if len(partes) > 1 else ""
    if len(hora) == 5:
        hora += ":00"
    return fecha, hora


def normalizar_keys(obj):
    keys_map = {
        'odómetro (kms.)': 'Odómetro (Kms.)',
        'tipo de tarjeta': 'Tipo de Tarjeta',
        'producto': 'Producto',
        'tipo de vehículo': 'Tipo de Vehículo',
        'tarjeta': 'Tarjeta',
        'fecha transacción': 'Fecha Transacción',
        'hora transacción': 'Hora Transacción',
        'rendimiento': 'Rendimiento',
        'guía despacho': 'Guía Despacho'
    }
    nuevo = {}
    for k, v in obj.items():
        nk = keys_map.get(k.lower(), k)
        nuevo[nk] = v
    return nuevo


def obtener_region_desde_comuna(comuna):
    if not comuna:
        return ""
    nombre = str(comuna).lower().strip()
    match = next((c for c in comunas_regiones if c.get("comuna", "").lower() == nombre), None)
    return match["region"] if match else ""


def canonical_string(obj):
    sorted_obj = {k: obj[k] for k in sorted(obj.keys())}
    return json.dumps(sorted_obj, ensure_ascii=False)


def sanitize_value(v):
    if isinstance(v, datetime):
        return v.strftime("%d-%m-%Y %H:%M:%S")
    if isinstance(v, date):
        return v.strftime("%d-%m-%Y")
    if isinstance(v, timeobj):
        return v.strftime("%H:%M:%S")
    if isinstance(v, list):
        return [sanitize_value(x) for x in v]
    if isinstance(v, dict):
        return {k: sanitize_value(x) for k, x in v.items()}
    return v


# === POST /upload ===
def upload_file(request):
    if "files" not in request.files:
        return jsonify({"error": "No se subieron archivos."}), 400

    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No se subieron archivos."}), 400

    db_path = os.path.join(DATA_FOLDER, "admindb.json")
    database = json.load(open(db_path, "r", encoding="utf8")) if os.path.exists(db_path) else []
    existing_set = set(canonical_string(r) for r in database)

    try:
        for f in files:
            filename = secure_filename(f.filename)
            if not filename.endswith(".xlsx"):
                return jsonify({"error": "Solo archivos .xlsx permitidos"}), 400

            save_path = os.path.join(UPLOAD_FOLDER, f"{int(time.time())}-{filename}")
            f.save(save_path)

            rows = process_excel(save_path)

            nombre_archivo = filename.lower()
            is_movimiento = ("shell" in nombre_archivo) or ("movimiento" in nombre_archivo)
            origen = "TSE_Movimiento" if is_movimiento else "Consumos_por_Patente"
            proveedor = "SHELL" if is_movimiento else "COPEC"

            transformed = []
            for item in rows:
                clean = dict(item)

                # Patente sin guiones
                if "Patente" in clean and clean["Patente"]:
                    clean["Patente"] = str(clean["Patente"]).replace("-", "")

                if is_movimiento:
                    fval = clean.get("Fecha")
                    if isinstance(fval, (int, float)):
                        clean["Fecha"] = excel_date_to_js(fval)
                        clean["Hora Transacción"] = excel_time_to_js(fval % 1)
                    elif isinstance(fval, datetime):
                        clean["Fecha"] = fval.strftime("%d-%m-%Y")
                        clean["Hora Transacción"] = fval.strftime("%H:%M:%S")
                    elif isinstance(fval, str):
                        if " " in fval:
                            fecha, hora = separar_fecha_hora(fval)
                            clean["Fecha"], clean["Hora Transacción"] = fecha, hora
                        else:
                            clean["Fecha"] = fval.replace("/", "-")
                            clean["Hora Transacción"] = clean.get("Hora") or clean.get("Hora Movimiento") or "00:00:00"

                else:
                    ft = clean.get("Fecha Transacción")
                    ht = clean.get("Hora Transacción")
                    if isinstance(ft, (int, float)):
                        clean["Fecha Transacción"] = excel_date_to_js(ft)
                    elif isinstance(ft, datetime):
                        clean["Fecha Transacción"] = ft.date().strftime("%d-%m-%Y")
                    elif isinstance(ft, date):
                        clean["Fecha Transacción"] = ft.strftime("%d-%m-%Y")
                    elif isinstance(ft, str):
                        clean["Fecha Transacción"] = ft.split(" ")[0].replace("/", "-")
                    if isinstance(ht, (int, float)):
                        clean["Hora Transacción"] = excel_time_to_js(ht)
                    elif isinstance(ht, datetime):
                        clean["Hora Transacción"] = ht.strftime("%H:%M:%S")
                    elif isinstance(ht, timeobj):
                        clean["Hora Transacción"] = ht.strftime("%H:%M:%S")
                    elif isinstance(ht, str):
                        h = ht.strip()
                        if len(h) == 5:
                            h += ":00"
                        clean["Hora Transacción"] = h

                # ✅ Monto siempre positivo
                if "Monto" in clean and clean["Monto"] not in ("", None):
                    try:
                        clean["Monto"] = abs(float(clean["Monto"]))
                    except Exception:
                        pass

                # ✅ Región desde comuna
                if not clean.get("Región") and clean.get("Comuna"):
                    clean["Región"] = obtener_region_desde_comuna(clean["Comuna"])

                # ✅ Calcular precio = Monto / Litros o Volumen
                litros_val = clean.get("Litros") or clean.get("Volumen")
                try:
                    monto = float(clean.get("Monto", 0))
                    litros = float(litros_val or 0)
                    clean["Precio"] = round(monto / litros, 0) if litros > 0 else 0
                except Exception:
                    clean["Precio"] = 0

                registro = normalizar_keys({"origen": origen, "proveedor": proveedor, **clean})
                transformed.append(registro)

            # Deduplicación
            nuevos = 0
            for row in transformed:
                sig = canonical_string(row)
                if sig not in existing_set:
                    existing_set.add(sig)
                    database.append(row)
                    nuevos += 1
            print(f"✅ {filename}: {nuevos} nuevos")

        with open(db_path, "w", encoding="utf8") as f:
            json.dump(sanitize_value(database), f, indent=2, ensure_ascii=False)

        return jsonify({"message": "Datos guardados correctamente", "total_registros_db": len(database)})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# === GET /data ===
def get_data(filename):
    filepath = os.path.join(DATA_FOLDER, "admindb.json")
    if not os.path.exists(filepath):
        return jsonify({"error": "No hay datos cargados aún."}), 404
    with open(filepath, "r", encoding="utf8") as f:
        return jsonify(json.load(f))


# === GET /buscar?desde=&hasta= ===
def search_by_date(request):
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    db_path = os.path.join(DATA_FOLDER, "admindb.json")
    if not os.path.exists(db_path):
        return jsonify({"error": "Base de datos no encontrada."}), 404

    with open(db_path, "r", encoding="utf8") as f:
        all_data = json.load(f)

    try:
        d0 = datetime.strptime(desde, "%Y-%m-%d")
        d1 = datetime.strptime(hasta, "%Y-%m-%d")
        out = []
        for item in all_data:
            f = item.get("Fecha Transacción") or item.get("Fecha")
            if not f:
                continue
            dt = datetime.strptime(f, "%d-%m-%Y")
            if d0 <= dt <= d1:
                out.append(item)
        return jsonify(out)
    except Exception:
        return jsonify({"error": "Error procesando búsqueda"}), 500
