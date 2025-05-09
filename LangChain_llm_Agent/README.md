# [LangChain_LLM_Agent](https://langchain-llm-agent.streamlit.app/)

* This app presents two types of agents: 'Tool Calling' and 'ReAct' using LangChain.
  GPT models from OpenAI and Gemini models from Google are supported, but only the 'ReAct'
  type of agent is implemented for Gemini models.
  
  - For GPT models such as 'gpt-4o', your OpenAI API key is needed. You can obtain
    an API key from https://platform.openai.com/account/api-keys.

  - For Gemini models such as 'gemini-1.5-pro', your Google API key is needed.
    You can obtain an API key from https://levelup.gitconnected.com/api-tutorial-how-to-use-bing-web-search-api-in-python-4165d5592a7e.

  - For internet searches, obtain your Bing Subscription Key
    [here](https://portal.azure.com/) or Google CSE ID
    [here](https://programmablesearchengine.google.com/about/).

  - Temperature can be set by the user.

  - Voice recognition and Text-To-Speech (TTS) functionalities are supported
    using OpenAI functions, and therefore are enabled when you use
    GPT models from OpenAI.

  - Recording of the user's voice is stopped when there is no input for 3 seconds.
  
  - In addition to the search tools from Bing or Google, ArXiv, Wikipedia,
    Retrieval (RAG), and pythonREPL are supported.
    (PythonREPL from LangChain is still experimental, so caution is needed.)

  - Tracing LLM messages is possible using LangSmith if you download the source code
    and run it on your machine or server.  For this, you need a
    LangChain API key that can be obtained [here](https://smith.langchain.com/settings).

  - When running the code on your machine or server, you can use st.secrets to keep and
    fetch your API keys as environments variables. For such secrets management, see
    [this page](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

## Usage
```python
streamlit run LangChain_llm_Agent.py
```
[![Exploring the App: A Visual Guide](files/Streamlit_Agent_App.png)](https://youtu.be/6uD480u49lU)

Resources:
- [Build a Secure Local RAG Application with Chat History using LangChain, llama3, Qdrant, Redis & Streamlit](https://medium.com/@hemz/build-a-secure-local-rag-application-with-chat-history-using-langchain-llama3-qdrant-redis-986be3628a94)
