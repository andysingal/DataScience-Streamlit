import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

st.title("SF Tree")

st.write('This app analyses trees in San Francisco using a dataset kindly provided by SF DPW')

trees_df = pd.read_csv('https://raw.githubusercontent.com/tylerjrichards/'
                       'Getting-Started-with-Streamlit-for-Data-Science/main/pretty_trees/trees.csv')

# df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id'])
#
# st.line_chart(df_dbh_grouped)
#
# df_dbh_grouped['new_col'] = np.random.randn(len(df_dbh_grouped)) * 500
# st.line_chart(df_dbh_grouped)
#
# st.bar_chart(df_dbh_grouped)
#
# st.area_chart(df_dbh_grouped)
trees_df = trees_df.dropna(subset=['longitude', 'latitude'])

trees_df = trees_df.sample(n = 1000)

st.map(trees_df)

st.write(trees_df.head())

# tree_file = st.file_uploader('Select Your Local Penguins CSV (default provided)')
#
# @st.cache_resource
# def load_file(penguin):
#     time.sleep(3)
#
#     if tree_file is not None:
#
#            df = pd.read_csv(tree_file)
#
#     else:
#
#            df = pd.read_csv('https://raw.githubusercontent.com/tylerjrichards/Getting-Started-with-Streamlit-for-Data-Science/main/pretty_trees/trees.csv')
#
#     return (df)
