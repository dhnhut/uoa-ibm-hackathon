import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA

# Bring in streamlit for the web interface
import streamlit as st

# Import the WatsonxLangchain interface
# from watsonxlangchain import LangchainInterface
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters


load_dotenv()  # take environment variables from .env.

## ======== Setup all the variables ========
# Load environment variables from .env file
# Ensure that the .env file is in the same directory as this script or provide the path to it
APIKEY = os.getenv("APIKEY")
WATSONX_AI_URL=os.getenv("WATSONX_AI_URL")
PROJECT_ID=os.getenv("PROJECT_ID")
model_id = "mistralai/mistral-large"
temperature = 1


credentials = Credentials(
    url=WATSONX_AI_URL,
    api_key=APIKEY,
)

params = TextChatParameters(
    temperature=temperature
)

model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=PROJECT_ID,
    params=params
)

st.title("Watsonx Langchain Example")
st.write("This is a simple example of using Langchain with Watsonx AI.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])

prompt = st.chat_input("Ask a question about the PDF document:")

if prompt:
  st.chat_message("user").markdown(prompt)
  st.session_state.messages.append({"role": "user", "content": prompt})
  response = model.chat(st.session_state.messages)
  response_content = response["choices"][0]["message"]["content"]
  st.chat_message("assistant").markdown(response_content)
  st.session_state.messages.append({"role": "assistant", "content": response_content})