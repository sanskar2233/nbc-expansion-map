import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

st.set_page_config(page_title="NBC Expansion Engine | Bring on the Buzz", layout="wide")

st.markdown("""
<style>
/* Main Layout Styling */
.main { background-color: #FFFFFF; font-family: 'Montserrat', sans-serif; }
.main-title { font-size: 42px; font-weight: bold; color: #1660C7; margin-bottom: 5px; text-align: center; }
.sub-title { font-size: 20px; color: #4A6984; margin-bottom: 25px; text-align: center; }

/* Custom Wave Header Styling */
.wave-header { 
    background-image: linear-gradient(135deg, #CCE0FF 0%, #FFFFFF 100%);
    padding: 40px; 
    border-radius: 50px 50px 20px 20px; 
    border-bottom: 5px solid #1660C7;
    margin-bottom: 30px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}

.metric-container { 
    background-color: #FFFFFF; 
    padding: 20px; 
    border-radius: 15px; 
    border: 2px solid #EBF2F9;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.metric-value { font-size: 32px; font-weight: bold; color: #E54A4A; }
.metric-label { font-size: 14px; font-weight: bold; color: #1660C7; text-transform: uppercase; margin-top: 5px; }

.team-box { background-color: #e6f0fa; padding: 15px; border-radius: 15px; margin-top: 20px; margin-bottom: 10px; border-left: 5px solid #1660C7; }
.stat-box { font-weight: bold; color: #1660C7; font-size: 18px; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    st.markdown('<div class="stat-box">• NBC Expansion •</div>', unsafe_allow_html=True)
    st.markdown('Strategic Growth Map')
    st.markdown("---")
    
    if not st.session_state.logged_in:
        st.subheader("🔒 Employee Login")
        emp_id = st.text_input("Employee ID / Username", placeholder="sanskar@nbc")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if emp_id.strip().lower() == "sanskar@nbc" and password == "NBC_team_2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Employee ID or Password")
    else:
        st.success("✅ Logged in as: sanskar@nbc")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
        st.markdown('<div class="team-box"><b>Business Development & Expansion Team</b><br><small>(Click on a name to view profile)</small></div>', unsafe_allow_html=True)
        
        with st.expander("👤 Vipin Singh Shekhawat (BD Manager)"):
            st.image("https://raw.githubusercontent.com/sanskar2233/nbc-expansion-map/main/WhatsApp%20Image%202026-10-18%20at%204.16.48%20AM.jpeg", width=150)
            st.caption("BD Manager - Nothing Before Coffee")
        
        with st.expander("👤 Manoj Singh (BD Manager)"):
            st.caption("BD Manager - Nothing Before Coffee")
             
        with st.expander("👤 Mayank Iktiyan (BD & Expansion)"):
            st.image("https://media.licdn.com/dms/image/v2/D5603AQHz626IIqkTwg/profile-displayphoto-scale_200_200/B56ZkI2jvGHcAc-/0/1756790144972?e=1793836800&v=beta&t=ydEZyJSU7IgMIgD-IAUMasQV2vF2qQOIEW_-s6Jg-dE", width=150)
            st.caption("BD & Expansion - Nothing Before Coffee")

        with st.expander("👤 Sanskar Singh Yadav (BD & Expansion)"):
            st.image("https://media.licdn.com/dms/image/v2/D5603AQGLFnKYfzwXsg/profile-displayphoto-crop_800_800/B56Z3eEcL2IUAI-/0/1777547205499?e=1793836800&v=beta&t=TTtIjmFD5qAWQwAUcxOe5zNrdXEC_VV8eyPD563w1pw", width=150)
            st.caption("BD & Expansion - Nothing Before Coffee")
        
        st.markdown("---")
        phases = ["Phase 1 (150 stores)", "Phase 2 (250 stores)", "Phase 3 (500 stores)", "Phase 4 (750 stores)", "Phase 5 (1000 stores)"]
        selected_phases = st.multiselect("Select Expansion Phase", phases, default=phases)

# Main Dashboard Content (Only visible after login)
if st.session_state.logged_in:
    # Wavy Header Section with Mascots
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.image("https://nothingbeforecoffee.com/wp-content/themes/damnperfect/assets/images/hero-left.webp")
    with col2:
        st.markdown('''
        <div class="wave-header">
            <div class="main-title">Bring on the Buzz</div>
            <div class="sub-title">Business Development Next 1000 Stores Catchment Strategy</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.image("https://nothingbeforecoffee.com/wp-content/themes/damnperfect/assets/images/hero-right.webp")

    # Metric Cards Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown('<div class="metric-container"><div class="metric-value">110+</div><div class="metric-label">Outlets</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown('<div class="metric-container"><div class="metric-value">20</div><div class="metric-label">Cities</div></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown('<div class="metric-container"><div class="metric-value">1,00,000+</div><div class="metric-label">Cups Served</div></div>', unsafe_allow_html=True)
    with m_col4:
        st.markdown('<div class="metric-container"><div class="metric-value">2,50,000+</div><div class="metric-label">Happy Customers</div></div>', unsafe_allow_html=True)

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
            st.warning("Data files load nahi ho paayi. Kripya check karein ki CSV/Excel files GitHub par sahi naam se uploaded hain.")
        else:
            lat_col = next((c for c in df.columns if c.strip().lower() in ['latitude', 'lat']), None)
            lon_col = next((c for c in df.columns if c.strip().lower() in ['longitude', 'lon', 'long']), None)
            addr_col = next((c for c in df.columns if 'address' in c.strip().lower() or 'location' in c.strip().lower()), None)
            name_col = next((c for c in df.columns if 'name' in c.strip().lower() or 'store' in c.strip().lower() or 'brand' in c.strip().lower()), None)
            city_col = next((c for c in df.columns if 'city' in c.strip().lower() or 'location' in c.strip().lower()), None)
            phase_col = next((c for c in df.columns if 'phase' in c.strip().lower()), None)

            if not lat_col or not lon_col:
                if addr_col:
                    st.info("Fetching coordinates from addresses...")
                    coords = df[addr_col].apply(get_coordinates)
                    df['Latitude'] = [c[0] for c in coords]
                    df['Longitude'] = [c[1] for c in coords]
                    lat_col, lon_col = 'Latitude', 'Longitude'
                    df = df.dropna(subset=[lat_col, lon_col])

            filtered_df = df
            if phase_col and selected_phases:
                filtered_df = df[df[phase_col].astype(str).isin([p.split(' ')[1] for p in selected_phases])]
                if filtered_df.empty:
                    filtered_df = df

            if city_col and city_col in filtered_df.columns:
                city_distribution = filtered_df[city_col].value_counts().reset_index()
                city_distribution.columns = ['City', 'Store Count']
                st.subheader("City-wise Store Distribution")
                st.bar_chart(city_distribution.set_index('City'))

            st.subheader("📍 Strategic Catchment & Expansion Map")
            m = folium.Map(location=[28.4595, 77.0266], zoom_start=11, tiles="OpenStreetMap")
            
            if lat_col and lon_col:
                nbc_stores = filtered_df.to_dict('records')
                for comp in nbc_stores:
                    lat = comp.get(lat_col)
                    lon = comp.get(lon_col)
                    if pd.notna(lat) and pd.notna(lon):
                        store_title = str(comp.get(name_col, "Store")) if name_col else "Store"
                        popup_html = f"""
                        <div style='width: 160px;'>
                        <b>{store_title}</b><br>
                        NBC Target Catchment
                        </div>
                        """
                        icon_color = 'green' if comp.get(city_col) == "Standard" else 'red'
                        folium.Marker(
                            location=[float(lat), float(lon)],
                            popup=folium.Popup(popup_html, max_width=200),
                            tooltip=store_title,
                            icon=folium.Icon(color=icon_color)
                        ).add_to(m)

            st_folium(m, width=1100, height=600)
    except Exception as e:
        st.error(f"Error loading CSV/Map data: {e}")
else:
    # Lock screen message on main page before login
    st.markdown('''
    <div class="wave-header" style="margin-top: 40px;">
        <div class="main-title">🔒 NBC Expansion Engine</div>
        <div class="sub-title">Please log in from the left sidebar using your Employee ID and Password to access the catchment map.</div>
    </div>
    ''', unsafe_allow_html=True)
