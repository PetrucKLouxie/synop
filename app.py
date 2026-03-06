import streamlit as st
import requests
import re
import numpy as np
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Wind Compass Jawa Timur", layout="wide")

# refresh setiap 60 detik
st_autorefresh(interval=60000, key="refresh")

stations = {
    "Juanda": "WARR",
    "Banyuwangi": "WADY",
    "Malang": "WARA",
    "Trunojoyo": "WATR",
    "Bawean": "WBAW",
    "Kalianget": "WIMA",
    "Pacitan": "WARP",
    "Tuban": "WBTB",
    "Nganjuk": "WING",
    "Sumenep": "WIAS",
    "Kediri": "WIDK"
}

# =========================
# GET METAR NOAA TXT
# =========================

def get_wind(station):

    url=f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{station}.TXT"

    try:

        r=requests.get(url,timeout=10)

        lines=r.text.split("\n")

        metar=lines[1]

        wind=re.search(r"(\d{3})(\d{2})KT",metar)

        if wind:

            direction=int(wind.group(1))
            speed=int(wind.group(2))

            return direction,speed

        else:

            return None,None

    except:

        return None,None


# =========================
# WIND COMPASS
# =========================

def wind_compass(direction,speed,title):

    rad=np.radians(direction)

    x=np.cos(rad)
    y=np.sin(rad)

    fig=go.Figure()

    # lingkaran kompas
    theta=np.linspace(0,2*np.pi,200)

    fig.add_trace(go.Scatter(
        x=np.cos(theta),
        y=np.sin(theta),
        mode="lines",
        line=dict(width=3,color="white")
    ))

    # panah arah angin
    fig.add_trace(go.Scatter(
        x=[0,x],
        y=[0,y],
        mode="lines+markers",
        line=dict(width=6,color="cyan"),
        marker=dict(size=12)
    ))

    fig.update_layout(
        title=f"{title}<br>{speed} kt",
        height=300,
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="white")
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    return fig


# =========================
# DASHBOARD
# =========================

st.title("🌬️ Wind Compass Monitoring Jawa Timur")

cols=st.columns(3)

i=0

for name,code in stations.items():

    direction,speed=get_wind(code)

    with cols[i%3]:

        if direction is not None:

            st.plotly_chart(
                wind_compass(direction,speed,name),
                use_container_width=True
            )

            st.caption(f"Direction : {direction}° | Speed : {speed} kt")

        else:

            st.error("No METAR data")

    i+=1
