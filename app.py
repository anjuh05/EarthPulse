
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(
    page_title="EarthPulse",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f0f7f4;
}
.title {
    text-align: center;
    color: #087f5b;
    font-size: 45px;
    font-weight: bold;
}
.hero {
    background: linear-gradient(120deg,#087f5b,#087eaa);
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border-left: 4px solid #087f5b;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌍 EarthPulse</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h2>Explore Earth's Climate</h2>
<p>Discover temperature and rainfall patterns using NASA satellite data.</p>
</div>
""", unsafe_allow_html=True)

locations = {
    "Kochi, Kerala": (9.9312, 76.2673),
    "Thrissur, Kerala": (10.5276, 76.2144),
    "Ernakulam, Kerala": (9.9816, 76.2999),
    "Thiruvananthapuram, Kerala": (8.5241, 76.9366),
    "Kozhikode, Kerala": (11.2588, 75.7804),
    "Palakkad, Kerala": (10.7867, 76.6548),
    "Bengaluru, Karnataka": (12.9716, 77.5946),
    "Chennai, Tamil Nadu": (13.0827, 80.2707),
    "Mumbai, Maharashtra": (19.0760, 72.8777),
    "Delhi, India": (28.6139, 77.2090),
    "Hyderabad, Telangana": (17.3850, 78.4867),
    "Kolkata, West Bengal": (22.5726, 88.3639)
}

@st.cache_data(ttl=86400)
def get_data(latitude, longitude, start, end):

    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"

    params = {
        "parameters": "T2M,PRECTOTCORR",
        "community": "RE",
        "longitude": longitude,
        "latitude": latitude,
        "start": start.strftime("%Y"),
        "end": end.strftime("%Y"),
        "format": "JSON"
    }

    response = requests.get(url, params=params, timeout=35)
    response.raise_for_status()

    result = response.json()
    data = result["properties"]["parameter"]

    temperature = data["T2M"]
    rainfall = data["PRECTOTCORR"]

    df = pd.DataFrame({
        "Date": list(temperature.keys()),
        "Temperature (°C)": list(temperature.values()),
        "Rainfall": list(rainfall.values())
    })

    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m")

    df["Temperature (°C)"] = pd.to_numeric(
        df["Temperature (°C)"], errors="coerce"
    )

    df["Rainfall"] = pd.to_numeric(
        df["Rainfall"], errors="coerce"
    )

    df = df.replace([-999, -999.0], pd.NA).dropna()

    return df


st.sidebar.header("🌍 Climate Explorer")

location = st.sidebar.selectbox(
    "Select Location",
    list(locations.keys())
)

period = st.sidebar.selectbox(
    "Select Period",
    ["Last 30 days", "Last 6 months", "Last 1 year", "Last 5 years"]
)

periods = {
    "Last 30 days": 30,
    "Last 6 months": 180,
    "Last 1 year": 365,
    "Last 5 years": 1825
}

search = st.sidebar.button(
    "🔍 Explore Climate",
    use_container_width=True
)

if search:

    latitude, longitude = locations[location]

    end_date = date.today() - timedelta(days=45)
    start_date = end_date - timedelta(days=periods[period])

    try:

        with st.spinner(
            "🛰️ Connecting to NASA... Please wait while we retrieve climate data. This may take a little time."
        ):

            df = get_data(
                latitude,
                longitude,
                start_date,
                end_date
            )

        if df.empty:
            st.warning("No climate data available for this period.")

        else:
            df = df[
                (df["Date"].dt.date >= start_date) &
                (df["Date"].dt.date <= end_date)
            ]

            st.session_state["df"] = df
            st.session_state["location"] = location

            st.success("Climate data loaded successfully!")

    except requests.exceptions.Timeout:
        st.error("NASA is taking too long. Please try again.")

    except requests.exceptions.RequestException:
        st.error("Unable to connect to NASA. Check your internet connection.")

    except Exception as e:
        st.error(f"Error retrieving climate data: {e}")


if "df" in st.session_state:

    df = st.session_state["df"]

    st.markdown("---")
    st.header(f"📊 Climate Dashboard: {st.session_state['location']}")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Temperature",
        f"{df['Temperature (°C)'].mean():.1f} °C"
    )

    c2.metric(
        "Maximum Temperature",
        f"{df['Temperature (°C)'].max():.1f} °C"
    )

    c3.metric(
        "Total Rainfall",
        f"{df['Rainfall'].sum():.1f} mm"
    )

    st.subheader("🌡️ Temperature Analysis")

    fig1 = px.line(
        df,
        x="Date",
        y="Temperature (°C)",
        markers=True,
        title="Monthly Temperature Variation"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🌧️ Rainfall Analysis")

    fig2 = px.bar(
        df,
        x="Date",
        y="Rainfall",
        title="Monthly Rainfall Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 Climate Records")

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇️ Download Climate Data",
        df.to_csv(index=False),
        file_name="earthpulse_data.csv",
        mime="text/csv"
    )

else:

    st.info(
        "👈 Select a location and click Explore Climate to view NASA data."
    )

st.markdown("---")

st.markdown(
    "<center>🌍 EarthPulse | Powered by NASA POWER API</center>",
    unsafe_allow_html=True
)
