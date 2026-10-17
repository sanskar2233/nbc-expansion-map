import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="NBC Expansion Engine", layout="wide")

st.title("Nothing Before Coffee – Expansion Map")
st.write("Click on any store pin or catchment circle to inspect the location.")

# Center map on Jaipur/Delhi
m = folium.Map(location=[28.6139, 77.2090], zoom_start=11)

# Read CSV with encoding and bad lines handling
try:
    df = pd.read_csv(
        "Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv",
        encoding="latin1",
        on_bad_lines="skip"
    )
    nbc_stores = df.to_dict('records')
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    nbc_stores = []

# Competitor Cafes
competitors = [
    {"name": "Competitor Cafe A", "lat": 28.5355, "lon": 77.3910},
    {"name": "Competitor Cafe B", "lat": 28.4595, "lon": 77.0266},
]

# 1. Plot Outlets with Catchment
for store in nbc_stores:
    lat = store.get("Latitude") or store.get("lat") or store.get("LATITUDE")
    lon = store.get("Longitude") or store.get("lon") or store.get("LONGITUDE")
    name = store.get("Store_Name") or store.get("Outlet_Name") or store.get("name") or "Store"

    if pd.notna(lat) and pd.notna(lon):
        try:
            lat = float(lat)
            lon = float(lon)
            
            folium.Circle(
                location=[lat, lon],
                radius=1000,
                color="#8F4E37",
                fill=True,
                fill_opacity=0.15,
                popup=f'Catchment: {name}'
            ).add_to(m)

            folium.Marker(
                location=[lat, lon],
                popup=f'<b>{name}</b>',
                tooltip=str(name),
                icon=folium.Icon(color='darkred', icon='coffee', prefix='fa')
            ).add_to(m)
        except (ValueError, TypeError):
            continue

# 2. Plot Sample Competitors
for comp in competitors:
    folium.Marker(
        location=[comp['lat'], comp['lon']],
        popup=f'<b>{comp["name"]}</b>',
        tooltip=comp['name'],
        icon=folium.Icon(color='blue', icon='cutlery', prefix='fa')
    ).add_to(m)

st_folium(m, width=1100, height=600)
