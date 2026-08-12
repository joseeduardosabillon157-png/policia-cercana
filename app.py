import json
import math
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend (HTML)

def haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia en kilómetros entre dos coordenadas."""
    R = 6371.0  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/estaciones', methods=['GET'])
def obtener_estaciones():
    try:
        user_lat = float(request.args.get('lat'))
        user_lon = float(request.args.get('lon'))
        limite = int(request.args.get('limite', 3))
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros 'lat' y 'lon' son requeridos y deben ser números."}), 400

    with open('estaciones.json', 'r', encoding='utf-8') as f:
        estaciones = json.load(f)

    # Calcular distancia para cada estación
    for est in estaciones:
        est['distancia_km'] = round(haversine(user_lat, user_lon, est['lat'], est['lon']), 2)

    # Ordenar por distancia y limitar
    estaciones_ordenadas = sorted(estaciones, key=lambda x: x['distancia_km'])[:limite]

    return jsonify(estaciones_ordenadas)

if __name__ == '__main__':
    app.run(debug=True, port=5000)