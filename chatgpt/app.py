import streamlit as st
import openai, os
model_engine = "text-davinci-003"
openai.api_key = os.environ.get('OPENAI_API_KEY', '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')
def ChatGPT(user_query):
    '''
    This function uses the OpenAI API to generate a response to the given
    user_query using the ChatGPT model
    '''
    # Use the OpenAI API to generate a response
    completion = openai.Completion.create(
                                  engine = model_engine,
                                  prompt = user_query,
                                  max_tokens = 1024,
                                  n = 1,
                                  temperature = 0.5,
                                      )
    response = completion.choices[0].text
    return response

def main():
    '''
    This function gets the user input, pass it to ChatGPT function and
    displays the response
    '''
    # Get user input
    user_query = st.text_input("Enter query here, to exit enter :q", "what is Python?")
    if user_query != ":q" or user_query != "":
        # Pass the query to the ChatGPT function
        response = ChatGPT(user_query)
        return st.write(f"{user_query} {response}")

