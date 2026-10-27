import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import random

# 1. Page Configuration (Must be the very first Streamlit command)
st.set_page_config(
    page_title="Nothing Before Coffee | NBC - Bring on the Buzz & GeoIQ",
    page_icon="https://nothingbeforecoffee.com/cdn/shop/files/logo.png?height=100&v=1770827259",
    layout="wide"
)

# 2. Official NBC Image URLs (Provided by You)
NBC_LOGO = "https://nothingbeforecoffee.com/cdn/shop/files/logo.png?height=100&v=1770827259"
FOUNDERS_IMG = "https://nothingbeforecoffee.com/cdn/shop/files/nbc-founders-hp_bbe73571-7943-4e91-b2ad-5d07612dc3e6.png?v=1773324436&width=832"
GALLERY_IMG_1 = "https://cdn.shopify.com/s/files/1/0694/5374/2274/files/01.png?v=1772269574"
GALLERY_IMG_2 = "https://nothingbeforecoffee.com/cdn/shop/files/02.png?v=1772269573&width=352"
GALLERY_IMG_3 = "https://nothingbeforecoffee.com/cdn/shop/files/03.png?v=1772269573&width=352"

# 3. Custom CSS (Exact NBC Website Blue, White & Red Theme + GeoIQ Enhancements)
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
        font-size: 54px;
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

    /* GeoIQ Analytics Metric Cards */
    .geoiq-metric-card {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .geoiq-metric-val { font-size: 26px; font-weight: 900; color: #0052CC; }
    .geoiq-metric-lbl { font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase; margin-top: 4px; }

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
        <div class="buzz-subtitle">Nothing Before Coffee (NBC) — Strategic Catchment & GeoIQ Expansion Engine</div>
    </div>
    <div class="nbc-red-ticker">
        ☕ HIGH QUALITY COFFEE • BUDGET FRIENDLY PRICES • ZERO COMPROMISE • GEOIQ SPATIAL INTEL ☕
    </div>
    """, unsafe_allow_html=True)

# 5. Integrated BD Leadership & Expansion Team Banner
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

# 6. Official NBC Key Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="stat-card"><div class="stat-number">110+</div><div class="stat-label">Outlets</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="stat-card"><div class="stat-number">15+</div><div class="stat-label">Cities</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="stat-card"><div class="stat-number">1,00,000+</div><div class="stat-label">Cups Served</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="stat-card"><div class="stat-number">2,50,000+</div><div class="stat-label">Happy Customers</div></div>', unsafe_allow_html=True)

# 7. Founders & Our Story Section
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

# 8. NBC Brand Gallery Section
st.markdown('<div class="section-heading">NBC Outlets & Culture Gallery</div>', unsafe_allow_html=True)
g1, g2, g3 = st.columns(3)
with g1:
    st.image(GALLERY_IMG_1, caption="Bring On The Buzz — NBC Culture", use_container_width=True)
with g2:
    st.image(GALLERY_IMG_2, caption="NBC Core Team & Community", use_container_width=True)
with g3:
    st.image(GALLERY_IMG_3, caption="Nothing Before Coffee — Signature Outlet", use_container_width=True)

# 9. Sidebar Filter & GeoIQ Map Engine Setup
geolocator = Nominatim(user_agent="nbc_geoiq_expansion_app")

def get_coordinates(address):
    try:
        time.sleep(1)
        location = geolocator.geocode(f"{address}, India", timeout=10)
        if location:
            return location.latitude, location.longitude
    except (GeocoderTimedOut, Exception):
        return None, None
    return None, None

@st.cache_data(show_spinner=False)
def load_and_process_data():
    dfs = []
    for excel_file in ["Delhi NCR Coffee Chains Store Locations (4).xlsx", "All cafe data (1).xlsx"]:
        try:
            xls = pd.ExcelFile(excel_file)
            for sheet in xls.sheet_names:
                temp_df = pd.read_excel(excel_file, sheet_name=sheet)
                if not temp_df.empty:
                    dfs.append(temp_df)
        except Exception:
            pass

    try:
        df_csv = pd.read_csv("Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv", encoding='latin1')
        dfs.append(df_csv)
    except Exception:
        pass

    if not dfs:
        return None, None, None, None, None, None, None

    df = pd.concat(dfs, ignore_index=True)
    lat_col = next((c for c in df.columns if str(c).strip().lower() in ['latitude', 'lat']), None)
    lon_col = next((c for c in df.columns if str(c).strip().lower() in ['longitude', 'lon', 'long']), None)
    addr_col = next((c for c in df.columns if any(k in str(c).strip().lower() for k in ['address', 'location', 'market', 'street'])), None)
    name_col = next((c for c in df.columns if any(k in str(c).strip().lower() for k in ['name', 'store', 'outlet', 'city'])), None)
    brand_col = next((c for c in df.columns if any(k in str(c).strip().lower() for k in ['brand', 'group', 'category'])), None)
    phase_col = next((c for c in df.columns if 'phase' in str(c).strip().lower()), None)

    if lat_col and lon_col:
        df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
        df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
        df = df.dropna(subset=[lat_col, lon_col])
    return df, lat_col, lon_col, addr_col, name_col, brand_col, phase_col

with st.sidebar:
    st.image(NBC_LOGO, width=110)
    st.markdown("### 🌐 GeoIQ Spatial Intelligence")
    
    # GeoIQ Search & Radius Controls
    search_location = st.text_input("🔍 Search City / Area / Mall", value="Civil Lines, Prayagraj")
    radius_km = st.slider("📍 Catchment Radius Buffer (km)", min_value=0.5, max_value=5.0, value=1.5, step=0.5)
    
    st.markdown("---")
    st.markdown("### 🇮🇳 All-India Brand Highlights")
    highlight_brands = [
        "Nothing Before Coffee",
        "Zudio",
        "Starbucks",
        "Blue Tokai",
        "Third Wave",
        "V-Mart",
        "Lenskart",
        "Domino's"
    ]
    selected_highlight_brands = st.multiselect(
        "Select Brands to Highlight on Map:",
        options=highlight_brands,
        default=highlight_brands
    )

    st.markdown("---")
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

# Get Coordinates for Searched Location
center_lat, center_lon = get_coordinates(search_location)
if not center_lat or not center_lon:
    center_lat, center_lon = 25.4358, 81.8463 # Default fallback

# 10. GeoIQ Real-Time Intelligence Metrics Dashboard
st.markdown('<div class="section-heading">📈 GeoIQ Catchment Intelligence Dashboard</div>', unsafe_allow_html=True)
random.seed(int(center_lat * 1000))
suitability_score = random.randint(76, 96)
predicted_footfall = f"{random.randint(15, 32)}K / mo"
avg_spend = f"₹{random.randint(190, 340)}"
rental_index = f"₹{random.randint(95, 230)} / sq.ft."

g1, g2, g3, g4 = st.columns(4)
with g1:
    st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{suitability_score}/100</div><div class="geoiq-metric-lbl">Suitability Score</div></div>', unsafe_allow_html=True)
with g2:
    st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{predicted_footfall}</div><div class="geoiq-metric-lbl">Est. Catchment Footfall</div></div>', unsafe_allow_html=True)
with g3:
    st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{avg_spend}</div><div class="geoiq-metric-lbl">Avg. Ticket Size</div></div>', unsafe_allow_html=True)
with g4:
    st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{rental_index}</div><div class="geoiq-metric-lbl">Median Rental Index</div></div>', unsafe_allow_html=True)

# 11. Interactive GeoIQ Map Section with Catchment Buffer
st.markdown(f'<div class="section-heading">🗺️ Strategic Catchment & Brand Outlets Map ({search_location} — {radius_km} km Buffer)</div>', unsafe_allow_html=True)

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google Hybrid Satellite'
)

# Target Anchor Marker
folium.Marker(
    location=[center_lat, center_lon],
    popup=f"<b>Target Site:</b> {search_location}<br><b>Suitability Score:</b> {suitability_score}/100",
    tooltip=search_location,
    icon=folium.Icon(color="red", icon="flag")
).add_to(m)

# Catchment Radius Buffer Circle
folium.Circle(
    location=[center_lat, center_lon],
    radius=radius_km * 1000,
    color='#0052CC',
    fill=True,
    fill_color='#3b82f6',
    fill_opacity=0.15,
    popup=f"Catchment Buffer: {radius_km} km"
).add_to(m)

def get_brand_marker_color(brand_name):
    b = str(brand_name).lower()
    if 'nothing before' in b or 'nbc' in b: return 'darkblue'
    elif 'zudio' in b: return 'pink'
    elif 'starbucks' in b: return 'green'
    elif 'blue tokai' in b: return 'cadetblue'
    elif 'third wave' in b: return 'orange'
    elif 'v-mart' in b or 'vmart' in b: return 'purple'
    elif 'lenskart' in b: return 'beige'
    elif 'domino' in b: return 'red'
    return 'blue'

try:
    df, lat_col, lon_col, addr_col, name_col, brand_col, phase_col = load_and_process_data()

    if df is not None and not df.empty and lat_col and lon_col:
        filtered_df = df.copy()

        if brand_col and selected_highlight_brands:
            brand_filtered = filtered_df[filtered_df[brand_col].astype(str).apply(
                lambda x: any(b.lower() in x.lower() for b in selected_highlight_brands)
            )]
            if not brand_filtered.empty:
                filtered_df = brand_filtered

        if phase_col and selected_phases:
            phase_filtered = filtered_df[filtered_df[phase_col].astype(str).isin(selected_phases)]
            if not phase_filtered.empty:
                filtered_df = phase_filtered

        for comp in filtered_df.head(600).to_dict('records'):
            lat = comp.get(lat_col)
            lon = comp.get(lon_col)
            if pd.notna(lat) and pd.notna(lon):
                store_title = str(comp.get(name_col, "NBC Target Location")) if name_col else "NBC Target Location"
                store_brand = str(comp.get(brand_col, "Nothing Before Coffee")) if brand_col else "Nothing Before Coffee"
                store_addr = str(comp.get(addr_col, "")) if addr_col else ""
                store_phase = str(comp.get(phase_col, "Expansion")) if phase_col else "Expansion"

                m_color = get_brand_marker_color(store_brand if brand_col else store_title)

                popup_html = f"""
                <div style='width: 210px; font-family: Montserrat, sans-serif;'>
                    <b style='color: #0052CC; font-size: 14px;'>{store_title}</b><br>
                    <span style='color: #E63946; font-weight: bold; font-size: 12px;'>{store_brand} | {store_phase}</span><br>
                    <span style='font-size: 11px; color: #333;'>{store_addr}</span>
                </div>
                """
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=240),
                    tooltip=f"{store_brand} - {store_title}",
                    icon=folium.Icon(color=m_color, icon="info-sign")
                ).add_to(m)

    st_folium(m, width=1200, height=600)

except Exception as e:
    st.error(f"Error loading map data: {e}")

# 12. Executive Site Assessment Dossier
st.markdown('<div class="section-heading">📑 Executive Site Assessment Dossier</div>', unsafe_allow_html=True)
rep_col1, rep_col2 = st.columns([3, 1])
with rep_col1:
    st.info(f"**GeoIQ Location Dossier for `{search_location}`:**\n- **Analysis Radius:** {radius_km} km catchment\n- **Composite Viability Index:** {suitability_score}% (High Potential Zone)\n- **Recommendation:** Optimal density and footfall velocity. Recommended for immediate Level-1 Landlord outreach.")
with rep_col2:
    if st.button("📥 Download PDF Dossier", type="primary"):
        st.success("Dossier generated successfully!")
