from flask import Flask, jsonify, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # Permite que la web de Netlify consulte la API sin bloqueos

# Estado global en memoria
timbre_pulsado = False
ultimo_evento = 0

@app.route('/trigger', methods=['POST'])
def trigger():
    """El ESP32 llama a esta ruta para avisar que llamaron a la puerta"""
    global timbre_pulsado, ultimo_evento
    timbre_pulsado = True
    ultimo_evento = time.time()
    return jsonify({"status": "ok", "message": "Alarma disparada"}), 200

@app.route('/status', methods=['GET'])
def get_status():
    """La página web consulta esta ruta cada 2 segundos"""
    global timbre_pulsado
    estado_actual = timbre_pulsado
    # Una vez leído, se reinicia el estado
    if timbre_pulsado:
        timbre_pulsado = False
    return jsonify({"timbre": estado_actual, "timestamp": ultimo_evento}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)