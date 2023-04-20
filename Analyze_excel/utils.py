import os
import re
import sqlite3
import pandas as pd
import streamlit as st
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

unsafe_characters = re.compile(r'[^a-zA-Z0-9 ]')
DEBUG = True
uri = "file::memory:?cache=shared"
sqlalchmey_uri = 'sqlite:///' + uri

def prepare_excel_data(df):
    df.columns = [clean_name(x) for x in df.columns]
    return df


def clean_name(word):
    clean_word = unsafe_characters.sub('_', word)
    return clean_word.replace(' ', '_').lower()


def load_data_to_database(conn, data, table_name):
    data.to_sql(table_name, conn, if_exists='replace', index=False)


def load_sample_from_database(conn, table_name):
    return pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 3", conn)


def get_query_module(conn):
    # reuse the existing connection
    # https://stackoverflow.com/questions/23743336/in-sqlalchemy-can-i-create-an-engine-from-an-existing-odbc-connection
    eng = create_engine(url='sqlite:///file:memdb1?mode=memory&cache=shared', poolclass=StaticPool,
                        creator=lambda: conn)
    db = SQLDatabase(engine=eng)

    llm = OpenAI(temperature=0)

    db_chain = SQLDatabaseChain(llm=llm,
                                database=db,
                                verbose=True
                                # ,return_intermediate_steps=True
                                )

    return db_chain


def set_session_state(name, data):
    if DEBUG:
        print(f'setting state {name}')
    st.session_state[name] = data

def get_session_state(name):
    if name in st.session_state:
        return st.session_state[name]