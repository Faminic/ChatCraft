import streamlit as st
import os
import time
from langchain_openai import ChatOpenAI
from utils import create_chat_history_pdf
time.sleep(0.1)

st.title("ChatCraft Settings")

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = os.environ.get("OPENAI_API_KEY")
    
if "llm" not in st.session_state:
    llm = ChatOpenAI(openai_api_key=st.session_state.openai_api_key, model='gpt-3.5-turbo-0125', temperature=0.8)
    st.session_state.llm = llm

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "recipient" not in st.session_state:
    st.session_state.recipient = ""

if "relationship" not in st.session_state:
    st.session_state.relationship = ""
    
if "context" not in st.session_state:
    st.session_state.context = ""

if "specific_instructions" not in st.session_state:
    st.session_state.specific_instructions = ""

def submit_recipient():
    st.session_state.recipient = st.session_state.recipient_widget
    st.session_state.recipient_widget = ""
    
def submit_relationship():
    st.session_state.relationship = st.session_state.relationship_widget
    st.session_state.relationship_widget = ""

def submit_context():
    st.session_state.context = st.session_state.context_widget
    st.session_state.context_widget = ""
    
def submit_specific_instructions():
    st.session_state.specific_instructions = st.session_state.specific_instructions_widget
    st.session_state.specific_instructions_widget = ""

st.text_input(label = "Who do you want to message?", key="recipient_widget", help = "Type who you want to message", on_change=submit_recipient)
if st.session_state.recipient:
    st.write(f"Current Recipient: {st.session_state.recipient}")

st.text_input(label = f"What is your relationship with {st.session_state.recipient}?", key="relationship_widget", help = f"Type your relationship with {st.session_state.recipient}", on_change=submit_relationship)
if st.session_state.relationship:
    st.write(f"Current Relationship: {st.session_state.relationship}")
    
st.text_input(label = "What is the context behind this conversation?", key="context_widget", help = "Type the context for the conversation", on_change=submit_context)
if st.session_state.context:
    st.write(f"Current Context: {st.session_state.context}")
    
st.text_input(label = "Any specific instructions you want to give to the AI? You can leave this blank.", key="specific_instructions_widget", help = "Type any further details you want to add", on_change=submit_specific_instructions)
if st.session_state.specific_instructions:
    st.write(f"Further Details: {st.session_state.specific_instructions}")

create_chat_history_pdf(st.session_state.messages, st.session_state.recipient) #create empty chat history PDF

st.subheader("Please fill out all the above settings before starting the conversation")
next_page = st.button(label = 'Start Conversation', key = 'switch_page')
if next_page: 
    st.switch_page("pages/💬_Chat.py")
    
st.subheader("Please click below to end the conversation and download the chat history as a PDF")

with open("chat_history.pdf", "rb") as file:
    download_chat_history = st.download_button(
        label="End Conversation and Download Chat History", 
        key="end_chat", 
        help="Click to end the conversation and download the chat history",
        on_click=create_chat_history_pdf(st.session_state.messages, st.session_state.recipient),
        data = file,
        file_name="chat_history.pdf",
        mime="application/octet-stream"
    )
    
if download_chat_history:
    st.session_state.messages = []
    st.session_state.recipient = ""
    st.session_state.relationship = ""
    st.session_state.context = ""
    st.session_state.specific_instructions = ""
    st.session_state.llm = ChatOpenAI(openai_api_key=st.session_state.openai_api_key, model='gpt-3.5-turbo-0125', temperature=0.8)
    st.rerun()  
    
    



        