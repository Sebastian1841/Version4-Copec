import os
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from controllers.upload_controller import upload_file, get_data, search_by_date
from controllers.manual_controller import guardar_manual, obtener_manuales

# Cargar variables de entorno (.env)
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# CORS
CORS(app)

# Carpetas estáticas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATA_FOLDER = os.path.join(BASE_DIR, "data")

# Asegurar existencia de carpetas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# ✅ Rutas estáticas (equivalente a express.static)
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(DATA_FOLDER, filename)

# ✅ Rutas principales
@app.route('/upload', methods=['POST'])
def upload_route():
    return upload_file(request)

@app.route('/data/<filename>', methods=['GET'])
def data_route(filename):
    return get_data(filename)

@app.route('/buscar', methods=['GET'])
def buscar_route():
    return search_by_date(request)

@app.route('/descarga/manual', methods=['POST'])
def guardar_manual_route():
    return guardar_manual()

@app.route('/descarga/manual', methods=['GET'])
def obtener_manuales_route():
    return obtener_manuales()

# ✅ Inicio del servidor
if __name__ == '__main__':
    port = int(os.getenv("PORT", 3001))
    print(f"✅ Servidor Flask corriendo en http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
