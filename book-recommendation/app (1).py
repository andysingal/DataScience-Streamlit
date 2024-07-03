import os
import streamlit as st
import pandas as pd
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
api_key = os.getenv("GROQ_API_KEY")
@st.cache_data
def load_books():
    return pd.read_csv('books.csv')

books_df = load_books()

st.title("Book Recommendations App - By Soham Mhatre")
st.sidebar.header("CSV-based Recommendations - By Soham Mhatre")
csv_genre = st.sidebar.selectbox("Select a genre (CSV)", books_df['Genre'].unique())
if csv_genre:
    st.sidebar.subheader(f"Books in {csv_genre} genre:")
    genre_books = books_df[books_df['Genre'] == csv_genre]
    for _, row in genre_books.iterrows():
        link_text = f"{row['Name']} [Link]({row['URL']}) |"
        st.sidebar.markdown(link_text, unsafe_allow_html=True)
st.header("LLM-based Recommendations")
model_name = st.selectbox("Choose your preferred model", ["llama3-8b-8192", "llama3-70b-8192"])
groq_genre = st.selectbox("Select a genre", ["Science Fiction", "Fantasy", "Mystery", "Romance", "Thriller", "Horror", "Historical Fiction", "Non-fiction"])

if st.button("Get Recommendations"):
    if api_key and groq_genre:
        with st.spinner("Generating recommendations..."):
            model = ChatGroq(model=model_name, api_key=api_key)
            parser = StrOutputParser()
            
            messages = [
                SystemMessage(content="You're a book recommendation expert."),
                HumanMessage(content=f"Generate 100 book recommendations for the {groq_genre} genre. Provide the output as a numbered list of book titles. and write the word 'Link' and then give a link to the wikipedia of that book")
            ]
            
            response = parser.invoke(model.invoke(messages))
            
        st.subheader(f"Book Recommendations for {groq_genre}:")
        st.write(response)
    else:
        st.error("404")

st.sidebar.markdown("---")
st.sidebar.info("This tool uses GroQ inferencing to generate book recommendations. Select a genre from the CSV data on the left, and use the Groq-based recommendations in the main area.")
st.sidebar.info("By Soham Mhatre")