import streamlit as st
import requests
import json
import re

BACKEND_URL = "http://localhost:8000"  # Replace with your actual backend URL

def embed_and_store_url():
    response = requests.post(f"{BACKEND_URL}/embed-and-store")
    if response.status_code == 200:
        st.write("Embedding and storing successful!")
    else:
        st.write(f"Error: {response.status_code}")

def handle_query(question):
    response = requests.post(f"{BACKEND_URL}/handle-query", params={"question": question})
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.text}"

def delete_index():
    response = requests.post(f"{BACKEND_URL}/delete-index")
    if response.status_code == 200:
        st.write("Index deleted successfully!")
    else:
        st.write(f"Error: {response.status_code}")


st.write("# Welcome to Bookstore Assistant! 👋")

st.write(
    "Hi! I'm your Bookstore assistant.\n Start by asking me for recommendations for a book!")

if st.button("Embed"):
    embed_and_store_url()


question = st.chat_input("Enter a question:")
chat_history = [{"isBot": True, "text": "Enter a question:"}]

if question:
    with st.chat_message("user"):
        st.markdown(question)
    with st.spinner("..."):
        response = handle_query(question)
        with st.chat_message("assistant"):
            print(response)
            st.write(response)
    chat_history.append({"isBot": False, "text": question}) 
    chat_history.append({"isBot": True, "text": response})

if st.button("End session", key="final"):
    delete_index()
