import os
import re
import sqlite3
import pandas as pd
import streamlit as st
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from utils import *
OPENAI_API_KEY= 'secret key'
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY




@st.cache_data
def load_sheet_names(filename):
    excel_file = pd.ExcelFile(file_to_load, engine='openpyxl')
    sheet_names = excel_file.sheet_names

    return sheet_names


@st.cache_data
def load_file_data(filename, sheet_name):
    excel_file = pd.ExcelFile(file_to_load, engine='openpyxl')
    df = excel_file.parse(sheet_name)

    return df


#### streamlit

conn = sqlite3.connect(uri)
chain = get_query_module(conn)
dataframes = []
sheet_names = []
options = []

print('----------start-------')
# set up
if "file_selected" not in st.session_state:
    st.session_state.file_selected = False

if "process_button" not in st.session_state:
    st.session_state.process_button = False

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

st.title('Analyse an Excel file using ChatGPT')

file_name = st.file_uploader('Upload an xlsx file here to begin',
                             type='xlsx',
                             accept_multiple_files=False)

if get_session_state('file_selected') is False:
    if file_name is not None:
        print('have a file name')
        set_session_state('filename', file_name)
        set_session_state('file_selected', True)

if get_session_state('file_selected'):
    print('loading cached file')
    file_to_load = get_session_state('filename')
    sheet_names = load_sheet_names(file_to_load)

options = st.multiselect('Select sheets to use', sheet_names)

button_disabled = (len(options) == 0)

process_button = st.button('Process Selected', disabled=button_disabled)

if process_button or get_session_state('process_button'):

    set_session_state('process_button', True)

    if get_session_state('data_loaded') is False:
        print('loading data')
        for option in options:
            raw_data = load_file_data(get_session_state('filename'), option)
            data = prepare_excel_data(raw_data)
            table_name = clean_name(option)

            dataframes.append({'sheet_name': option,
                               'table_name': clean_name(option)
                               })
            load_data_to_database(conn, data, table_name)

        set_session_state('data_loaded', True)
        set_session_state('dataframes', dataframes)
    else:
        dataframes = get_session_state('dataframes')

st.header('Database views')
if get_session_state('data_loaded'):
    for frame in dataframes:
        st.header(frame['sheet_name'])

        data_from_db = load_sample_from_database(conn, frame['table_name'])
        st.table(data=data_from_db)

st.header('Query Data')
text_query = st.text_input('Ask a question?',
                           value="",
                           max_chars=256,
                           placeholder='E.g. How many years in the data?'
                           )
print(f'text query: {text_query}')

if len(text_query) > 0 and get_session_state('data_loaded'):
    print('run chat')
    result = chain.run(text_query)
    st.write(result)