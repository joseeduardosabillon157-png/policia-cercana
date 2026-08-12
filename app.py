import streamlit as st
import json
import math
import os
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="Policía Cercana - Santa Bárbara", page_icon="🚓")

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
st.markdown("Consulta las estaciones más cercanas en **Santa Bárbara** o usa tu ubicación exacta.")

# Cargar base de datos de estaciones
estaciones = cargar_estaciones()

# Información contextual rápida
st.info(f"📌 **Base de datos actual:** {len(estaciones)} estaciones registradas en la plataforma.")

# Botón para obtener ubicación automática vía GPS del dispositivo
st.subheader("1. Tu Ubicación")
loc = get_geolocation()

# Coordenadas por defecto (Centro de Santa Bárbara, Honduras)
default_lat = 14.9194
default_lon = -88.2361

# Si el usuario acepta compartir su ubicación, se actualizan las coordenadas automáticamente
if loc and 'coords' in loc:
    default_lat = loc['coords']['latitude']
    default_lon = loc['coords']['longitude']
    st.success("📍 ¡Ubicación detectada por GPS correctamente!")

col1, col2 = st.columns(2)
with col1:
    user_lat = st.number_input("Latitud", value=default_lat, format="%.6f")

with col2:
    user_lon = st.number_input("Longitud", value=default_lon, format="%.6f")

st.subheader("2. Parámetros de Búsqueda")
limite = st.slider("¿Cuántas estaciones cercanas deseas ver?", min_value=1, max_value=len(estaciones), value=3)

if st.button("Buscar Estaciones Cercanas", type="primary"):
    if not estaciones:
        st.warning("No hay datos disponibles.")
    else:
        # Calcular distancias desde las coordenadas ingresadas
        for est in estaciones:
            est['distancia_km'] = round(haversine(user_lat, user_lon, est['lat'], est['lon']), 2)

        # Ordenar de la más cercana a la más lejana
        estaciones_ordenadas = sorted(estaciones, key=lambda x: x['distancia_km'])[:limite]

        st.subheader(f"Resultados ({len(estaciones_ordenadas)} más cercanas):")
        
        for i, est in enumerate(estaciones_ordenadas):
            st.markdown(f"### {i+1}. {est['nombre']}")
            st.metric(label="Distancia aproximada", value=f"{est['distancia_km']} km")
            st.markdown(f"**Coordenadas:** `{est['lat']}, {est['lon']}`")
            st.markdown("---")
