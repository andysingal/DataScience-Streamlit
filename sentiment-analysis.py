# Import the necessary packages
import streamlit as st
from api_key import apikey
from langchain.llms import OpenAI
import os

os.environ['OPENAI_API_KEY'] = apikey

llm = OpenAI()

# Create a Streamlit sidebar
st.sidebar.title('Real-Time Sentiment Analysis')

# Allow the user to upload a text file
uploaded_file = st.sidebar.file_uploader('Upload your text file', type='txt')

# Define a function to call the GPT-3 API and analyze sentiment
def analyze_sentiment(text):
    response = llm(
        f'This is a sentiment analysis request. What is the sentiment of the following text, and why?\n\n"{text}"\n\nSentiment: {{sentiment}}, Justification: {{justification}}')
    return response


if uploaded_file is not None:
    text = uploaded_file.read().decode('utf-8')

    # Analyze the sentiment of the whole text
    sentiment_and_explanation = analyze_sentiment(text)

    # Display the sentiment analysis and explanation
    st.write(f'Sentiment Analysis and Explanation: {sentiment_and_explanation}')
