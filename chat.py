import streamlit as st
import os
os.environ['STREAMLIT_SERVER_WATCH_FILE_CHANGES'] = 'true'
import requests

# Set page config
st.set_page_config(page_title="Auto-CoT Chat", page_icon="💬")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for API settings
with st.sidebar:
    st.title("API Settings")
    api_url = st.text_input("API URL", "http://localhost:8000/v1")
    full_url = f"{api_url}/chat/completions"

# Display chat messages
st.title("Auto-CoT Chat")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Send request to API
    try:
        response = requests.post(
            full_url,
            json={
                "messages": st.session_state.messages,
                "model": "gpt-4o-mini"
            }
        )
        
        if response.status_code == 200:
            assistant_response = response.json()['choices'][0]['message']['content']
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")