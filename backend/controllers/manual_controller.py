import os
import json
from flask import request, jsonify
from datetime import datetime

# Ruta a descargas manuales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(os.path.dirname(BASE_DIR), "data")
MANUAL_PATH = os.path.join(DATA_FOLDER, "descargas_manual.json")

# ✅ Asegura que exista descargas_manual.json
def cargar_db():
    if not os.path.exists(MANUAL_PATH):
        with open(MANUAL_PATH, "w", encoding="utf8") as f:
            f.write("[]")
    with open(MANUAL_PATH, "r", encoding="utf8") as f:
        return json.load(f)

# ✅ POST /descarga/manual
def guardar_manual():
    body = request.get_json()

    fecha = body.get("fecha")
    litros = body.get("litros")
    tipo_descarga = body.get("tipo_descarga", "")
    encargado = body.get("encargado", "")
    dispositivo = body.get("dispositivo", "")

    if not fecha or litros is None:
        return jsonify({"error": "Fecha y Litros son obligatorios"}), 400

    db = cargar_db()

    nuevo = {
        "id": int(__import__("time").time() * 1000),
        "origen": "MANUAL",
        "Fecha": fecha,
        "Litros": float(litros),
        "TipoDescarga": tipo_descarga,
        "Encargado": encargado,
        "Dispositivo": dispositivo
    }

    db.append(nuevo)

    with open(MANUAL_PATH, "w", encoding="utf8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    print("✅ Registro manual guardado en descargas_manual.json")
    return jsonify({"message": "Registro guardado", "registro": nuevo}), 200


# ✅ GET /descarga/manual?desde=&hasta=
def obtener_manuales():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")

    if not os.path.exists(MANUAL_PATH):
        return jsonify([])

    with open(MANUAL_PATH, "r", encoding="utf8") as f:
        registros = json.load(f)

    # Si no se filtró → devolver todos
    if not desde or not hasta:
        return jsonify(registros)

    d0 = datetime.strptime(desde, "%Y-%m-%d")
    d1 = datetime.strptime(hasta, "%Y-%m-%d")

    filtrados = []
    for i in registros:
        f_str = i.get("Fecha", "")
        if not f_str:
            continue

        try:
            # ✅ Acepta ambos formatos: dd-mm-yyyy o yyyy-mm-dd
            try:
                f = datetime.strptime(f_str, "%d-%m-%Y")
            except ValueError:
                f = datetime.strptime(f_str, "%Y-%m-%d")

            if d0 <= f <= d1:
                filtrados.append(i)
        except Exception as e:
            print("❌ Error procesando registro:", e)
            continue

    print(f"📦 Filtrados ({len(filtrados)}):", filtrados)
    return jsonify(filtrados)