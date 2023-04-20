import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
from utils import *

st.set_page_config(page_title="Excel file",
                   page_icon="📈",
                   menu_items={
                       'Get Help': "mailto:andysingal@gmail.com",
                       'Report a bug': "mailto:andysingal@gmail.com",
                       'About': "An expense tracker app made with Streamlit."
                       })
st.title('Excel Plotter 📈')
st.subheader('Feed me with your Excel file')

uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)
    groupby_column = st.selectbox(
        'What would you like to analyse?',
        ('Ship Mode', 'Segment', 'Category', 'Sub-Category'),
    )
    # -- GROUP DATAFRAME
    output_columns = ['Sales', 'Profit']
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    # -- PLOT DATAFRAME
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y='Sales',
        color='Profit',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Sales & Profit by {groupby_column}</b>'
    )
    st.plotly_chart(fig)

    # -- DOWNLOAD SECTION
    st.subheader('Downloads:')
    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)