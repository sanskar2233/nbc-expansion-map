import streamlit as st
st.markdown("### 📍 Google Maps Location View")

# Google Maps ka embed iframe HTML code yahan paste karein
google_map_html = """
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14011.691745484888!2d77.2090!3d28.6139!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjjCsDM2JzUwLjQiTiA3N8KwMTInMzIuNCJF!5e0!3m2!1sen!2sin!4v1234567890" 
width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
"""

st.markdown(google_map_html, unsafe_allow_html=True)
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Nothing Before Coffee | NBC - Bring on the Buzz",
    page_icon="https://nothingbeforecoffee.com/cdn/shop/files/logo.png?height=100&v=1770827259",
    layout="wide"
)

# 2. Official NBC Image URLs (Provided by You)
NBC_LOGO = "https://nothingbeforecoffee.com/cdn/shop/files/logo.png?height=100&v=1770827259"
FOUNDERS_IMG = "https://nothingbeforecoffee.com/cdn/shop/files/nbc-founders-hp_bbe73571-7943-4e91-b2ad-5d07612dc3e6.png?v=1773324436&width=832"
GALLERY_IMG_1 = "https://cdn.shopify.com/s/files/1/0694/5374/2274/files/01.png?v=1772269574"
GALLERY_IMG_2 = "https://nothingbeforecoffee.com/cdn/shop/files/02.png?v=1772269573&width=352"
GALLERY_IMG_3 = "https://nothingbeforecoffee.com/cdn/shop/files/03.png?v=1772269573&width=352"

# 3. Custom CSS (Exact NBC Website Blue, White & Red Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Top Header & Bring on the Buzz Banner */
    .nbc-hero-wrapper {
        background: linear-gradient(180deg, #F4F8FB 0%, #FFFFFF 100%);
        border: 3px solid #0052CC;
        border-radius: 16px;
        padding: 25px 30px;
        text-align: center;
        margin-bottom: 0px;
        box-shadow: 0 6px 18px rgba(0, 82, 204, 0.08);
    }
    .buzz-title {
        font-size: 64px;
        font-weight: 900;
        color: #0052CC;
        letter-spacing: 2px;
        line-height: 1.05;
        text-transform: uppercase;
        margin: 10px 0 5px 0;
    }
    .buzz-subtitle {
        font-size: 18px;
        font-weight: 700;
        color: #333333;
        margin-bottom: 12px;
    }

    /* Red Ticker Bar like NBC Website */
    .nbc-red-ticker {
        background-color: #E63946;
        color: #FFFFFF;
        padding: 12px 20px;
        font-weight: 800;
        font-size: 14px;
        letter-spacing: 1.5px;
        text-align: center;
        text-transform: uppercase;
        border-radius: 0 0 12px 12px;
        margin-top: -8px;
        margin-bottom: 20px;
    }

    /* Unified BD Team Strip (Integrated right into the main dashboard) */
    .bd-team-banner {
        background-color: #0052CC;
        color: #FFFFFF;
        padding: 16px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0, 82, 204, 0.2);
    }
    .bd-team-title {
        font-size: 15px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #FFD166;
    }
    .bd-members {
        font-size: 16px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .bd-badge {
        background-color: rgba(255, 255, 255, 0.18);
        padding: 6px 14px;
        border-radius: 20px;
        margin: 0 5px;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }

    /* NBC Stats Counter Cards */
    .stat-card {
        background-color: #FFFFFF;
        border-bottom: 4px solid #0052CC;
        border-radius: 12px;
        padding: 18px 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    .stat-number {
        font-size: 36px;
        font-weight: 900;
        color: #E63946;
        line-height: 1.1;
    }
    .stat-label {
        font-size: 14px;
        font-weight: 800;
        color: #0052CC;
        text-transform: uppercase;
        margin-top: 6px;
    }

    /* Founders Blue Story Section */
    .founders-story-box {
        background-color: #0052CC;
        color: #FFFFFF;
        padding: 35px;
        border-radius: 16px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 6px 18px rgba(0, 82, 204, 0.18);
    }
    .founders-story-box h3 {
        color: #FFFFFF;
        font-weight: 900;
        font-size: 26px;
        margin-bottom: 15px;
    }
    .founders-story-box p {
        font-size: 16px;
        line-height: 1.6;
        font-weight: 500;
        color: #F0F4F8;
    }

    /* Red Gallery Section Header */
    .section-heading {
        font-size: 26px;
        font-weight: 900;
        color: #0052CC;
        text-transform: uppercase;
        margin: 30px 0 15px 0;
        border-left: 6px solid #E63946;
        padding-left: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 4. Top Header with Official NBC Logo & "BRING ON THE BUZZ"
col_logo, col_hero = st.columns([1, 5])
with col_logo:
    st.image(NBC_LOGO, width=130)
with col_hero:
    st.markdown("""
    <div class="nbc-hero-wrapper">
        <div class="buzz-title">BRING ON THE BUZZ</div>
        <div class="buzz-subtitle">Nothing Before Coffee (NBC) — Next 1000 Stores Strategic Catchment & Expansion Engine</div>
    </div>
    <div class="nbc-red-ticker">
        ☕ HIGH QUALITY COFFEE • BUDGET FRIENDLY PRICES • ZERO COMPROMISE • EST. 2017 JAIPUR • BRING ON THE BUZZ ☕
    </div>
    """, unsafe_allow_html=True)

# 5. Integrated BD Leadership & Expansion Team Banner (One Unified Team Strip)
st.markdown("""
<div class="bd-team-banner">
    <div class="bd-team-title">🚀 Business Development & Expansion Team</div>
    <div class="bd-members">
        <span class="bd-badge">👔 Vipin Singh Shekhawat (BD Manager)</span>
        <span class="bd-badge">👔 Manoj Singh (BD Manager)</span>
        <span class="bd-badge">📍 Mayank Iktiyan (BD & Expansion)</span>
        <span class="bd-badge">📍 Sanskar Singh Yadav (BD & Expansion)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Official NBC Key Metrics (110+ Outlets, 15 Cities, 1,00,000+ Cups, 2,50,000+ Customers)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="stat-card"><div class="stat-number">110+</div><div class="stat-label">Outlets</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="stat-card"><div class="stat-number">15+</div><div class="stat-label">Cities</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="stat-card"><div class="stat-number">1,00,000+</div><div class="stat-label">Cups Served</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="stat-card"><div class="stat-number">2,50,000+</div><div class="stat-label">Happy Customers</div></div>', unsafe_allow_html=True)

# 7. Founders & Our Story Section (Exact NBC Blue Split Interface)
st.markdown('<div class="section-heading">Our Story & Founders</div>', unsafe_allow_html=True)
f_col1, f_col2 = st.columns([1.2, 1])
with f_col1:
    st.image(FOUNDERS_IMG, caption="Nothing Before Coffee — Founders (Ankesh Jain, Anand Jain, Akshay Kedia & Shubham Bhandari)", use_container_width=True)
with f_col2:
    st.markdown("""
    <div class="founders-story-box">
        <h3>BREWING STORIES SINCE 2017</h3>
        <p><b>It all started in Jaipur. Four friends. Endless conversations. Big dreams. And one simple question:</b><br>
        <i>Why is great coffee either too expensive or too ordinary?</i></p>
        <p>In 2017, these four Jaipur-based coffee lovers decided to change the game. They believed you should not have to choose between quality and affordability. You deserve both. And so, <b>Nothing Before Coffee</b> was born.</p>
    </div>
    """, unsafe_allow_html=True)

# 8. NBC Brand Gallery & Outlets Section (Using Your 3 Copied Links)
st.markdown('<div class="section-heading">NBC Outlets & Culture Gallery</div>', unsafe_allow_html=True)
g1, g2, g3 = st.columns(3)
with g1:
    st.image(GALLERY_IMG_1, caption="Bring On The Buzz — NBC Culture", use_container_width=True)
with g2:
    st.image(GALLERY_IMG_2, caption="NBC Core Team & Community", use_container_width=True)
with g3:
    st.image(GALLERY_IMG_3, caption="Nothing Before Coffee — Signature Outlet", use_container_width=True)

# 9. Sidebar Filter & Map Engine
geolocator = Nominatim(user_agent="nbc_bd_expansion_app")

def get_coordinates(address):
    try:
        time.sleep(1)
        location = geolocator.geocode(f"{address}, Delhi NCR, India", timeout=10)
        if location:
            return location.latitude, location.longitude
    except (GeocoderTimedOut, Exception):
        return None, None
    return None, None

@st.cache_data(show_spinner=False)
def load_and_process_data():
    df = pd.read_csv("Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv", encoding='latin1')
    lat_col = next((c for c in df.columns if c.strip().lower() in ['latitude', 'lat']), None)
    lon_col = next((c for c in df.columns if c.strip().lower() in ['longitude', 'lon', 'long']), None)
    addr_col = next((c for c in df.columns if 'address' in c.strip().lower() or 'location' in c.strip().lower() or 'market' in c.strip().lower()), None)
    name_col = next((c for c in df.columns if 'name' in c.strip().lower() or 'store' in c.strip().lower() or 'city' in c.strip().lower()), None)
    phase_col = next((c for c in df.columns if 'phase' in c.strip().lower()), None)

    if lat_col and lon_col:
        df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
        df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
        df = df.dropna(subset=[lat_col, lon_col])
    elif addr_col:
        coords = df[addr_col].apply(get_coordinates)
        df['Latitude'] = [c[0] if c else None for c in coords]
        df['Longitude'] = [c[1] if c else None for c in coords]
        lat_col, lon_col = 'Latitude', 'Longitude'
        df = df.dropna(subset=[lat_col, lon_col])

    return df, lat_col, lon_col, addr_col, name_col, phase_col

with st.sidebar:
    st.image(NBC_LOGO, width=110)
    st.markdown("### 🗺️ NBC Expansion Phases")
    phases = [
        "Phase 1 (150 stores)",
        "Phase 2 (250 stores)",
        "Phase 3 (500 stores)",
        "Phase 4 (750 stores)",
        "Phase 5 (1000 stores)"
    ]
    selected_phases = st.multiselect("Select Target Expansion Phase:", phases, default=phases)
    st.markdown("---")
    st.markdown("**BD Leadership Team:**\n- Vipin Singh Shekhawat\n- Manoj Singh\n- Mayank Iktiyan\n- Sanskar Singh Yadav")

# 10. Interactive Catchment Map Section
st.markdown('<div class="section-heading">Next 1000 Stores Catchment & Expansion Map</div>', unsafe_allow_html=True)

m = folium.Map(location=[28.6139, 77.2090], zoom_start=10, tiles="OpenStreetMap")

try:
    df, lat_col, lon_col, addr_col, name_col, phase_col = load_and_process_data()

    if phase_col and selected_phases:
        filtered_df = df[df[phase_col].astype(str).isin(selected_phases)]
        if filtered_df.empty:
            filtered_df = df
    else:
        filtered_df = df

    for comp in filtered_df.to_dict('records'):
        lat = comp.get(lat_col)
        lon = comp.get(lon_col)
        if pd.notna(lat) and pd.notna(lon):
            store_title = comp.get(name_col, "NBC Target Location") if name_col else "NBC Target Location"
            store_addr = comp.get(addr_col, "") if addr_col else ""
            store_phase = comp.get(phase_col, "Expansion") if phase_col else "Expansion"

            popup_html = f"""
            <div style='width: 200px; font-family: Montserrat, sans-serif;'>
                <b style='color: #0052CC; font-size: 14px;'>{store_title}</b><br>
                <span style='color: #E63946; font-weight: bold; font-size: 12px;'>{store_phase}</span><br>
                <span style='font-size: 11px; color: #333;'>{store_addr}</span>
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=240),
                tooltip=str(store_title),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    st_folium(m, width=1200, height=550)

except Exception as e:
    st.error(f"Error loading CSV file: {e}")
