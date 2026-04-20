import streamlit as st
import requests  # Standard library for sending API requests

st.set_page_config(page_title="Medical AI Assistant", layout="centered")
st.title("⚕️ General Medicine Chatbot")


API_URL = "http://127.0.0.1:8000/ask"

# for HF space deployment
#API_URL = "http://localhost:8000/ask" # Localhost works because both services are in one container

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a medical question..."):
    # 1. Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Call the API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # We send the query to your FastAPI server
                # Note: 'query' must match the Pydantic model in main.py
                payload = {"query": prompt}
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer found.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
            
            except Exception as e:
                st.error(f"Could not connect to the API. Is Uvicorn running? Error: {e}")