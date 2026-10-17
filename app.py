import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

st.set_page_config(page_title="NBC Expansion Engine", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E3799; margin-bottom: 5px; }
    .sub-title { font-size: 18px; color: #4A6984; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

geolocator = Nominatim(user_agent="nbc_store_locator")

def get_coordinates(address):
    try:
        time.sleep(1)
        location = geolocator.geocode(f"{address}, Delhi NCR, India", timeout=10)
        if location:
            return location.latitude, location.longitude
    except (GeocoderTimedOut, Exception):
        return None, None
    return None, None

with st.sidebar:
    st.markdown("<div class='main-title'>NBC Expansion</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Strategic Growth Map</div>", unsafe_allow_html=True)
    
    phases = [
        "Phase 1 (150 stores)", 
        "Phase 2 (250 stores)", 
        "Phase 3 (500 stores)", 
        "Phase 4 (750 stores)", 
        "Phase 5 (1000 stores)"
    ]
    selected_phases = st.multiselect("Select Expansion Phase", phases, default=phases)

st.markdown("<div class='main-title'>Nothing Before Coffee (NBC)</div>", unsafe_allow_html=True)
st.subheader("Business Development Next 1000 Stores Catchment Strategy")

m = folium.Map(location=[28.4595, 77.0266], zoom_start=11, tiles="OpenStreetMap")

try:
    df = pd.read_csv("Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv", encoding="latin1", on_bad_lines='skip')
    
    lat_col = next((c for c in df.columns if c.strip().lower() in ['latitude', 'lat']), None)
    lon_col = next((c for c in df.columns if c.strip().lower() in ['longitude', 'lon', 'long']), None)
    addr_col = next((c for c in df.columns if 'address' in c.strip().lower() or 'location' in c.strip().lower()), None)
    name_col = next((c for c in df.columns if 'name' in c.strip().lower() or 'store' in c.strip().lower() or 'outlet' in c.strip().lower()), None)

    if not lat_col or not lon_col:
        if addr_col:
            st.info("Fetching coordinates from addresses...")
            coords = df[addr_col].apply(get_coordinates)
            df['Latitude'] = [c[0] for c in coords]
            df['Longitude'] = [c[1] for c in coords]
            lat_col, lon_col = 'Latitude', 'Longitude'
            df = df.dropna(subset=[lat_col, lon_col])
    
    nbc_stores = df.to_dict('records')
except Exception as e:
    st.error(f"Error loading CSV file: {e}")
