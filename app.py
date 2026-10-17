import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

st.set_page_config(page_title="NBC Expansion Engine | Bring on the Buzz", layout="wide")

# Custom CSS for NBC Website Look (Fixed Outer Frame, Scalloped Corners, Fonts & Colors)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;900&display=swap');

/* Fixed Outer Frame like NBC Website that stays constant on scroll */
.stApp {
    background-color: #1660C7;
    padding: 18px;
}

.main .block-container {
    background-color: #F4F8FB;
    border-radius: 36px;
    border: 4px solid #1660C7;
    box-shadow: inset 0 0 0 6px #FFFFFF, 0 12px 35px rgba(0,0,0,0.25);
    padding: 2.5rem 3rem !important;
    max-width: 96% !important;
    margin-top: 10px;
    margin-bottom: 20px;
    font-family: 'Montserrat', sans-serif;
}

/* Red Marquee Top Bar */
.red-ticker {
    background-color: #E53935;
    color: #FFFFFF;
    padding: 10px 20px;
    font-weight: 800;
    font-size: 14px;
    text-align: center;
    letter-spacing: 1.5px;
    border-radius: 12px;
    margin-bottom: 25px;
    text-transform: uppercase;
    box-shadow: 0 4px 10px rgba(229, 57, 53, 0.3);
}

/* Hero Banner */
.hero-box {
    background: linear-gradient(180deg, #FFFFFF 0%, #EBF3FA 100%);
    padding: 30px 20px;
    border-radius: 28px;
    border: 3px solid #1660C7;
    text-align: center;
    margin-bottom: 25px;
    position: relative;
}

.main-title {
    font-size: 54px;
    font-weight: 900;
    color: #1660C7;
    letter-spacing: 1px;
    margin-bottom: 5px;
    text-transform: uppercase;
    line-height: 1.1;
}

.sub-title {
    font-size: 18px;
    font-weight: 700;
    color: #334E68;
    margin-bottom: 15px;
}

/* Mascot & Stats Strip (Exact NBC Website Style) */
.nbc-stats-wrapper {
    background-color: #EBF3FA;
    border: 3px solid #1660C7;
    border-radius: 28px;
    padding: 25px 15px 15px 15px;
    margin: 25px 0;
    box-shadow: 0 8px 20px rgba(22, 96, 199, 0.1);
}

.stat-num-red {
    font-size: 40px;
    font-weight: 900;
    color: #E53935;
    line-height: 1;
    text-align: center;
}

.stat-num-blue {
    font-size: 40px;
    font-weight: 900;
    color: #1660C7;
    line-height: 1;
    text-align: center;
}

.stat-label-blue {
    font-size: 14px;
    font-weight: 800;
    color: #1660C7;
    text-transform: uppercase;
    margin-top: 8px;
    letter-spacing: 0.8px;
    text-align: center;
}

.stat-label-red {
    font-size: 14px;
    font-weight: 800;
    color: #E53935;
    text-transform: uppercase;
    margin-top: 8px;
    letter-spacing: 0.8px;
    text-align: center;
}

/* Blue Section Banner like 'ESPRESSO IS READY ARE YOU?' */
.blue-wave-section {
    background-color: #1660C7;
    color: #FFFFFF;
    padding: 35px 25px;
    border-radius: 28px;
    text-align: center;
    margin: 30px 0;
    border: 3px solid #FFFFFF;
    box-shadow: 0 8px 25px rgba(22, 96, 199, 0.25);
}

.blue-wave-title {
    font-size: 44px;
    font-weight: 900;
    color: #FFFFFF;
    text-transform: uppercase;
    line-height: 1.1;
    margin-bottom: 12px;
}

.stay-unfiltered-badge {
    background-color: #E53935;
    color: #FFFFFF;
    padding: 6px 18px;
    font-weight: 900;
    border-radius: 8px;
    display: inline-block;
    transform: rotate(-3deg);
    font-size: 16px;
    margin-bottom: 15px;
    letter-spacing: 1px;
}

/* BD Team Card */
.team-banner {
    background-color: #1660C7;
    color: white;
    padding: 25px;
    border-radius: 24px;
    margin-bottom: 25px;
    box-shadow: 0 6px 18px rgba(22, 96, 199, 0.2);
}

.team-pill {
    background-color: rgba(255, 255, 255, 0.15);
    border: 1.5px solid rgba(255, 255, 255, 0.5);
    padding: 10px 18px;
    border-radius: 12px;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 15px;
    margin-bottom: 10px;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# Sidebar with BD Team & Vipin Singh's Photo
with st.sidebar:
    st.image("https://nothingbeforecoffee.com/wp-content/uploads/2024/11/About-Us-NBC.png", width=120)
    st.markdown("### 🚀 NBC Expansion Engine")
    st.markdown("**Strategic Growth & Catchment Map**")
    st.markdown("---")
    
    st.markdown("#### 👥 Business Development & Expansion Team")
    st.image(
        "https://raw.githubusercontent.com/sanskar2233/nbc-expansion-map/main/WhatsApp%20Image%202026-10-18%20at%204.16.48%20AM.jpeg",
        caption="Vipin Singh Shekhawat (BD Manager)",
        width=160
    )
    st.markdown("""
    * **Vipin Singh Shekhawat** *(BD Manager)*
    * **Manoj Singh** *(BD Manager)*
    * **Mayank Iktiyan** *(BD & Expansion)*
    * **Sanskar Singh Yadav** *(BD & Expansion)*
    """)
    st.markdown("---")
    
    phases = [
        "Phase 1 (150 stores)",
        "Phase 2 (250 stores)",
        "Phase 3 (500 stores)",
        "Phase 4 (750 stores)",
        "Phase 5 (1000 stores)"
    ]
    selected_phases = st.multiselect("Select Expansion Phase", phases, default=phases)

# Top Header & Hero Section
h_col1, h_col2 = st.columns([1, 5])
with h_col1:
    st.image("https://nothingbeforecoffee.com/wp-content/uploads/2024/11/About-Us-NBC.png", width=130)
with h_col2:
    st.markdown("""
    <div class="hero-box">
        <div class="main-title">BRING ON THE BUZZ</div>
        <div class="sub-title">Nothing Before Coffee (NBC) — Next 1000 Stores Strategic Catchment & Expansion Engine</div>
        <div class="red-ticker">
            ★ HIGH QUALITY COFFEE • BUDGET FRIENDLY PRICES • ZERO COMPROMISE • EST. 2017 JAIPUR • BRING ON THE BUZZ ★
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main BD Team Highlight Box with Vipin's Photo
st.markdown('<div class="team-banner">', unsafe_allow_html=True)
t_col1, t_col2 = st.columns([1, 4])
with t_col1:
    st.image(
        "https://raw.githubusercontent.com/sanskar2233/nbc-expansion-map/main/WhatsApp%20Image%202026-10-18%20at%204.16.48%20AM.jpeg",
        width=130
    )
with t_col2:
    st.markdown("<h4 style='color: #FFD54F; margin-top: 0;'>🚀 BUSINESS DEVELOPMENT & EXPANSION TEAM</h4>", unsafe_allow_html=True)
    st.markdown("""
    <div class="team-pill">👤 Vipin Singh Shekhawat (BD Manager)</div>
    <div class="team-pill">👤 Manoj Singh (BD Manager)</div><br>
    <div class="team-pill">👤 Mayank Iktiyan (BD & Expansion)</div>
    <div class="team-pill">👤 Sanskar Singh Yadav (BD & Expansion)</div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Cartoon Characters + 110 Outlets | 20 Cities | 1,00,000+ Cups | 2,50,000+ Customers Section
st.markdown('<div class="nbc-stats-wrapper">', unsafe_allow_html=True)
c_left, s1, s2, s3, s4, c_right = st.columns([1.3, 1.5, 1.3, 2, 2, 1.3])

with c_left:
    st.image("https://nothingbeforecoffee.com/wp-content/themes/damnperfect/assets/images/hero-left.webp", use_container_width=True)

with s1:
    st.markdown('<div style="padding-top:25px;"><div class="stat-num-red">110+</div><div class="stat-label-blue">OUTLETS</div></div>', unsafe_allow_html=True)

with s2:
    st.markdown('<div style="padding-top:25px;"><div class="stat-num-blue">20</div><div class="stat-label-red">CITIES</div></div>', unsafe_allow_html=True)

with s3:
    st.markdown('<div style="padding-top:25px;"><div class="stat-num-red">1,00,000+</div><div class="stat-label-blue">CUPS SERVED</div></div>', unsafe_allow_html=True)

with s4:
    st.markdown('<div style="padding-top:25px;"><div class="stat-num-blue">2,50,000+</div><div class="stat-label-red">HAPPY CUSTOMERS</div></div>', unsafe_allow_html=True)

with c_right:
    st.image("https://nothingbeforecoffee.com/wp-content/themes/damnperfect/assets/images/hero-right.webp", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# NBC Website Styled Blue Banner Section
st.markdown("""
<div class="blue-wave-section">
    <div class="stay-unfiltered-badge">STAY UNFILTERED</div>
    <div class="blue-wave-title">ESPRESSO IS READY.<br>ARE YOU?</div>
    <p style="font-size: 16px; font-weight: 600; max-width: 750px; margin: 0 auto; opacity: 0.95;">
        High quality coffee. Budget friendly prices. Zero compromise.<br>
        At NBC, coffee is not just a beverage. It is a ritual. A mood. A pre-work boost. A late-night companion.
    </p>
</div>
""", unsafe_allow_html=True)

# Map & Data Processing
geolocator = Nominatim(user_agent="nbc_expansion_app")

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
    dfs = []
    try:
        df_csv = pd.read_csv("Delhi NCR Coffee Chains Store Locations - ALL Brands Data.csv", encoding='latin1')
        dfs.append(df_csv)
    except Exception:
        pass
    try:
        df_excel = pd.read_excel("All cafe data (1).xlsx")
        dfs.append(df_excel)
    except Exception:
        pass
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return None

st.markdown("### 📍 NEXT 1000 STORES CATCHMENT & EXPANSION MAP")

try:
    df = load_and_process_data()
    if df is None or df.empty:
        st.warning("Data files load nahi ho paayi. Please check karein ki CSV file repo mein sahi naam se hai.")
    else:
        lat_col = next((c for c in df.columns if c.strip().lower() in ['latitude', 'lat']), None)
        lon_col = next((c for c in df.columns if c.strip().lower() in ['longitude', 'lon', 'long']), None)
        addr_col = next((c for c in df.columns if 'address' in c.strip().lower() or 'location' in c.strip().lower()), None)
        name_col = next((c for c in df.columns if 'name' in c.strip().lower() or 'store' in c.strip().lower() or 'brand' in c.strip().lower()), None)
        city_col = next((c for c in df.columns if 'city' in c.strip().lower() or 'location' in c.strip().lower()), None)

        if (not lat_col or not lon_col) and addr_col:
            st.info("Fetching coordinates from addresses...")
            coords = df[addr_col].apply(get_coordinates)
            df['Latitude'] = [c[0] for c in coords]
            df['Longitude'] = [c[1] for c in coords]
            lat_col, lon_col = 'Latitude', 'Longitude'
            df = df.dropna(subset=[lat_col, lon_col])

        total_stores = len(df)
        progress = min(total_stores / 1000, 1.0)
        st.write(f"**Expansion Pipeline Progress:** {total_stores} / 1000 Target Stores")
        st.progress(progress)

        if city_col and city_col in df.columns:
            st.subheader("📊 City-wise Store Distribution")
            city_distribution = df[city_col].value_counts().reset_index()
            city_distribution.columns = ['City', 'Store Count']
            st.bar_chart(city_distribution.set_index('City'))

        m = folium.Map(location=[28.6139, 77.2090], zoom_start=10, tiles="OpenStreetMap")

        if lat_col and lon_col:
            for _, comp in df.iterrows():
                lat = comp.get(lat_col)
                lon = comp.get(lon_col)
                if pd.notna(lat) and pd.notna(lon):
                    store_title = str(comp.get(name_col, "NBC Target Store"))
                    popup_html = f"""
                    <div style='width: 170px; font-family: Montserrat, sans-serif;'>
                        <b style='color: #1660C7;'>{store_title}</b><br>
                        <span style='color: #E53935; font-size: 12px; font-weight: bold;'>NBC Catchment Zone</span>
                    </div>
                    """
                    folium.Marker(
                        location=[float(lat), float(lon)],
                        popup=folium.Popup(popup_html, max_width=220),
                        tooltip=store_title,
                        icon=folium.Icon(color='blue', icon='coffee', prefix='fa')
                    ).add_to(m)

        st_folium(m, width=1150, height=550)

except Exception as e:
    st.error(f"Error loading CSV/Map data: {e}")
