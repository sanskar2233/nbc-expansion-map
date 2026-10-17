import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="NBC Expansion Engine", layout="wide")

st.title("Nothing Before Coffee (NBC) - Expansion")
st.subheader("Business Development Next 1000 Stores Catchment Strategy")
st.write("Click on any store pin or catchment circle to inspect the location.")

# Center map on Gurugram/Delhi NCR region using OpenStreetMap (No API Key Required)
m = folium.Map(location=[28.4595, 77.0266], zoom_start=11, tiles="OpenStreetMap")

# Read CSV with encoding and bad lines handling
try:
    df = pd.read_csv("Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv", encoding="latin1", on_bad_lines='skip')
    nbc_stores = df.to_dict('records')
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
    nbc_stores = []

# Competitor Cafes and Brands
competitors = [
    {"name": "Starbucks Store", "lat": 28.5355, "lon": 77.3910, "brand": "Starbucks"},
    {"name": "Blue Tokai Store", "lat": 28.4595, "lon": 77.0266, "brand": "Blue Tokai"},
    {"name": "Third Wave Coffee", "lat": 28.5355, "lon": 77.3910, "brand": "Third Wave"},
    {"name": "Zudio Outlet", "lat": 28.4595, "lon": 77.0266, "brand": "Zudio"},
    {"name": "Lenskart Outlet", "lat": 28.5355, "lon": 77.0390, "brand": "Lenskart"},
    {"name": "McDonald's Outlet", "lat": 28.5355, "lon": 77.1910, "brand": "McDonald's"},
    {"name": "Domino's Pizza", "lat": 28.5355, "lon": 77.2090, "brand": "Dominos"},
    {"name": "Costa Coffee", "lat": 28.4595, "lon": 77.0860, "brand": "Costa Coffee"},
    {"name": "Cafe Coffee Day", "lat": 28.5355, "lon": 77.2340, "brand": "Cafe Coffee Day"},
    {"name": "V-Mart Outlet", "lat": 28.4712, "lon": 77.0289, "brand": "V-Mart"},
    {"name": "Love Over Coffee Outlet", "lat": 28.5218, "lon": 77.1110, "brand": "Love Over Coffee"}
]

# 1. Plot Outlets with Blue Catchment (1 km radius)
for store in nbc_stores:
    lat = store.get("Latitude") or store.get("lat") or store.get("LATITUDE")
    lon = store.get("Longitude") or store.get("lon") or store.get("LONGITUDE")
    name = store.get("Store_Name") or store.get("Outlet_Name") or store.get("name") or "NBC Store"

    if pd.notna(lat) and pd.notna(lon):
        try:
            lat = float(lat)
            lon = float(lon)
            folium.Circle(
                location=[lat, lon],
                radius=1000,
                color="blue",
                fill=True,
                fill_opacity=0.15,
                popup=f'Catchment: {name}'
            ).add_to(m)

            folium.Marker(
                location=[lat, lon],
                popup=f'<b>NBC Store: {name}</b>',
                tooltip=name,
                icon=folium.Icon(color='darkred', icon='coffee', prefix='fa')
            ).add_to(m)
        except (ValueError, TypeError):
            continue

# 2. Plot Competitors & Brands
for comp in competitors:
    if comp["brand"] == "V-Mart":
        folium.Marker(
            location=[comp['lat'], comp['lon']],
            popup=f'<b>{comp["brand"]}: {comp["name"]}</b>',
            tooltip=comp['name'],
            icon=folium.Icon(color='green', icon='shopping-bag', prefix='fa')
        ).add_to(m)
    elif comp["brand"] == "Love Over Coffee":
        folium.Marker(
            location=[comp['lat'], comp['lon']],
            popup=f'<b>{comp["brand"]}: {comp["name"]}</b>',
            tooltip=comp['name'],
            icon=folium.Icon(color='purple', icon='heart', prefix='fa')
        ).add_to(m)
    else:
        folium.Marker(
            location=[comp['lat'], comp['lon']],
            popup=f'<b>{comp["brand"]}: {comp["name"]}</b>',
            tooltip=comp['name'],
            icon=folium.Icon(color='blue', icon='cutlery', prefix='fa')
        ).add_to(m)

st_folium(m, width=1100, height=600)
