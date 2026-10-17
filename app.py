import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

st.set_page_config(page_title="NBC Expansion Engine | Bring on the Buzz", layout="wide")

# Custom CSS for NBC Website Look
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap');

.stApp {
    background-color: #1660C7;
    font-family: 'Montserrat', sans-serif;
}

/* White Scalloped / Rounded Card Banner */
.hero-box {
    background-color: #FFFFFF;
    padding: 35px 25px;
    border-radius: 35px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    margin-bottom: 25px;
    border: 4px solid #EBF2F9;
}
.main-title {
    font-size: 46px;
    font-weight: 900;
    color: #1660C7;
    letter-spacing: 1px;
    margin-bottom: 5px;
    text-transform: uppercase;
}
.sub-title {
    font-size: 18px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 15px;
}
.red-pill-banner {
    background-color: #E53935;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 13px;
    padding: 8px 20px;
    border-radius: 50px;
    display: inline-block;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

/* BD Team Section */
.team-header {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 800;
    text-transform: uppercase;
    margin-top: 15px;
    margin-bottom: 12px;
    letter-spacing: 0.5px;
}

/* Custom Styling for Team Expanders */
div[data-testid="stExpander"] {
    background-color: rgba(255, 255, 255, 0.12) !important;
    border: 2px solid rgba(255, 255, 255, 0.7) !important;
    border-radius: 30px !important;
    color: #FFFFFF !important;
    margin-bottom: 10px !important;
}
div[data-testid="stExpander"] summary p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}

/* Stats Section */
.stat-num-red {
    font-size: 38px;
    font-weight: 900;
    color: #FF3B30;
    text-align: center;
    line-height: 1.1;
}
.stat-label-red {
    font-size: 12px;
    font-weight: 800;
    color: #FF3B30;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 20px;
}

/* Blue Section Banner */
.blue-wave-section {
    background-color: #0D47A1;
    color: #FFFFFF;
    padding: 35px 20px;
    border-radius: 25px;
    text-align: center;
    margin: 25px 0;
    border: 2px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}
.stay-unfiltered-badge {
    background-color: #E53935;
    color: #FFFFFF;
    font-weight: 800;
    padding: 5px 16px;
    border-radius: 6px;
    display: inline-block;
    transform: rotate(-3deg);
    font-size: 13px;
    margin-bottom: 12px;
    letter-spacing: 1px;
}
.blue-wave-title {
    font-size: 34px;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1.15;
    margin-bottom: 12px;
    text-transform: uppercase;
}

/* Sidebar Styling */
.stat-box {
    font-size: 20px;
    font-weight: 900;
    color: #1660C7;
}
</style>
""", unsafe_allow_html=True)

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""

# Sidebar Login & Filters
with st.sidebar:
    st.markdown('<div class="stat-box">• NBC Expansion •</div>', unsafe_allow_html=True)
    st.caption("Strategic Growth Map")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        st.subheader("🔒 Employee Login")
        username = st.text_input("Employee ID / Username", placeholder="sanskar@nbc").strip().lower()
        password = st.text_input("Password", type="password").strip()
        
        if st.button("Login", use_container_width=True):
            valid_users = ["sanskar@nbc", "mayank@nbc", "vipin@nbc", "manoj@nbc"]
            valid_passwords = ["NBCteam2026", "NBC_team_2026", "nbcteam2026"]
            
            if username in valid_users and password in valid_passwords:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("Invalid Employee ID or Password")
    else:
        st.success(f"Logged in: {st.session_state.current_user}")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()
            
        st.markdown("---")
        phases = [
            "Phase 1 (150 stores)", 
            "Phase 2 (250 stores)", 
            "Phase 3 (500 stores)", 
            "Phase 4 (750 stores)", 
            "Phase 5 (1000 stores)"
        ]
        selected_phases = st.multiselect("Select Expansion Phase", phases, default=phases)

# Main Dashboard Content
if st.session_state.logged_in:
    st.markdown("""
    <div class="hero-box">
        <div class="main-title">BRING ON THE BUZZ</div>
        <div class="sub-title">Nothing Before Coffee (NBC) — Next 1000 Stores Strategic Catchment & Expansion Engine</div>
        <div class="red-pill-banner">• HIGH QUALITY COFFEE • BUDGET FRIENDLY PRICES • ZERO COMPROMISE • EST. 2017 JAIPUR • BRING ON THE BUZZ •</div>
    </div>
    """, unsafe_allow_html=True)

    # Founders & BD Team Section
    col_f, col_t = st.columns([1.2, 3.8])
    with col_f:
        st.image(
            "https://raw.githubusercontent.com/sanskar2233/nbc-expansion-map/main/WhatsApp%20Image%202026-10-18%20at%204.16.48%20AM.jpeg", 
            caption="Founders | Nothing Before Coffee", 
            use_container_width=True
        )
    with col_t:
        st.markdown('<div class="team-header">🚀 BUSINESS DEVELOPMENT & EXPANSION TEAM</div>', unsafe_allow_html=True)
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            with st.expander("Vipin Singh Shekhawat (BD Manager)"):
                st.image("https://raw.githubusercontent.com/sanskar2233/nbc-expansion-map/main/WhatsApp%20Image%202026-10-18%20at%204.16.48%20AM.jpeg", width=160)
            with st.expander("Mayank Iktiyan (BD & Expansion)"):
                st.image("https://media.licdn.com/dms/image/v2/D5603AQHzm90d5J6g-dE/profile-displayphoto-scale_200_200/B56ZkZlJVgH4-Ae-1793836800&e=1793836800&v=beta&t=TttJlmFD5QAWQwD0o63w1pw", width=160)
        with t_col2:
            with st.expander("Manoj Singh (BD Manager)"):
                st.write("**Manoj Singh** — BD Manager (NBC Expansion)")
            with st.expander("Sanskar Singh Yadav (BD & Expansion)"):
                st.image("https://media.licdn.com/dms/image/v2/D5603AQHzm90d5J6g-dE/profile-displayphoto-crop_800_800/B56Z3eEcl_2iS6jg-dE/profile-displayphoto-crop_800_800/B56Z3eEcl_2iS6j-dE/0/1793836800800?e=1793836800&v=beta&t=TttJlmFD5QAWQwD0o63w1pw", width=160)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.25);'>", unsafe_allow_html=True)

    # Cartoon Mascots & Stats Row
    c_left, s1, s2, s3, s4, c_right = st.columns([1.2, 1, 1, 1.2, 1.2, 1.2])
    with c_left:
        st.image("https://nothingbeforecoffee.com/wp-content/themes/damnperfect/assets/images/hero-left.webp", width=130)
    with s1:
        st.markdown('<div class="stat-num-red">110+</div><div class="stat-label-red">OUTLETS</div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="stat-num-red">20</div><div class="stat-label-red">CITIES</div>', unsafe_allow_html=True)
    with s3:
        st.markdown('<div class="stat-num-red">1,00,000+</div><div class="stat-label-red">CUPS SERVED</div>', unsafe_allow_html=True)
    with s4:
        st.markdown('<div class="stat-num-red">2,50,000+</div><div class="stat-label-red">HAPPY CUSTOMERS</div>', unsafe_allow_html=True)
    with c_right:
        st.image("https://nothingbeforecoffee.com/wp-content/themes/damnperfect/assets/images/hero-right.webp", width=130)

    # Blue Banner Section
    st.markdown("""
    <div class="blue-wave-section">
        <div class="stay-unfiltered-badge">STAY UNFILTERED</div>
        <div class="blue-wave-title">ESPRESSO IS READY.<br>ARE YOU?</div>
        <p style="font-size: 15px; font-weight: 600; max-width: 750px; margin: 0 auto; opacity: 0.95;">
            High quality coffee. Budget friendly prices. Zero compromise.<br>
            At NBC, coffee is not just a beverage. It is a ritual. A mood. A pre-work boost. A late-night companion.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Map & Catchment Section
    st.markdown('<div class="team-header">📍 NEXT 1000 STORES CATCHMENT & EXPANSION MAP</div>', unsafe_allow_html=True)

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

    try:
        df = load_and_process_data()
        if df is None or df.empty:
            st.warning("Data files load nahi ho paayi. Kripya GitHub repository mein CSV/Excel file names check karein.")
        else:
            lat_col = next((c for c in df.columns if c.strip().lower() in ['latitude', 'lat']), None)
            lon_col = next((c for c in df.columns if c.strip().lower() in ['longitude', 'lon', 'long']), None)
            addr_col = next((c for c in df.columns if 'address' in c.strip().lower() or 'location' in c.strip().lower()), None)
            name_col = next((c for c in df.columns if 'name' in c.strip().lower() or 'store' in c.strip().lower() or 'brand' in c.strip().lower()), None)
            city_col = next((c for c in df.columns if 'city' in c.strip().lower() or 'location' in c.strip().lower()), None)

            if not lat_col or not lon_col:
                if addr_col:
                    st.info("Fetching coordinates from addresses...")
                    coords = df[addr_col].head(50).apply(get_coordinates)
                    df = df.head(50).copy()
                    df['Latitude'] = [c[0] for c in coords]
                    df['Longitude'] = [c[1] for c in coords]
                    lat_col, lon_col = 'Latitude', 'Longitude'

            if lat_col and lon_col:
                df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
                df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
                filtered_df = df.dropna(subset=[lat_col, lon_col])

                m = folium.Map(location=[28.6139, 77.2090], zoom_start=11, tiles="OpenStreetMap")
                
                for _, comp in filtered_df.iterrows():
                    lat = comp.get(lat_col)
                    lon = comp.get(lon_col)
                    store_title = str(comp.get(name_col, "Coffee Store"))
                    popup_html = f"<div style='width: 160px;'><b>{store_title}</b><br>Catchment Marker</div>"
                    icon_color = 'blue' if 'nbc' in store_title.lower() or 'nothing before' in store_title.lower() else 'red'
                    
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_html, max_width=200),
                        tooltip=store_title,
                        icon=folium.Icon(color=icon_color, icon='info-sign')
                    ).add_to(m)

                st_folium(m, width=1200, height=550)
    except Exception as e:
        st.error(f"Error loading CSV/Map data: {e}")

else:
    st.markdown("""
    <div class="hero-box" style="margin-top: 40px;">
        <div class="main-title" style="font-size: 32px;">🔒 NBC Expansion Engine</div>
        <div class="sub-title">Please log in from the left sidebar using your Employee ID and Password to access the catchment map.</div>
    </div>
    """, unsafe_allow_html=True)
