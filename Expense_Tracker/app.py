import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
from openpyxl import load_workbook as open_xlsb
from utils import convert_df, convert_excel

st.set_page_config(page_title="Expense Tracker",
                   page_icon="💰",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                       'Get Help': "mailto:andysingal@gmail.com",
                       'Report a bug': "mailto:andysingal@gmail.com",
                       'About': "An expense tracker app made with Streamlit."
                       })

st.markdown("""
# Expense Tracker
Select the type of visualization you want to see using the sidebar, then 
insert your expenses in the dataframe below.
""")


# sidebar
st.sidebar.header("1. Visualization Type 🖼️")
st.sidebar.markdown("""Select the type of plot(s) you want to see.""")
viz_type = st.sidebar.multiselect("Visualization Type", ("Pie Chart", "Bar Chart", "Line Chart"), ("Pie Chart", "Bar Chart", "Line Chart"),
                                  label_visibility="collapsed")
st.sidebar.markdown("""---""")

# select which column to focus on when generating the visualization
st.sidebar.header("2. Focus Column 📌")
st.sidebar.markdown("""Select the column you want to emphasize.""")
focus_column = st.sidebar.selectbox("Focus Column", ("Expense", "Details", "Recipient", "Date", "Payment Method"), label_visibility="collapsed")
st.sidebar.markdown("""---""")

# create a dataframe
df = pd.DataFrame({
    "Expense": ["Rent", "Food", "Transportation", "Phone", "Other", "Food", "Transportation"],
    "Details": ["Monthly rent", "Groceries", "Gas, Uber, etc.", "Phone bill", "Charity", "Groceries", "Gas, Uber, etc."],
    "Recipient": ["Landlord", "Grocery Store", "Gas Station", "Phone Company", "Charity", "Grocery Store", "Gas Station"],
    "Date": ["01/12/2021", "02/12/2021", "03/12/2021", "04/12/2021", "05/12/2021", "06/12/2021", "07/12/2021"],
    "Payment Method": ["Debit", "Cash", "Cash", "Credit", "Cash", "Cash", "Cash"],
    "Amount": [1000, 400, 200, 50, 300, 400, 200]
    }, index=[i for i in range(1, 8)])

edited_df = st.experimental_data_editor(df, use_container_width=True, num_rows="dynamic", )

# download the dataframe as a csv file
st.sidebar.header("3. Download Dataframe 📥")
st.sidebar.markdown("""Export the dataframe as a csv or excel file.""")
file_type = st.sidebar.radio("Download as", ("CSV", "Excel"), horizontal=True, label_visibility="collapsed")

if file_type == "CSV":
    file = convert_df(edited_df)
    st.sidebar.download_button("Download dataframe", file, "expense_report.csv", "text/csv", use_container_width=True)
elif file_type == "Excel":
    file = convert_excel(edited_df)
    st.sidebar.download_button("Download dataframe", file, "expense_report.xlsx", use_container_width=True)

# create columns depending on the visualization type
cols = st.columns(len(viz_type))

# generate the visualization
for i, viz in enumerate(viz_type):
    with cols[i]:
        if viz == "Pie Chart":
            fig = px.pie(edited_df, values="Amount", names=focus_column, title=f"{focus_column} Pie Chart")
            st.plotly_chart(fig, use_container_width=True)
        elif viz == "Bar Chart":
            fig = px.bar(edited_df, x=focus_column, y="Amount", title=f"{focus_column} Bar Chart")
            st.plotly_chart(fig, use_container_width=True)
        elif viz == "Line Chart":
            fig = px.line(edited_df, x=focus_column, y="Amount", title=f"{focus_column} Line Chart")
            st.plotly_chart(fig, use_container_width=True)
