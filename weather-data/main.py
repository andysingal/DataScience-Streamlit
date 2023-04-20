import streamlit as st
import datetime,requests
from plotly import graph_objects as go
from utils import sidebar_bg

st.set_page_config(page_title="Weather Forecast",
                   page_icon="🌧",
                   menu_items={
                       'Get Help': "mailto:andysingal@gmail.com",
                       'Report a bug': "mailto:andysingal@gmail.com",
                       'About': "Weather App made with Streamlit."
                       })

st.title("8-DAY WEATHER FORECAST 🌧️🌥️")

city=st.text_input("ENTER THE NAME OF THE CITY ")

unit=st.selectbox("SELECT TEMPERATURE UNIT ",["Celsius","Fahrenheit"])

speed=st.selectbox("SELECT WIND SPEED UNIT ",["Metre/sec","Kilometre/hour"])

graph=st.radio("SELECT GRAPH TYPE ",["Bar Graph","Line Graph"])

if unit == "Celsius":
    temp_unit = " °C"
else:
    temp_unit = " °F"

if speed == "Kilometre/hour":
    wind_unit = " km/h"
else:
    wind_unit = " m/s"

api = "9b833c0ea6426b70902aa7a4b1da285c"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
response = requests.get(url)
x = response.json()