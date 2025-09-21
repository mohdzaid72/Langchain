import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
MODEL_ID = os.getenv("MODEL_ID", "HuggingFaceH4/zephyr-7b-beta")

HF_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="Q & A Engine", page_icon="💬", layout="centered")
st.title("💬 Ask Related Question")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Format chat for API
    conversation = ""
    for m in st.session_state.messages:
        if m["role"] == "user":
            conversation += f"User: {m['content']}\n"
        elif m["role"] == "assistant":
            conversation += f"Assistant: {m['content']}\n"
    prompt_text = "You are a helpful assistant.\n\n" + conversation + "Assistant:"

    # Call Hugging Face Inference API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            payload = {
                "inputs": prompt_text,
                "parameters": {"max_new_tokens": 300, "temperature": 0.7, "return_full_text": False},
            }
            response = requests.post(HF_URL, headers=HEADERS, json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and "generated_text" in data[0]:
                    reply = data[0]["generated_text"].strip()
                else:
                    reply = str(data)
            else:
                reply = f"Error: {response.text}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
