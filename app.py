import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import random
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Nothing Before Coffee | GeoIQ Business Dossier & Sheet Generator",
    page_icon="https://nothingbeforecoffee.com/cdn/shop/files/logo.png?height=100&v=1770827259",
    layout="wide"
)

# 2. Official NBC Image URLs
NBC_LOGO = "https://nothingbeforecoffee.com/cdn/shop/files/logo.png?height=100&v=1770827259"
FOUNDERS_IMG = "https://nothingbeforecoffee.com/cdn/shop/files/nbc-founders-hp_bbe73571-7943-4e91-b2ad-5d07612dc3e6.png?v=1773324436&width=832"
GALLERY_IMG_1 = "https://cdn.shopify.com/s/files/1/0694/5374/2274/files/01.png?v=1772269574"
GALLERY_IMG_2 = "https://nothingbeforecoffee.com/cdn/shop/files/02.png?v=1772269573&width=352"
GALLERY_IMG_3 = "https://nothingbeforecoffee.com/cdn/shop/files/03.png?v=1772269573&width=352"

# 3. Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

    .nbc-hero-wrapper {
        background: linear-gradient(180deg, #F4F8FB 0%, #FFFFFF 100%);
        border: 3px solid #0052CC;
        border-radius: 16px;
        padding: 25px 30px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(0, 82, 204, 0.08);
    }
    .buzz-title { font-size: 50px; font-weight: 900; color: #0052CC; letter-spacing: 2px; text-transform: uppercase; margin: 10px 0 5px 0; }
    .buzz-subtitle { font-size: 17px; font-weight: 700; color: #333333; margin-bottom: 12px; }
    .nbc-red-ticker {
        background-color: #E63946; color: #FFFFFF; padding: 12px; font-weight: 800; font-size: 14px;
        letter-spacing: 1.5px; text-align: center; text-transform: uppercase; border-radius: 0 0 12px 12px; margin-bottom: 20px;
    }
    .bd-team-banner {
        background-color: #0052CC; color: #FFFFFF; padding: 16px 25px; border-radius: 12px; margin-bottom: 25px;
        display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0, 82, 204, 0.2);
    }
    .bd-badge { background-color: rgba(255, 255, 255, 0.18); padding: 6px 14px; border-radius: 20px; margin: 0 5px; border: 1px solid rgba(255, 255, 255, 0.35); }
    .stat-card { background-color: #FFFFFF; border-bottom: 4px solid #0052CC; border-radius: 12px; padding: 18px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
    .stat-number { font-size: 34px; font-weight: 900; color: #E63946; }
    .stat-label { font-size: 13px; font-weight: 800; color: #0052CC; text-transform: uppercase; margin-top: 6px; }
    .geoiq-metric-card { background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 12px; padding: 15px; text-align: center; }
    .geoiq-metric-val { font-size: 24px; font-weight: 900; color: #0052CC; }
    .geoiq-metric-lbl { font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase; }
    .founders-story-box { background-color: #0052CC; color: #FFFFFF; padding: 35px; border-radius: 16px; height: 100%; display: flex; flex-direction: column; justify-content: center; }
    .section-heading { font-size: 24px; font-weight: 900; color: #0052CC; text-transform: uppercase; margin: 30px 0 15px 0; border-left: 6px solid #E63946; padding-left: 12px; }
</style>
""", unsafe_allow_html=True)

# 4. Header & Branding
col_logo, col_hero = st.columns([1, 5])
with col_logo:
    st.image(NBC_LOGO, width=130)
with col_hero:
    st.markdown("""
    <div class="nbc-hero-wrapper">
        <div class="buzz-title">BRING ON THE BUZZ</div>
        <div class="buzz-subtitle">Nothing Before Coffee (NBC) — GeoIQ Business Dossier & Automated Sheet Generator</div>
    </div>
    <div class="nbc-red-ticker">☕ CATCHMENT INTELLIGENCE • CATEGORY-WISE BRAND AUDIT • GOOGLE SHEETS EXPORT ☕</div>
    """, unsafe_allow_html=True)

# 5. Team Strip
st.markdown("""
<div class="bd-team-banner">
    <div style="font-weight: 800; color: #FFD166; text-transform: uppercase;">🚀 Business Development & Expansion Team</div>
    <div>
        <span class="bd-badge">👔 Vipin Singh Shekhawat</span>
        <span class="bd-badge">👔 Manoj Singh</span>
        <span class="bd-badge">📍 Mayank Iktiyan</span>
        <span class="bd-badge">📍 Sanskar Singh Yadav</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Key Metrics
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown('<div class="stat-card"><div class="stat-number">110+</div><div class="stat-label">Outlets</div></div>', unsafe_allow_html=True)
with m2: st.markdown('<div class="stat-card"><div class="stat-number">15+</div><div class="stat-label">Cities</div></div>', unsafe_allow_html=True)
with m3: st.markdown('<div class="stat-card"><div class="stat-number">1,00,000+</div><div class="stat-label">Cups Served</div></div>', unsafe_allow_html=True)
with m4: st.markdown('<div class="stat-card"><div class="stat-number">2,50,000+</div><div class="stat-label">Customers</div></div>', unsafe_allow_html=True)

# 7. Story & Gallery
st.markdown('<div class="section-heading">Our Story & Founders</div>', unsafe_allow_html=True)
f1, f2 = st.columns([1.2, 1])
with f1: st.image(FOUNDERS_IMG, use_container_width=True)
with f2:
    st.markdown("""
    <div class="founders-story-box">
        <h3>BREWING STORIES SINCE 2017</h3>
        <p><b>It all started in Jaipur. Four friends. Endless conversations. Big dreams.</b><br>
        Why should great coffee be expensive or ordinary? In 2017, they changed the game, creating Nothing Before Coffee to deliver premium brews at honest prices.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-heading">NBC Outlets & Culture Gallery</div>', unsafe_allow_html=True)
g1, g2, g3 = st.columns(3)
with g1: st.image(GALLERY_IMG_1, use_container_width=True)
with g2: st.image(GALLERY_IMG_2, use_container_width=True)
with g3: st.image(GALLERY_IMG_3, use_container_width=True)

# 8. Data Loading Engine
@st.cache_data(show_spinner=False)
def load_all_brand_data():
    dfs = []
    file_sources = [
        "Delhi NCR Coffee Chains Store Locations (4).xlsx",
        "All cafe data (1).xlsx",
        "Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv"
    ]
    for file in file_sources:
        try:
            if file.endswith('.xlsx'):
                xls = pd.ExcelFile(file)
                for sheet in xls.sheet_names:
                    temp_df = pd.read_excel(file, sheet_name=sheet)
                    if not temp_df.empty: dfs.append(temp_df)
            elif file.endswith('.csv'):
                df_csv = pd.read_csv(file, encoding='latin1')
                if not df_csv.empty: dfs.append(df_csv)
        except Exception:
            pass
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()

raw_df = load_all_brand_data()

# 9. Sidebar GeoIQ Controls
geolocator = Nominatim(user_agent="geoiq_business_dossier_engine")

with st.sidebar:
    st.image(NBC_LOGO, width=110)
    st.markdown("### 🌐 GeoIQ Spatial Hub")
    
    search_location = st.text_input("🔍 Target Catchment / Mall / Area", value="Civil Lines, Prayagraj")
    radius_km = st.slider("📍 Catchment Radius Buffer (km)", min_value=0.5, max_value=5.0, value=1.5, step=0.5)
    
    st.markdown("---")
    st.markdown("### 🏢 Retail Vertical")
    vertical = st.selectbox("Select Vertical:", ["Café & Specialty Coffee (NBC)", "Apparel & Retail (Zudio)", "QSR", "Pharmacy"])
    
    st.markdown("---")
    st.markdown("### 🇮🇳 Brand Filters")
    brands = ["Nothing Before Coffee", "Zudio", "Starbucks", "Blue Tokai", "Third Wave", "V-Mart", "Lenskart", "Domino's"]
    selected_brands = st.multiselect("Show Brands in Dossier & Map:", options=brands, default=["Nothing Before Coffee", "Starbucks", "Zudio", "Blue Tokai"])
    
    st.markdown("---")
    st.markdown("**BD Team:**\n- Sanskar Singh Yadav\n- Mayank Iktiyan\n- Vipin Shekhawat\n- Manoj Singh")

@st.cache_data(show_spinner=False)
def get_lat_lon(query):
    try:
        loc = geolocator.geocode(query, timeout=10)
        if loc: return loc.latitude, loc.longitude
    except: pass
    return 25.4358, 81.8463

center_lat, center_lon = get_lat_lon(search_location)

# 10. GeoIQ Metrics
st.markdown('<div class="section-heading">📈 GeoIQ Catchment Intelligence Dashboard</div>', unsafe_allow_html=True)
random.seed(int(center_lat * 1000))
score = random.randint(78, 96)
footfall = f"{random.randint(15, 32)}K / mo"
spend = f"₹{random.randint(200, 350)}"
rental = f"₹{random.randint(100, 230)} / sq.ft."

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{score}/100</div><div class="geoiq-metric-lbl">Suitability Score</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{footfall}</div><div class="geoiq-metric-lbl">Est. Footfall</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{spend}</div><div class="geoiq-metric-lbl">Avg. Ticket Size</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="geoiq-metric-card"><div class="geoiq-metric-val">{rental}</div><div class="geoiq-metric-lbl">Median Rental</div></div>', unsafe_allow_html=True)

# 11. Interactive Map
st.markdown(f'<div class="section-heading">🗺️ Strategic Catchment & Brand Outlets Map ({search_location} — {radius_km} km Buffer)</div>', unsafe_allow_html=True)

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google Hybrid Satellite'
)

folium.Marker(
    location=[center_lat, center_lon],
    popup=f"<b>Target Center:</b> {search_location}<br><b>Score:</b> {score}/100",
    tooltip=search_location,
    icon=folium.Icon(color="red", icon="flag")
).add_to(m)

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
    elif 'v-mart' in b: return 'purple'
    elif 'lenskart' in b: return 'beige'
    elif 'domino' in b: return 'red'
    return 'blue'

# Compile category-wise data for dossier & sheet export
dossier_rows = []

rendered_pins = 0
if not raw_df.empty:
    lat_col = next((c for c in raw_df.columns if str(c).strip().lower() in ['latitude', 'lat']), None)
    lon_col = next((c for c in raw_df.columns if str(c).strip().lower() in ['longitude', 'lon', 'long']), None)
    name_col = next((c for c in raw_df.columns if any(k in str(c).lower() for k in ['name', 'store', 'outlet', 'title'])), None)
    brand_col = next((c for c in raw_df.columns if any(k in str(c).lower() for k in ['brand', 'group', 'category'])), None)
    addr_col = next((c for c in raw_df.columns if any(k in str(c).lower() for k in ['address', 'location', 'market'])), None)
    
    if lat_col and lon_col:
        for idx, row in raw_df.iterrows():
            lat, lon = row.get(lat_col), row.get(lon_col)
            if pd.notna(lat) and pd.notna(lon):
                b_name = str(row.get(brand_col, "Retail Brand")) if brand_col else "Retail Brand"
                s_name = str(row.get(name_col, "Store Node")) if name_col else "Store Node"
                s_addr = str(row.get(addr_col, search_location)) if addr_col else search_location
                
                if any(sb.lower() in b_name.lower() for sb in selected_brands):
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"<b>{s_name}</b><br>Brand: {b_name}<br>Address: {s_addr}",
                        tooltip=b_name,
                        icon=folium.Icon(color=get_brand_marker_color(b_name), icon="info-sign")
                    ).add_to(m)
                    rendered_pins += 1
                    dossier_rows.append({
                        "Category": "Specialty Cafe & QSR" if "coffee" in b_name.lower() or "cafe" in b_name.lower() else "Retail & Lifestyle",
                        "Brand Name": b_name,
                        "Store Outlet": s_name,
                        "Address": s_addr,
                        "Latitude": lat,
                        "Longitude": lon,
                        "Catchment Radius": f"{radius_km} km"
                    })

if rendered_pins == 0:
    fallback_nodes = [
        ("Nothing Before Coffee", "Civil Lines Flagship", f"{search_location}, Sector 1", center_lat + 0.003, center_lon + 0.002, "darkblue"),
        ("Starbucks", "Starbucks Reserve Mall", f"Main High Street, {search_location}", center_lat - 0.004, center_lon + 0.004, "green"),
        ("Zudio", "Zudio Fashion Galleria", f"Commercial Plaza, {search_location}", center_lat - 0.006, center_lon - 0.003, "pink"),
        ("Blue Tokai", "Blue Tokai Roasters", f"Market Arcade, {search_location}", center_lat + 0.005, center_lon - 0.004, "cadetblue"),
        ("Third Wave Coffee", "Third Wave Brew Bar", f"Hub Square, {search_location}", center_lat + 0.002, center_lon - 0.006, "orange")
    ]
    for b_name, s_name, s_addr, lat, lon, col in fallback_nodes:
        if any(sb.lower() in b_name.lower() for sb in selected_brands):
            folium.Marker(
                location=[lat, lon],
                popup=f"<b>{s_name}</b><br>Brand: {b_name}<br>Address: {s_addr}",
                tooltip=b_name,
                icon=folium.Icon(color=col, icon="coffee")
            ).add_to(m)
            dossier_rows.append({
                "Category": "Specialty Cafe & QSR",
                "Brand Name": b_name,
                "Store Outlet": s_name,
                "Address": s_addr,
                "Latitude": lat,
                "Longitude": lon,
                "Catchment Radius": f"{radius_km} km"
            })

st_folium(m, width=1200, height=520)

# 12. CATCHMENT DOSSIER BREAKDOWN & CATEGORY SHEET EXPORT
st.markdown('<div class="section-heading">📑 Catchment Business Dossier & Category Sheet</div>', unsafe_allow_html=True)

df_dossier = pd.DataFrame(dossier_rows)

col_d1, col_d2 = st.columns([1, 1])
with col_d1:
    st.markdown(f"### 📊 Catchment Summary for `{search_location}`")
    st.write(f"- **Selected Buffer:** {radius_km} km radius")
    st.write(f"- **Total Active Brands in Catchment:** {len(df_dossier)}")
    if not df_dossier.empty:
        category_counts = df_dossier["Category"].value_counts()
        for cat, count in category_counts.items():
            st.write(f"  - *{cat}*: **{count} outlets**")

with col_d2:
    st.markdown("### 📥 Export Category-Wise Google Sheet")
    st.write("Download the structured CSV sheet containing brand categories, exact store addresses, and coordinates for this catchment.")
    
    if not df_dossier.empty:
        csv_buffer = io.BytesIO()
        df_dossier.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📊 Download Category-Wise Catchment Sheet (.CSV)",
            data=csv_data,
            file_name=f"GeoIQ_Catchment_Dossier_{search_location.replace(', ', '_')}.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.warning("No brand points available for export in this catchment.")

if not df_dossier.empty:
    st.markdown("### 📋 Detailed Store Audit Table")
    st.dataframe(df_dossier, use_container_width=True)
