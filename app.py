import streamlit as st
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go

st.set_page_config(page_title="BMKG Jatim Wind Monitor", layout="wide")

# =========================
# STATION WMO BMKG JATIM
# =========================

stations = {
    "Juanda":96933,
    "Banyuwangi":96935,
    "Bawean":96937,
    "Kalianget":96973,
    "Malang":96987,
    "Pacitan":96925,
    "Sumenep":96975,
    "Trunojoyo":96939,
    "Tuban":96991,
    "Nganjuk":96983,
    "Karangkates":96989
}

# =========================
# GET SYNOP FROM OGIMET
# =========================

def get_synop(wmo):

    url = f"https://ogimet.com/display_synops2.php?lang=en&lugar={wmo}&tipo=ALL"

    try:

        r = requests.get(url, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        pre = soup.find("pre")

        if pre:
            return pre.text

    except:
        return None


# =========================
# PARSE WIND
# =========================

def parse_wind(synop):

    try:

        groups = synop.split()

        wind = groups[2]

        direction = int(wind[1:3]) * 10
        speed = int(wind[3:5])

        return direction, speed

    except:

        return None, None


# =========================
# SPEEDOMETER GAUGE
# =========================

def wind_gauge(speed, title):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=speed,
        title={'text': title},
        gauge={
            'axis': {'range': [0,40]},
            'bar': {'color': "#00f2ff"},
            'steps': [
                {'range':[0,10],'color':"#00ff9f"},
                {'range':[10,20],'color':"#ffee00"},
                {'range':[20,30],'color':"#ff9900"},
                {'range':[30,40],'color':"#ff0000"}
            ]
        }
    ))

    fig.update_layout(height=250)

    return fig


# =========================
# UI
# =========================

st.title("🌬️ Wind Monitoring BMKG Jawa Timur")

cols = st.columns(3)

i = 0

for name,wmo in stations.items():

    synop = get_synop(wmo)

    direction,speed = parse_wind(synop)

    with cols[i % 3]:

        if speed is not None:

            st.plotly_chart(
                wind_gauge(speed,name),
                use_container_width=True
            )

            st.caption(f"Direction : {direction}°")

        else:

            st.error("Data tidak tersedia")

    i += 1
