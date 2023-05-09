import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
st.title("Palmer's Penguins")
st.markdown('Use this Streamlit app to make your own scatterplot about penguins!')
selected_species = st.selectbox('What species would you like to visualize?',

     ['Adelie', 'Gentoo', 'Chinstrap'])

selected_x_var = st.selectbox('What do want the x variable to be?',

['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])

selected_y_var = st.selectbox('What about the y?',

['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])

url = "https://raw.githubusercontent.com/tylerjrichards/Streamlit-for-Data-Science/main/penguin_app/penguins.csv"
penguins_df = pd.read_csv(url)
penguins_df = penguins_df[penguins_df['species'] == selected_species]

sns.set_style('darkgrid')

markers = {"Adelie": "X", "Gentoo": "s", "Chinstrap":'o'}

fig, ax = plt.subplots()

ax = sns.scatterplot(x = penguins_df[selected_x_var],

y = penguins_df[selected_y_var], hue = penguins_df['species'])

plt.xlabel(selected_x_var)

plt.ylabel(selected_y_var)

plt.title('Scatterplot of {} Penguins'.format(selected_species))

st.pyplot(fig)