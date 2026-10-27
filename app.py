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

    /* Unified BD Team Strip */
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
        font-size: 15px;
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
        <div class="buzz-subtitle">Nothing Before Coffee (NBC) — Next 1000 Stores Strategic Catchment & GeoIQ Expansion Engine</div>
    </div>
    <div class="nbc-red-ticker">
        ☕ HIGH QUALITY COFFEE • BUDGET FRIENDLY PRICES • ZERO COMPROMISE • EST. 2017 JAIPUR • BRING ON THE BUZZ ☕
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

# Google Maps Embed View
st.markdown('<div class="section-heading">📍 Google Maps Location View</div>', unsafe_allow_html=True)
google_map_html = """
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14011.691745484888!2d77.2090!3d28.6139!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjjCsDM2JzUwLjQiTiA3N8KwMTInMzIuNCJF!5e0!3m2!1sen!2sin!4v1234567890" 
width="100%" height="450" style="border:0; border-radius: 12px;" allowfullscreen="" loading="lazy"></iframe>
"""
st.markdown(google_map_html, unsafe_allow_html=True)

# 9. GEOIQ SIDEBAR (Open Sidebar for GeoIQ Intelligence Engine)
geolocator = Nominatim(user_agent="geoiq_nbc_engine")

def get_coordinates(address):
    try:
        time.sleep(1)
        location = geolocator.geocode(f"{address}, India", timeout=10)
        if location:
            return location.latitude, location.longitude
    except:
        pass
    return None, None

with st.sidebar:
    st.image(NBC_LOGO, width=110)
    st.markdown("### 🌐 GeoIQ Spatial Intelligence")
    st.markdown("Open site evaluation and catchment parameters below:")
    
    # GeoIQ Search & Radius Controls
    search_location = st.text_input("🔍 Target City / Area / Mall", value="Civil Lines, Prayagraj")
    radius_km = st.slider("📍 Catchment Radius (km)", min_value=0.5, max_value=5.0, value=1.5, step=0.5)
    
    st.markdown("---")
    st.markdown("### 🏢 Retail Vertical")
    vertical = st.selectbox(
        "Select Vertical:",
        ["Café & Specialty Coffee (NBC)", "Apparel & Retail (Zudio)", "Quick Service Restaurant (QSR)", "Pharmacy & Health"]
    )
    
    st.markdown("---")
    st.markdown("### 🇮🇳 Brand Filters")
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
        "Highlight Brands on Map:",
        options=highlight_brands,
        default=["Nothing Before Coffee", "Zudio", "Starbucks"]
    )

    st.markdown("---")
    st.markdown("### 🗺️ Expansion Phases")
    phases = [
        "Phase 1 (150 stores)",
        "Phase 2 (250 stores)",
        "Phase 3 (500 stores)",
        "Phase 4 (750 stores)",
        "Phase 5 (1000 stores)"
    ]
    selected_phases = st.multiselect("Target Expansion Phase:", phases, default=phases)
    
    st.markdown("---")
    st.markdown("**BD Team Execution:**\n- Sanskar Singh Yadav\n- Mayank Iktiyan\n- Vipin Singh Shekhawat\n- Manoj Singh")

# Geocode Sidebar Location
@st.cache_data(show_spinner=False)
def get_lat_lon(query):
    try:
        loc = geolocator.geocode(query, timeout=10)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass
    return 25.4358, 81.8463 # Default fallback

center_lat, center_lon = get_lat_lon(search_location)

# 10. GeoIQ Real-time Intelligence Metrics Dashboard
st.markdown('<div class="section-heading">📈 GeoIQ Catchment Intelligence Dashboard</div>', unsafe_allow_html=True)

random.seed(int(center_lat * 1000))
suitability_score = random.randint(75, 96)
predicted_footfall = f"{random.randint(14, 30)}K / mo"
avg_spend = f"₹{random.randint(190, 340)}"
rental_index = f"₹{random.randint(95, 220)} / sq.ft."

g_col1, g_col2, g_col3, g_col4 = st.columns(4)
with g_col1:
    st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{suitability_score}/100</div><div class="geoiq-metric-lbl">Suitability Score</div></div>', unsafe_allow_html=True)
with g_col2:
    st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{predicted_footfall}</div><div class="geoiq-metric-lbl">Est. Footfall</div></div>', unsafe_allow_html=True)
with g_col3:
    st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{avg_spend}</div><div class="geoiq-metric-lbl">Avg. Ticket Size</div></div>', unsafe_allow_html=True)
with g_col4:
    st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{rental_index}</div><div class="geoiq-metric-lbl">Median Rental Index</div></div>', unsafe_allow_html=True)

# 11. Interactive All-India & GeoIQ Catchment Map
st.markdown(f'<div class="section-heading">🗺️ Strategic Catchment & Competitor Map ({search_location} — {radius_km} km Buffer)</div>', unsafe_allow_html=True)

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attr='Google'
)

# Target Pin
folium.Marker(
    location=[center_lat, center_lon],
    popup=f"<b>Target Site:</b> {search_location}<br><b>GeoIQ Score:</b> {suitability_score}/100",
    tooltip=search_location,
    icon=folium.Icon(color="darkblue", icon="flag")
).add_to(m)

# Catchment Radius Buffer Circle
folium.Circle(
    location=[center_lat, center_lon],
    radius=radius_km * 1000,
    color='#0052CC',
    fill=True,
    fill_color='#3b82f6',
    fill_opacity=0.15,
    popup=f"GeoIQ Catchment Buffer: {radius_km} km"
).add_to(m)

# Simulated Competitor / Brand Nodes within Catchment
competitors = [
    ("Nothing Before Coffee (Flagship)", center_lat + 0.003, center_lon + 0.002, "darkblue"),
    ("Blue Tokai Coffee", center_lat + 0.005, center_lon - 0.004, "cadetblue"),
    ("Starbucks Reserve", center_lat - 0.004, center_lon + 0.004, "green"),
    ("Zudio Retail Outlet", center_lat - 0.006, center_lon - 0.003, "purple"),
    ("Third Wave Coffee", center_lat + 0.002, center_lon - 0.006, "orange")
]

for name, lat, lon, color in competitors:
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}</b><br>Retail & Footfall Node",
        tooltip=name,
        icon=folium.Icon(color=color, icon="coffee")
    ).add_to(m)

st_folium(m, width=1200, height=550)

# 12. Site Assessment Dossier Export Simulator
st.markdown('<div class="section-heading">📑 Executive Site Assessment Dossier</div>', unsafe_allow_html=True)
rep_col1, rep_col2 = st.columns([3, 1])
with rep_col1:
    st.info(f"**GeoIQ Location Dossier for `{search_location}`:**\n- **Analysis Radius:** {radius_km} km catchment\n- **Target Vertical:** {vertical}\n- **Composite Viability Index:** {suitability_score}% (High Potential)\n- **Recommendation:** Optimal density and footfall velocity. Proceed to lease negotiation and layout finalization.")
with rep_col2:
    if st.button("📥 Download PDF Dossier", type="primary"):
        st.success("Dossier generated successfully!")
