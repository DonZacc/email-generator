import streamlit as st
import requests

# Access secrets
apikey = st.secrets["api-key"]
deployment_name = st.secrets["dep-name"]  # This should be model name like "mistralai/Mixtral-8x7B-Instruct"

st.header("Email Generator App")

if 'processing' not in st.session_state:
    st.session_state.processing = False

prompt = st.text_input("Enter your prompt for email generation")

if st.button("Generate Email", disabled=st.session_state.processing):
    if not prompt:
        st.error("Please enter a prompt")
    else:
        st.session_state.processing = True
        st.rerun()

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
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            email = result[0]["generated_text"]
            st.text_area("Generated Email", value=email, height=300)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    st.session_state.processing = False
