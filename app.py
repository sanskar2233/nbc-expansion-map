import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
st.set_page_config(page_title="NBC Expansion Engine", layout="wide")

st.title("☕ Nothing Before Coffee — Expansion Map")
st.write("Click on any store pin or catchment circle to inspect the location.")

# Center map on Jaipur
m = folium.Map(location=[26.9124, 75.7873], zoom_start=12, )

# Sample NBC Outlets
df = pd.read_csv("Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv")
nbc_stores = df.to_dict('records')

# Sample Competitor Cafes
competitors = [
    {"name": "Competitor Cafe A", "lat": 26.9110, "lon": 75.7980},
    {"name": "Competitor Cafe B", "lat": 26.8540, "lon": 75.8200},
]

# 1. Plot NBC Outlets with 1km Catchments
for store in nbc_stores:
    folium.Circle(
        location=[store["lat"], store["lon"]],
        radius=1000,
        color="#6F4E37",
        fill=True,
        fill_opacity=0.15,
        popup=f"Catchment: {store['name']}"
    ).add_to(m)

    folium.Marker(
        location=[store["lat"], store["lon"]],
        popup=f"<b>{store['name']}</b>",
        tooltip="NBC Store",
        icon=folium.Icon(color="darkred", icon="coffee", prefix="fa")
    ).add_to(m)

# 2. Plot Competitors
for comp in competitors:
    folium.Marker(
        location=[comp["lat"], comp["lon"]],
        popup=f"<b>{comp['name']}</b>",
        tooltip="Competitor",
        icon=folium.Icon(color="blue", icon="cutlery", prefix="fa")
    ).add_to(m)

st_folium(m, width=1100, height=600)
