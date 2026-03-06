import streamlit as st
import requests
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Wind Compass Jatim", layout="wide")

stations = {
    "Juanda":"WARR",
    "Banyuwangi":"WADY",
    "Malang":"WARA",
    "Trunojoyo":"WATR",
    "Bawean":"WBAW",
    "Kalianget":"WIMA",
    "Pacitan":"WARP",
    "Tuban":"WBTB",
    "Nganjuk":"WING",
    "Sumenep":"WIAS",
    "Kediri":"WIDK"
}

# =========================
# GET WIND DATA
# =========================

def get_wind(icao):

    url=f"https://aviationweather.gov/api/data/metar?ids={icao}&format=json"

    try:
        r=requests.get(url,timeout=10).json()

        if len(r)==0:
            return None,None

        direction=r[0]["wdir"]
        speed=r[0]["wspd"]

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

    # arrow
    fig.add_trace(go.Scatter(
        x=[0,x],
        y=[0,y],
        mode="lines+markers",
        line=dict(width=6),
        marker=dict(size=10),
    ))

    # compass circle
    theta=np.linspace(0,2*np.pi,200)
    fig.add_trace(go.Scatter(
        x=np.cos(theta),
        y=np.sin(theta),
        mode="lines",
        line=dict(width=2)
    ))

    fig.update_layout(
        title=f"{title}<br>{speed} kt",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=300,
        showlegend=False,
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    return fig


# =========================
# DASHBOARD
# =========================

st.title("🌬️ Wind Compass Jawa Timur")

cols=st.columns(3)

i=0

for name,icao in stations.items():

    direction,speed=get_wind(icao)

    with cols[i%3]:

        if direction is not None:

            st.plotly_chart(
                wind_compass(direction,speed,name),
                use_container_width=True
            )

            st.caption(f"Direction : {direction}° | Speed : {speed} kt")

        else:

            st.error("No data")

    i+=1
