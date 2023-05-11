import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import time
from utils import *

# st.set_page_config(layout='wide')

st.title('Streamlit Data Report Generator')

st.markdown('Use this Streamlit app to make your own scatterplot about Xeek and FORCE 2020!')

df = pd.read_csv('https://raw.githubusercontent.com/andymcdgeo/Petrophysics-Python-Series/master/'
                 'Data/Xeek_Well_15-9-15.csv')

with st.form('report'):
    st.write("### Report Details")
    col1, col2 = st.columns(2, gap='large')

    report_title = col1.text_input("Enter report title")
    report_author = col1.text_input("Enter the report author's name")
    report_date = col2.date_input("Select a date for the report")
    report_client = col2.text_input("Enter the client's name")

    sect_col1, sect_col2 = st.columns(2, gap='large')

    sect_col1.write("### Section Details")
    section_title = sect_col1.text_input("Enter section title")
    section_text_summary = sect_col1.text_area("Section Summary")

    data_features = df.columns

    sect_col2.write("### Data Summary")
    data_to_summarise = sect_col2.multiselect("Select features to include in statistical summary",
                                              options=data_features)

    st.write("### Scatterplot Setup")
    sub_col1, sub_col2, sub_col3 = st.columns(3)

    chart_x = sub_col1.selectbox('X axis', options=data_features)
    chart_y = sub_col2.selectbox('Y axis', options=data_features)
    chart_z = sub_col3.selectbox('Z axis', options=data_features)

    if st.form_submit_button('Generate'):
        summary_stats = create_df_stats_summary(df, data_to_summarise)
        scatter_plot_file = create_scatterplot(df, chart_x, chart_y, chart_z,
                                               plot_name='scatter', yaxis_scale=[3, 1], )

        generate_report(report_title, report_author, report_date, report_client,
                        section_title, section_text_summary, summary_stats,
                        graph_figure='scatter.png')