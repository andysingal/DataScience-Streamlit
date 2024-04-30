We’ve basically been taking this option already, which works very well if we have less exploration work and more implementation work to do.

Pros:
- What you see is what you get – there is no need to maintain both IPython and Python versions of the same app.
- Better experience for learning how to write production code.

Cons:
- A slower feedback loop (the entire app must run before feedback).
- A potentially unfamiliar development environment.

## Data manipulation in Streamlit

Streamlit runs our Python file from the top down as a script, so we can perform data manipulation with powerful libraries such as pandas in the same way that we might in a Jupyter notebook or a regular Python script. As we’ve discussed before,
we can do all our regular data manipulation as normal. For our Palmer’s Penguins app, what if we wanted the user to be able to filter out penguins based on their gender? The following code filters our DataFrame using pandas: 

```py
import streamlit as st
import pandas as pd
import altair as alt 
import seaborn as sns
st.title("Palmer's Penguins")
st.markdown('Use this Streamlit app to make your own scatterplot about penguins!')
penguin_file = st.file_uploader(
    'Select Your Local Penguins CSV (default provided)')
if penguin_file is not None:
    penguins_df = pd.read_csv(penguin_file)
else:
    penguins_df = pd.read_csv('penguins.csv')
selected_x_var = st.selectbox('What do you want the x variable to be?',
                              ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])
selected_y_var = st.selectbox('What about the y?',
                              ['bill_depth_mm', 'bill_length_mm', 'flipper_length_mm', 'body_mass_g'])
selected_gender = st.selectbox('What gender do you want to filter for?',
                               ['all penguins', 'male penguins', 'female penguins'])
if selected_gender == 'male penguins':
    penguins_df = penguins_df[penguins_df['sex'] == 'male']
elif selected_gender == 'female penguins':
    penguins_df = penguins_df[penguins_df['sex'] == 'female']
else:
    pass
alt_chart = (
    alt.Chart(penguins_df, title="Scatterplot of Palmer's Penguins")
    .mark_circle()
    .encode(
        x=selected_x_var,
        y=selected_y_var,
        color="species",
    )
    .interactive()
)
st.altair_chart(alt_chart, use_container_width=True)
```

