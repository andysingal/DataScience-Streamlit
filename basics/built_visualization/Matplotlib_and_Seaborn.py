import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

import datetime as dt

st.title('SF Trees')

st.write('This app analyses trees in San Francisco using'

         ' a dataset kindly provided by SF DPW')

trees_df = pd.read_csv('https://raw.githubusercontent.com/tylerjrichards/'
                       'Getting-Started-with-Streamlit-for-Data-Science/main/pretty_trees/trees.csv')

trees_df['age'] = (pd.to_datetime('today') -

                   pd.to_datetime(trees_df['date'])).dt.days

st.subheader('Seaborn Chart')

fig_sb, ax_sb = plt.subplots()

ax_sb = sns.histplot(trees_df['age'])

plt.xlabel('Age (Days)')

st.pyplot(fig_sb)

st.subheader('Matploblib Chart')

fig_mpl, ax_mpl = plt.subplots()

ax_mpl = plt.hist(trees_df['age'])

plt.xlabel('Age (Days)')

st.pyplot(fig_mpl)