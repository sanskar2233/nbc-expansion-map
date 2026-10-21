import streamlit as st
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
    .buzz-title {
        font-size: 64px; font-weight: 900; color: #0052CC;
        letter-spacing: 2px; text-transform: uppercase; margin: 10px 0 5px 0;
    }
    .buzz-subtitle { font-size: 18px; font-weight: 700; color: #333333; margin-bottom: 12px; }
    .nbc-red-ticker {
        background-color: #E63946; color: #FFFFFF; padding: 12px 20px;
        font-weight: 800; font-size: 14px; text-align: center; text-transform: uppercase;
        border-radius: 0 0 12px 12px; margin-top: -8px; margin-bottom: 20px;
    }
    .bd-team-banner {
        background-color: #0052CC; color: #FFFFFF; padding: 16px 25px;
        border-radius: 12px; margin-bottom: 25px; display: flex; flex-wrap: wrap;
        justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0, 82, 204, 0.2);
    }
    .bd-team-title { font-size: 15px; font-weight: 800; text-transform: uppercase; color: #FFD166; }
    .bd-members { font-size: 15px; font-weight: 700; color: #FFFFFF; }
    .bd-badge {
        background-color: rgba(255, 255, 255, 0.18); padding: 6px 12px;
        border-radius: 20px; margin: 2px 4px; display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }
    .stat-card {
        background-color: #FFFFFF; border-bottom: 4px solid #0052CC;
        border-radius: 12px; padding: 18px 10px; text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin-bottom: 20px;
    }
    .stat-number { font-size: 36px; font-weight: 900; color: #E63946; line-height: 1.1; }
    .stat-label { font-size: 14px; font-weight: 800; color: #0052CC; text-transform: uppercase; margin-top: 6px; }
    .section-heading {
        font-size: 26px; font-weight: 900; color: #0052CC; text-transform: uppercase;
        margin: 30px 0 15px 0; border-left: 6px solid #E63946; padding-left: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 4. Top Header
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

# 5. Team Banner
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

# 6. Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="stat-card"><div class="stat-number">110+</div><div class="stat-label">Outlets</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="stat-card"><div class="stat-number">15+</div><div class="stat-label">Cities</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="stat-card"><div class="stat-number">1,00,000+</div><div class="stat-label">Cups Served</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="stat-card"><div class="stat-number">2,50,000+</div><div class="stat-label">Happy Customers</div></div>', unsafe_allow_html=True)

# 7. Data Loader (Reading from uploaded Excel file)
@st.cache_data(show_spinner=False)
def load_and_process_data():
    dfs = []
    try:
        excel_file = "Delhi NCR Coffee Chains Store Locations (4).xlsx"
        xls = pd.ExcelFile(excel_file)
        for sheet in xls.sheet_names:
            temp_df = pd.read_excel(excel_file, sheet_name=sheet)
            if not temp_df.empty:
                dfs.append(temp_df)
    except Exception:
        pass

    if dfs:
        df = pd.concat(dfs, ignore_index=True)
    else:
        return None, None, None, None, None, None

    lat_col = next((c for c in df.columns if c.strip().lower() in ['latitude', 'lat']), None)
    lon_col = next((c for c in df.columns if c.strip().lower() in ['longitude', 'lon', 'long']), None)
    addr_col = next((c for c in df.columns if 'address' in c.strip().lower() or 'location' in c.strip().lower() or 'market' in c.strip().lower()), None)
    name_col = next((c for c in df.columns if 'name' in c.strip().lower() or 'store' in c.strip().lower() or 'city' in c.strip().lower()), None)
    brand_col = next((c for c in df.columns if 'brand' in c.strip().lower() or 'group' in c.strip().lower()), None)

    if lat_col and lon_col:
        df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
        df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
        df = df.dropna(subset=[lat_col, lon_col])

    return df, lat_col, lon_col, addr_col, name_col, brand_col

# 8. Sidebar Filters for Key Highlighted Brands
with st.sidebar:
    st.image(NBC_LOGO, width=110)
    st.markdown("### 🎯 Highlight Competitor & Brand Filters")
    
    target_brands = [
        "Nothing Before Coffee", 
        "Blue Tokai", 
        "Third Wave Coffee", 
        "Starbucks", 
        "Domino's", 
        "Lenskart", 
        "Zudio"
    ]
    selected_brands = st.multiselect("Select Brands to Highlight:", target_brands, default=target_brands)
    st.markdown("---")
    st.markdown("**BD Leadership Team:**\n- Vipin Singh Shekhawat\n- Manoj Singh\n- Mayank Iktiyan\n- Sanskar Singh Yadav")

# 9. Interactive Google Maps Catchment Section
st.markdown('<div class="section-heading">India Key Brands Catchment & Expansion Map</div>', unsafe_allow_html=True)

# Google Maps tile integration
m = folium.Map(
    location=[28.6139, 77.2090], 
    zoom_start=6, 
    tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', 
    attr='Google'
)

# Brand color mapping function for distinct highlights
def get_brand_color(brand_name):
    b = str(brand_name).lower()
    if 'nothing before' in b or 'nbc' in b:
        return 'darkblue'
    elif 'blue tokai' in b:
        return 'cadetblue'
    elif 'third wave' in b:
        return 'orange'
    elif 'starbucks' in b:
        return 'green'
    elif 'domino' in b:
        return 'red'
    elif 'lenskart' in b:
        return 'purple'
    elif 'zudio' in b:
        return 'pink'
    return 'gray'

try:
    df, lat_col, lon_col, addr_col, name_col, brand_col = load_and_process_data()

    if df is not None and not df.empty and lat_col and lon_col:
        # Filter by selected brands if brand column exists
        if brand_col and selected_brands:
            filtered_df = df[df[brand_col].astype(str).apply(lambda x: any(b.lower() in x.lower() for b in selected_brands))]
            if filtered_df.empty:
                filtered_df = df
        else:
            filtered_df = df

        for comp in filtered_df.to_dict('records'):
            lat = comp.get(lat_col)
            lon = comp.get(lon_col)
            if pd.notna(lat) and pd.notna(lon):
                store_title = str(comp.get(name_col, "Store Location")) if name_col else "Store Location"
                store_brand = str(comp.get(brand_col, "Brand")) if brand_col else "Brand"
                store_addr = str(comp.get(addr_col, "")) if addr_col else ""

                marker_color = get_brand_color(store_brand)

                popup_html = f"""
                <div style='width: 210px; font-family: Montserrat, sans-serif;'>
                    <b style='color: #0052CC; font-size: 14px;'>{store_title}</b><br>
                    <span style='color: #E63946; font-weight: bold; font-size: 12px;'>Brand: {store_brand}</span><br>
                    <span style='font-size: 11px; color: #333;'>{store_addr}</span>
                </div>
                """
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=240),
                    tooltip=f"{store_brand} - {store_title}",
                    icon=folium.Icon(color=marker_color, icon="coffee" if "coffee" in store_brand.lower() else "tag")
                ).add_to(m)

        st_folium(m, width=1200, height=600)
    else:
        st.warning("Data could not be loaded properly from the spreadsheet.")

except Exception as e:
    st.error(f"Error loading map data: {e}")
