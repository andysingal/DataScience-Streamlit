import streamlit as st
import os
import openai
from pypdf import PdfReader
from llama_index.llms.openai import OpenAI
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import StorageContext
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

# Ensure the data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Function to extract text from a PDF using PyPDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to split text into nodes
def split_text_into_nodes(text):
    splitter = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=20,)
    nodes = splitter.get_nodes_from_documents([Document(text=text)])

    return nodes

# Function to get embeddings from OpenAI and store them in a Vector DB index
def embedding_and_storing(nodes, openai_api_key):
    openai.api_key = openai_api_key
    embed_model = OpenAIEmbedding(api_key=openai_api_key)
    
    # Create an ephemeral Chroma client (in-memory instance)
    chroma_client = chromadb.EphemeralClient()
    
    # Create or retrieve the collection
    collection_name = "my_collection"
    chroma_collection = chroma_client.get_or_create_collection(name=collection_name)
    
    # Construct VectorStore
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Convert nodes to Documents
    documents = [Document(text=node.text) for node in nodes]
    
    # Create index from documents (nodes)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

    return index

# Function to retrieve results
def retrieve_results(query, index):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    
    return response.response

# Streamlit UI
def main():
    st.title("PDF Search with LlamaIndex, Chroma and OpenAI")

    # API key input
    openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")
    
    if openai_api_key:
        st.session_state["openai_api_key"] = openai_api_key
        if 'hide_api_success' not in st.session_state:
            st.session_state['hide_api_success'] = False

        if not st.session_state['hide_api_success']:
            st.success("API key saved successfully ✅")
            st.session_state['hide_api_success'] = True  # Hide the success message when the upload starts


        # File uploader
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            file_path = os.path.join("data", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

              # Extract text from PDF
            with st.spinner("Extracting text from PDF..."):
                text = extract_text_from_pdf(file_path)
            
            # Split text into nodes
            with st.spinner("Splitting text into nodes..."):
                nodes = split_text_into_nodes(text)
            
            # Embed and store in vector DB index
            with st.spinner("Embedding text and storing in vector index..."):
                index = embedding_and_storing(nodes, openai_api_key)

            # Chat with the indexed documents
            query = st.text_input("Ask a question about the document:")
            if query:
                with st.spinner("Retrieving results..."):
                    results = retrieve_results(query, index)
                
                st.write(results)

if __name__ == "__main__":
    main()
