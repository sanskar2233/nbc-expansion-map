import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="NBC Expansion Engine", layout="wide")

# Custom UI Styling
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3799; margin-bottom: 2px; }
    .sub-title { font-size: 16px; color: #4A6984; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar: Brand, Phase Filters & Layers
with st.sidebar:
    st.markdown("### **NBC Expansion Deck Controls**")
    
    phase_options = {
        "Phase 1 (Initial 150 Pipeline)": 150,
        "Phase 2 (Target 250 - Addl. 100)": 250,
        "Phase 3 (Target 500 - Addl. 250)": 500,
        "Phase 4 (Target 750 - Addl. 250)": 750,
        "Phase 5 (Target 1000 Stores)": 1000
    }
    
    selected_phase = st.selectbox(
        "Select Expansion Milestone",
        list(phase_options.keys()),
        index=0
    )
    store_limit = phase_options[selected_phase]
    
    show_competitors = st.checkbox("Show Competitor Intelligence & Revenue", value=True)
    show_catchment = st.checkbox("Show 1 KM Catchment Buffers", value=True)

# Main Title Header
st.markdown("<div class='main-title'>Nothing Before Coffee (NBC) - Expansion Strategy</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>Visualizing <b>{selected_phase}</b> | Next 1000 Stores Catchment Analysis</div>", unsafe_allow_html=True)

# Default Map Center (Delhi NCR)
m = folium.Map(location=[28.4595, 77.0266], zoom_start=11, tiles="OpenStreetMap")

# Load Data from CSV / Fallback
@st.cache_data
def load_data():
    csv_file = "Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv"
    try:
        df = pd.read_csv(csv_file, encoding="latin1", on_bad_lines='skip')
        # Clean column names
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        # Fallback dummy stores in NCR if CSV fails or not found
        fallback_data = []
        base_lat, base_lon = 28.4595, 77.0266
        for i in range(1, 151):
            fallback_data.append({
                "Store_Name": f"NBC Pipeline Store #{i}",
                "Latitude": base_lat + ((i % 15) - 7) * 0.02,
                "Longitude": base_lon + ((i // 15) - 5) * 0.02
            })
        return pd.DataFrame(fallback_data)

df_stores = load_data()

# Find coordinate columns dynamically
lat_col = next((c for c in df_stores.columns if c.lower() in ['latitude', 'lat']), None)
lon_col = next((c for c in df_stores.columns if c.lower() in ['longitude', 'lon', 'long']), None)
name_col = next((c for c in df_stores.columns if c.lower() in ['store_name', 'name', 'outlet_name', 'store name']), None)

if lat_col and lon_col:
    df_filtered = df_stores.dropna(subset=[lat_col, lon_col]).head(store_limit)
    
    for _, row in df_filtered.iterrows():
        try:
            lat = float(row[lat_col])
            lon = float(row[lon_col])
            store_title = str(row[name_col]) if name_col else f"NBC Pipeline Store"
            
            # Catchment Area Buffer
            if show_catchment:
                folium.Circle(
                    location=[lat, lon],
                    radius=1000,
                    color="#0066FF",
                    fill=True,
                    fill_color="#74B9FF",
                    fill_opacity=0.18,
                    popup=f"1 KM Catchment: {store_title}"
                ).add_to(m)
                
            # NBC Marker
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(f"<b>NBC Expansion Site:</b><br>{store_title}", max_width=250),
                tooltip=store_title,
                icon=folium.Icon(color='darkred', icon='coffee', prefix='fa')
            ).add_to(m)
        except (ValueError, TypeError):
            continue

# Competitors Data
competitors = [
    {"name": "Starbucks CyberHub", "lat": 28.4950, "lon": 77.0890, "brand": "Starbucks", "rev": "₹2.8 Cr/yr"},
    {"name": "Blue Tokai Galleria", "lat": 28.4682, "lon": 77.0818, "brand": "Blue Tokai", "rev": "₹1.9 Cr/yr"},
    {"name": "Third Wave Sector 29", "lat": 28.4685, "lon": 77.0630, "brand": "Third Wave", "rev": "₹1.6 Cr/yr"},
    {"name": "Costa Coffee South Point", "lat": 28.4485, "lon": 77.1080, "brand": "Costa Coffee", "rev": "₹1.4 Cr/yr"}
]

if show_competitors:
    for comp in competitors:
        popup_html = f"<b>{comp['brand']}</b><br>{comp['name']}<br><span style='color:green;'>Est. Rev: {comp['rev']}</span>"
        folium.Marker(
            location=[comp['lat'], comp['lon']],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=comp['name'],
            icon=folium.Icon(color='green' if comp['brand'] == 'Starbucks' else 'blue', icon='cutlery', prefix='fa')
        ).add_to(m)

# Render map on Streamlit page
st_folium(m, width=1200, height=650)
