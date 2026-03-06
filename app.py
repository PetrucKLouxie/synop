import streamlit as st
import requests
from bs4 import BeautifulSoup
import numpy as np
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Wind SYNOP Jatim", layout="wide")

# refresh tiap 10 menit
st_autorefresh(interval=600000, key="refresh")

# =========================
# WMO STATION JAWA TIMUR
# =========================

stations = {
    "Juanda": 96935,
    "Banyuwangi": 96933,
    "Bawean": 96937,
    "Kalianget": 96973,
    "Malang": 96987,
    "Pacitan": 96925,
    "Trunojoyo": 96939,
    "Tuban": 96991,
    "Nganjuk": 96983,
    "Karangkates": 96989
}

# =========================
# GET SYNOP OGIMET
# =========================

def get_synop(wmo):

    url=f"https://ogimet.com/display_synops2.php?lang=en&lugar={wmo}"

    try:

        r=requests.get(url,timeout=10)

        soup=BeautifulSoup(r.text,"html.parser")

        table=soup.find("table")

        rows=table.find_all("tr")

        latest=rows[1].find_all("td")[-1].text

        return latest

    except:

        return None


# =========================
# PARSE WIND SYNOP
# =========================

def parse_wind(synop):

    try:

        groups=synop.split()

        wind=groups[2]

        direction=int(wind[1:3])*10
        speed=int(wind[3:5])

        return direction,speed

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

    theta=np.linspace(0,2*np.pi,200)

    # circle
    fig.add_trace(go.Scatter(
        x=np.cos(theta),
        y=np.sin(theta),
        mode="lines",
        line=dict(width=3,color="white")
    ))

    # arrow
    fig.add_trace(go.Scatter(
        x=[0,x],
        y=[0,y],
        mode="lines+markers",
        line=dict(width=6,color="cyan"),
        marker=dict(size=12)
    ))

    fig.update_layout(
        title=f"{title}<br>{speed} m/s",
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

st.title("🌬️ Wind Compass SYNOP Jawa Timur")

cols=st.columns(3)

i=0

for name,wmo in stations.items():

    synop=get_synop(wmo)

    direction,speed=parse_wind(synop)

    with cols[i%3]:

        if direction is not None:

            st.plotly_chart(
                wind_compass(direction,speed,name),
                use_container_width=True
            )

            st.caption(f"Direction : {direction}° | Speed : {speed} m/s")

        else:

            st.error("No SYNOP data")

    i+=1
