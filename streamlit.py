import streamlit as st
import requests

# Access secrets safely
apikey = st.secrets["api-key"]
deployment_name = st.secrets["dep-name"]

st.header("Email Generator App")

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Get user input
prompt = st.text_input("Enter your prompt for email generation")

# Button to trigger generation
if st.button("Generate Email", disabled=st.session_state.processing):
    if not prompt:
        st.error("Please enter a prompt")
    else:
        st.session_state.processing = True
        st.rerun()

# If processing is True
if st.session_state.processing and prompt:
    with st.spinner("Generating email..."):
        url = f"https://api-inference.huggingface.co/models/{deployment_name}"
        
        headers = {
            "Authorization": f"Bearer {apikey}"
        }

      payload = {
            "inputs": f"Write a professional email based on this: {prompt}",
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 300,
                "return_full_text": False
            }0
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            email = response.json()["choices"][0]["message"]["content"]
            st.text_area("Generated Email", value=email, height=300)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    st.session_state.processing = False
