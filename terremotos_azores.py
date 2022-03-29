# ----------------------------------------------
# DATOS:
# https://www.ipma.pt/en/geofisica/sismicidade/
# ----------------------------------------------

import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import datetime
import os


# Cargar datos:
df = pd.read_csv("Update_29-03-22.csv")
st.set_page_config(layout='wide')

# ----------------------------------------------
# TÍTULO
# ----------------------------------------------
fecha_inicio = df.iloc[-1,0]
dia_inicio = fecha_inicio[10:]
fecha_final= df.iloc[0,0]
dia_final = fecha_final[10:]
st.title("Terremotos en la Isla de San Jorge, Azores")
st.subheader(f"Datos de eventos sísmicos entre el: {fecha_inicio} y {fecha_final}")

# ----------------------------------------------
# SLIDERS:
# ----------------------------------------------
# Str a Timestamp
fecha_final = datetime.datetime.strptime(fecha_final, '%Y-%m-%d %H:%M:%S')
fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S')

rango=st.slider("Seleciona un rango de fechas:", min_value=fecha_inicio, max_value=fecha_final,
value= (fecha_inicio, fecha_final))
# Crear el df filtrado por fechas.
date_1= str(rango[0])
date_2 = str(rango[1])
df_dates = df[(df['date UTC'] >=date_1) & (df['date UTC']<=date_2)]


# ----------------------------------------------
# # MAPA
# ----------------------------------------------
st.markdown("El color indica la profundidad. El radio, la magnitud.")
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/satellite-v9', #'mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=38.68,
         longitude=-28.17,
         zoom=10.8,
         pitch=0,
     ),
     layers=[
         pdk.Layer(
    "ScatterplotLayer",
    df_dates,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=25,
    radius_min_pixels=5,
    radius_max_pixels=150,
    line_width_min_pixels=1,
    get_position="[lon, lat]",
    get_radius="mag*5",
    get_fill_color='[220-prof*4, 200/prof*4, 100+prof*6]',
    get_line_color=[0, 0, 0],
)]))
col_1, col_2 = st.columns(2)
# ----------------------------------------------
# # GRAFICOS SCATTER
# ----------------------------------------------

with col_1:
    st.subheader("Latitud-profundidad")
    Fig = px.scatter(df_dates, x="lat",y="prof", color="mag",size='mag',
        marginal_x = 'histogram')
    Fig.update_yaxes(autorange="reversed")
    Fig.update_layout(
        xaxis_title ="Latitud",
        yaxis_title = "Profundidad (Km)",
        font=dict(size=18)
    )
 
    st.plotly_chart(Fig)

with col_2:
    st.subheader("Longitud-profundidad")
    Fig_2 = px.scatter(df_dates, x="lon",y="prof", color="mag",size='mag',
        marginal_x = 'histogram')
    Fig_2.update_yaxes(autorange="reversed")
    Fig_2.update_layout(
        xaxis_title ="Longitud",
        yaxis_title = "Profundidad (Km)",
        font=dict(size=18)
    ) 
    st.plotly_chart(Fig_2)


# ----------------------------------------------
# # LINK 
# ----------------------------------------------
st.caption('Fuente de los datos:')
st.markdown('[Portuguese Institute for Sea and Atmosphere (IPMA)](https://www.ipma.pt/en/geofisica/sismicidade/)'
)
