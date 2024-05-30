
import os

# os.environ["HF_HOME"] = "/workspaces/chat-any/weights"

import gc
import re # website url validation
import uuid # unique id for each session
import nest_asyncio # allows nested access to the event loop
nest_asyncio.apply()

import streamlit as st
from torch import cuda
from dotenv import load_dotenv
load_dotenv() # Load Gemini API


from llama_index.core import Settings
from llama_index.core import PromptTemplate
from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from llama_index.llms.gemini import Gemini


# ---------- Init + Helper function ----------------

# setting up the embedding model
def load_embedding_model(
    model_name: str = "BAAI/bge-small-en",
    device: str = "cuda" if cuda.is_available() else "cpu"
) -> HuggingFaceBgeEmbeddings:
    model_kwargs = {"device": device}
    encode_kwargs = {
        "normalize_embeddings": True
    }  # set True to compute cosine similarity
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return embedding_model

lc_embedding_model = load_embedding_model()
embed_model = LangchainEmbedding(lc_embedding_model)

# setting up session
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

session_id = st.session_state.id
client = None

# setting up the llm
llm = Gemini(model_name="models/gemini-pro", api_key=os.environ['GOOGLE_API_KEY'])

# helper func
def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None
    gc.collect() # free up memory

def validate_website_url(url):

    url_pattern = re.compile(
        r'http[s]?://'  # http:// or https://
        r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|'  # domain...
        r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'  # ...or percent-encoded characters
        r'(?:\:[0-9]{1,5})?'  # optional port number
        r'(?:/[a-zA-Z0-9$-_@.&+!*\\(\\),=%]*)*'  # path
        r'(?:\?[a-zA-Z0-9$-_@.&+!*\\(\\),=%]*)?'  # query string
        r'(?:#[a-zA-Z0-9$-_@.&+!*\\(\\),=%]*)?'  # fragment
    )
    return bool(url_pattern.match(url))

# ---------- End helper function ----------------

with st.sidebar:
    # Input for URL
    website_url = st.text_input("URL")

    # Button to load and process url
    load_button = st.button("Load")

    message_container = st.empty()  # Placeholder for dynamic messages

    if load_button and website_url:
        if validate_website_url(website_url):
            with st.spinner(f"Loading website..."):
                try:
                    # -------------------------------------------
                    # Load data from a website via Llamaindex Loader
                    # -------------------------------------------
                    loader = SimpleWebPageReader()
                    docs = loader.load_data([website_url])

                    # ---- Create vector store and upload data ---
                    # Chunking and create embeddings
                    # Automatic via llama index VectorStoreIndex
                    # --------------------------------------------
                    Settings.embed_model = embed_model
                    index = VectorStoreIndex.from_documents(docs)

                    # ====== Setup a query engine ======
                    Settings.llm = llm
                    query_engine = index.as_query_engine(similarity_top_k=4) # TODO
                    # query_engine = index.as_query_engine(streaming=True, similarity_top_k=4) # TODO

                    # ====== Customise prompt template ======
                    qa_prompt_tmpl_str = (
                        "You are a formal, friendly and supportive assistant for question answering from given website (Answer questions in complete sentences).\n"
                        "Answer the question using the following information delimited by triple brackque.:\n\n"
                        "```\n{context_str}\n```"
                        "Question: {query_str}\n"
                        "\nYou can format ouput in a aesthetic way. Remember: Don't say based on information provided or something like that"
                        "\nIn case you don't know the answer or any exception occur, say 'I don't know!'"
                    )
                    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

                    query_engine.update_prompts(
                        {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
                    )
                    # ======= Complete setting up !!!! ========
                    if docs:
                        message_container.success("Data loaded successfully!!")
                    else:
                        message_container.write(
                            "No data found, check if the repository is not empty!"
                        )
                    st.session_state.query_engine = query_engine

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.stop()

                st.success("Ready to Chat!")
        else:
            st.error('Invalid url')
            st.stop()

col1, col2 = st.columns([6, 1])

with col1:
    st.header(f"Chat with any website")

with col2:
    st.button("Clear ↺", on_click=reset_chat)


# Initialize chat history
if "messages" not in st.session_state:
    reset_chat()


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("What's up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        query_engine = st.session_state.query_engine
        full_response = query_engine.query(prompt)
        # # TODO: Simulate stream of response with milliseconds delay
        # full_response = ""
        # streaming_response = query_engine.query(prompt)

        # for chunk in streaming_response.response_gen:
        #     full_response += chunk
        #     message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
