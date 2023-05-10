# from langchain.agents import create_pandas_dataframe_agent
# from langchain.llms import OpenAI
# import pandas as pd
#
# df = pd.read_csv('penguins.csv')
#
# agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)
# print(agent.run("how many rows are there?"))

import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt

st.title("pandas-ai streamlit interface")

st.write("A  interface for [PandasAI](https://github.com/gventuri/pandas-ai)")
st.write(
    "Looking for an example *.csv-file?, check [here](https://gist.github.com/netj/8836201)."
)
if "openai_key" not in st.session_state:
    with st.form("API key"):
        key = st.text_input("OpenAI Key", value="", type="password")
        if st.form_submit_button("Submit"):
            st.session_state.openai_key = key
            st.session_state.prompt_history = []
            st.session_state.df = None

if "openai_key" in st.session_state:
    if st.session_state.df is None:
        uploaded_file = st.file_uploader(
            "Choose a CSV file. This should be in long format (one datapoint per row).",
            type="csv",
        )
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df

    with st.form("Question"):
        question = st.text_input("Question", value="", type="default")
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner():
                llm = OpenAI(api_token=st.session_state.openai_key)
                pandas_ai = PandasAI(llm)
                x = pandas_ai.run(st.session_state.df, prompt=question)

                fig = plt.gcf()
                if fig.get_axes():
                    st.pyplot(fig)
                st.write(x)
                st.session_state.prompt_history.append(question)

    if st.session_state.df is not None:
        st.subheader("Current dataframe:")
        st.write(st.session_state.df)

    st.subheader("Prompt history:")
    st.write(st.session_state.prompt_history)


if st.button("Clear"):
    st.session_state.prompt_history = []
    st.session_state.df = None