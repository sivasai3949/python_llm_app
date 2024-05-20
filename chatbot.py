import streamlit as st
import os
from groq import Groq

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Groot Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')
    if 'GROOT_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        groot_api = st.secrets['GROOT_API_TOKEN']
    else:
        groot_api = st.text_input('Enter Groot API token:', type='password')
        if not (groot_api.startswith('g8_') and len(groot_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['GROOT_API_TOKEN'] = groot_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Groot model', ['llama3-8b-8192'], key='selected_model')
    groot_model = "llama3-8b-8192"
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=1000, step=8)
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')

# Store Groot generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating Groot response
def generate_groot_response(prompt_input):
    client = Groq(api_key=groot_api)
    completion = client.chat.completions.create(
        model=groot_model,
        messages=[{"role": "assistant", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt_input}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_length
    )
    return completion["data"]["completion"]

# User-provided prompt
if prompt := st.chat_input(disabled=not groot_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_groot_response(prompt)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
