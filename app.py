import streamlit as st
import json
import math
import os

st.set_page_config(page_title="Policía Cercana", page_icon="🚓")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def cargar_estaciones():
    ruta_json = os.path.join(os.path.dirname(__file__), 'estaciones.json')
    if not os.path.exists(ruta_json):
        st.error(f"No se encontró el archivo {ruta_json}")
        return []
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)

st.title("🚓 Buscar Estaciones Policiales")
st.markdown("Introduce tus coordenadas para encontrar las unidades más cercanas.")

col1, col2 = st.columns(2)

with col1:
    user_lat = st.number_input("Tu Latitud", value=14.0818, format="%.6f")

with col2:
    user_lon = st.number_input("Tu Longitud", value=-87.1921, format="%.6f")

limite = st.slider("Número de estaciones a mostrar", min_value=1, max_value=5, value=3)

if st.button("Buscar Estaciones", type="primary"):
    estaciones = cargar_estaciones()
    
    if not estaciones:
        st.warning("No hay datos de estaciones disponibles.")
    else:
        for est in estaciones:
            est['distancia_km'] = round(haversine(user_lat, user_lon, est['lat'], est['lon']), 2)

        estaciones_ordenadas = sorted(estaciones, key=lambda x: x['distancia_km'])[:limite]

        st.subheader(f"Las {len(estaciones_ordenadas)} estaciones más cercanas:")
        
        for i, est in enumerate(estaciones_ordenadas):
            st.markdown(f"### {i+1}. {est['nombre']}")
            st.metric(label="Distancia", value=f"{est['distancia_km']} km")
            st.markdown(f"**Coordenadas:** `{est['lat']}, {est['lon']}`")
            st.markdown("---")
