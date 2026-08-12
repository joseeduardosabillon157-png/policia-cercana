import os
import json
import math
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

def haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia en kilómetros entre dos coordenadas usando la fórmula del Haversine."""
    R = 6371.0  
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/', methods=['GET'])
def inicio():
    return jsonify({
        "mensaje": "API de Estaciones Policiales activa. Usa el endpoint /estaciones para consultar.",
        "ejemplo": "/estaciones?lat=14.0818&lon=-87.1921&limite=3"
    })

@app.route('/estaciones', methods=['GET'])
def obtener_estaciones():
    try:

        lat_raw = str(request.args.get('lat', '')).replace(',', '.')
        lon_raw = str(request.args.get('lon', '')).replace(',', '.')
        limite_raw = str(request.args.get('limite', '3'))

        user_lat = float(lat_raw)
        user_lon = float(lon_raw)
        limite = int(limite_raw)
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros 'lat' y 'lon' son requeridos y deben ser números válidos."}), 400

    ruta_json = os.path.join(os.path.dirname(__file__), 'estaciones.json')
    with open(ruta_json, 'r', encoding='utf-8') as f:
        estaciones = json.load(f)

    for est in estaciones:
        est['distancia_km'] = round(haversine(user_lat, user_lon, est['lat'], est['lon']), 2)

    estaciones_ordenadas = sorted(estaciones, key=lambda x: x['distancia_km'])[:limite]

    return jsonify(estaciones_ordenadas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
