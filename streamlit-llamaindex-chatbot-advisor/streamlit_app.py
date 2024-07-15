import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

st.set_page_config(page_title="adlicious advisor 💬", page_icon="💬", layout="centered", initial_sidebar_state="auto", menu_items=None)

css = r'''
    <style>
        [data-testid="stForm"] {border: 0px;}
        [data-testid="stApp"] {border: 0px;}
        div.block-container {
        max-width: 100vw;
        padding: 2.5rem 0.8rem 0.8rem;
        }
        h1 {
        padding: 0.25rem 0px 1rem;
        }
    </style>
'''

st.markdown(css, unsafe_allow_html=True)

openai.api_key = st.secrets.openai_key

st.title("adlicious advisor 💬")

st.info("Hello, I am an AI bot: chat with me about digital advertising! Interested in running ads with AI? [Contact our adlicious team](mailto:welcome@adlicious.me)")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about adlicious creative & media solutions",
        }
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    docs = reader.load_data()
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        system_prompt="""You are an expert on the adlicious digital advertising company and your job is to answer technical questions. Assume that all questions are related to the adlicious company and their digital advertising solutions. Keep your answers technical and based on facts. – do not hallucinate features.""",
    )
    index = VectorStoreIndex.from_documents(docs)
    return index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True, streaming=True
    )

if prompt := st.chat_input(
    "Ask a question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Write message history to UI
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response_stream = st.session_state.chat_engine.stream_chat(prompt)
        st.write_stream(response_stream.response_gen)
        message = {"role": "assistant", "content": response_stream.response}
        # Add response to message history
        st.session_state.messages.append(message)

