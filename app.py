import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import os

st.set_page_config(page_title="NBC Expansion & Competitor Radar Map", layout="wide")
st.title("Nothing Before Coffee (NBC) - Expansion & Competitor Map")
st.write("ब्रांड्स, स्टोर्स और 1000 कैचमेंट लोकेशंस का लाइव विज़ुअलाइज़ेशन")

# डिफ़ॉल्ट मैप सेंटर (Delhi NCR)
m = folium.Map(location=[28.6139, 77.2090], zoom_start=10, tiles="CartoDB positron")

# ----------------- 1. BRAND COLOR & ICON CONFIGURATION -----------------
BRAND_CONFIG = {
    'Nothing Before Coffee': {'color': 'red', 'icon': 'coffee', 'prefix': 'fa'},
    'NBC': {'color': 'red', 'icon': 'coffee', 'prefix': 'fa'},
    'Blue Tokai': {'color': 'blue', 'icon': 'coffee', 'prefix': 'fa'},
    'Starbucks': {'color': 'darkgreen', 'icon': 'coffee', 'prefix': 'fa'},
    'Third Wave Coffee': {'color': 'cadetblue', 'icon': 'coffee', 'prefix': 'fa'},
    'Cafe Coffee Day': {'color': 'darkpurple', 'icon': 'coffee', 'prefix': 'fa'},
    'Costa Coffee': {'color': 'purple', 'icon': 'coffee', 'prefix': 'fa'},
    "McDonald's": {'color': 'orange', 'icon': 'cutlery', 'prefix': 'fa'},
    "Domino's": {'color': 'darkblue', 'icon': 'cutlery', 'prefix': 'fa'},
    'Zudio': {'color': 'black', 'icon': 'shopping-bag', 'prefix': 'fa'},
    'Lenskart': {'color': 'lightblue', 'icon': 'eye', 'prefix': 'fa'},
}

# ----------------- 2. NBC CATCHMENTS & LOCATIONS LOAD -----------------
nbc_file = 'NBC_1000_Location_Catchment_Single_Sheet.xlsx'
if os.path.exists(nbc_file):
    try:
        df_nbc = pd.read_excel(nbc_file, sheet_name=0)
        # Latitude और Longitude वाले रिकॉर्ड्स
        df_nbc_clean = df_nbc.dropna(subset=['Latitude', 'Longitude'])
        
        for _, row in df_nbc_clean.iterrows():
            try:
                lat = float(row['Latitude'])
                lon = float(row['Longitude'])
                site_name = str(row.get('Micro-Market / Catchment', 'NBC Proposed Site'))
                city = str(row.get('City', ''))
                phase = str(row.get('Expansion Phase', 'Phase 1'))
                
                popup_html = f"""
                <b>NBC Catchment: {site_name}</b><br>
                City: {city}<br>
                Phase: {phase}
                """
                
                # 1.5 km / 1 km Catchment Circle (रेडियस)
                folium.Circle(
                    location=[lat, lon],
                    radius=1200,
                    color="#FF4B4B",
                    fill=True,
                    fill_opacity=0.15,
                    popup=f"Catchment: {site_name}"
                ).add_to(m)
                
                # NBC Pin Marker
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"NBC: {site_name}",
                    icon=folium.Icon(color="red", icon="coffee", prefix="fa")
                ).add_to(m)
            except Exception:
                continue
    except Exception as e:
        st.warning(f"NBC Locations लोड करने में त्रुटि: {e}")

# ----------------- 3. COMPETITOR CAFE & RETAIL BRANDS LOAD -----------------
csv_file = 'Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv'
if os.path.exists(csv_file):
    try:
        df_brands = pd.read_csv(csv_file, encoding='latin1', on_bad_lines='skip')
        
        # कॉलम नाम मानकीकरण (case-insensitive check)
        lat_col = next((c for c in df_brands.columns if c.strip().lower() in ['latitude', 'lat']), None)
        lon_col = next((c for c in df_brands.columns if c.strip().lower() in ['longitude', 'lon', 'long']), None)
        
        if lat_col and lon_col:
            df_brands_valid = df_brands.dropna(subset=[lat_col, lon_col])
            for _, row in df_brands_valid.iterrows():
                try:
                    lat = float(row[lat_col])
                    lon = float(row[lon_col])
                    brand = str(row.get('Brand', 'Brand')).strip()
                    outlet = str(row.get('Store / Outlet Name', brand)).strip()
                    address = str(row.get('Address', ''))
                    
                    cfg = BRAND_CONFIG.get(brand, {'color': 'gray', 'icon': 'info-sign', 'prefix': 'glyphicon'})
                    
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(f"<b>{brand}</b><br>{outlet}<br>{address}", max_width=250),
                        tooltip=f"{brand} - {outlet}",
                        icon=folium.Icon(color=cfg['color'], icon=cfg['icon'], prefix=cfg['prefix'])
                    ).add_to(m)
                except Exception:
                    continue
    except Exception as e:
        st.warning(f"Brand CSV लोड करने में त्रुटि: {e}")

# ----------------- 4. MAP DISPLAY -----------------
st_folium(m, width="100%", height=720)
