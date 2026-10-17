import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="NBC Expansion Engine", layout="wide")

# Custom UI Styling
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E272C; margin-bottom: 2px; }
    .sub-title { font-size: 16px; color: #607D8B; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar: Brand Logo, Phase Filters & Layers ---
with st.sidebar:
    # NBC Logo - Direct image path ya URL replace karein
    st.image(
        "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/mug-hot.svg", 
        width=70, 
        caption="Nothing Before Coffee"
    )
    st.markdown("### Expansion Deck Controls")
    
    # Phase Breakdown Filters
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
    
    # Competitor Layer Toggle
    show_competitors = st.checkbox("Show Competitor Intelligence & Revenue", value=True)
    show_catchment = st.checkbox("Show 1 KM Catchment Buffers", value=True)

st.markdown("<div class='main-title'>Nothing Before Coffee (NBC) - Expansion Strategy</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>Visualizing <b>{selected_phase}</b> | Next 1000 Stores Catchment Analysis</div>", unsafe_allow_html=True)

# Default Map Center (Delhi NCR / North India coverage)
m = folium.Map(location=[28.4595, 77.0266], zoom_start=10, tiles="OpenStreetMap")

# --- Load Data from Excel/CSV ---
@st.cache_data
def load_data():
    try:
        # Agar multiple sheets wali Excel/CSV file hai toh usse read karein
        df = pd.read_csv("Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv", encoding="latin1", on_bad_lines='skip')
        return df
    except Exception as e:
        # Fallback empty dataframe
        return pd.DataFrame()

df_stores = load_data()

# Data plotting according to selected phase count
if not df_stores.empty:
    # Latitude aur Longitude columns detect karein
    lat_col = next((c for c in df_stores.columns if c.strip().lower() in ['latitude', 'lat']), None)
    lon_col = next((c for c in df_stores.columns if c.strip().lower() in ['longitude', 'lon', 'lng']), None)
    name_col = next((c for c in df_stores.columns if c.strip().lower() in ['micro-market / catchment', 'micro-market', 'store_name', 'outlet_name', 'name']), None)

    if lat_col and lon_col:
        # Limit records based on phase selection
        df_filtered = df_stores.dropna(subset=[lat_col, lon_col]).head(store_limit)
        
        for _, row in df_filtered.iterrows():
            try:
                lat = float(row[lat_col])
                lon = float(row[lon_col])
                store_title = str(row[name_col]) if name_col else "Proposed NBC Site"
                
                # Catchment Area Buffer
                if show_catchment:
                    folium.Circle(
                        location=[lat, lon],
                        radius=1000,
                        color="#0984E3",
                        fill=True,
                        fill_color="#74B9FF",
                        fill_opacity=0.18,
                        popup=f"1 KM Catchment: {store_title}"
                    ).add_to(m)

                # NBC Marker
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(f"<b>NBC Expansion Site</b><br>{store_title}", max_width=250),
                    tooltip=store_title,
                    icon=folium.Icon(color='darkred', icon='coffee', prefix='fa')
                ).add_to(m)
            except (ValueError, TypeError):
                continue

# --- Competitors
