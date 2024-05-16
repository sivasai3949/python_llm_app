import streamlit as st
import requests

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Replicate API endpoint
REPLICATE_API_ENDPOINT = "https://api.replicate.com/v1/predictions"

# Function to get Replicate API token from Streamlit secrets
def get_replicate_api_token():
    return st.secrets["replicate_api_token"]

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    headers = {
        "Authorization": f"Bearer {get_replicate_api_token()}",
        "Content-Type": "application/json"
    }
    payload = {
        "version": llm,
        "input": {
            "text": prompt_input
        }
    }
    response = requests.post(REPLICATE_API_ENDPOINT, json=payload, headers=headers)
    prediction_id = response.json().get("id")

    # Polling for the prediction result
    prediction_result = None
    while prediction_result is None:
        prediction_response = requests.get(f"{REPLICATE_API_ENDPOINT}/{prediction_id}", headers=headers)
        prediction_result = prediction_response.json().get("input")

    return prediction_result.get("text")

# User-provided prompt
if prompt := st.text_input("Enter your message"):
    with st.spinner("Thinking..."):
        response = generate_llama2_response(prompt)
        st.write(response)
