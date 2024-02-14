import streamlit as st
import os
from langchain_openai import ChatOpenAI
from streamlit_extras.switch_page_button import switch_page
from utils import create_call_history_pdf

st.title("ComfortCall Settings")

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = os.environ.get("OPENAI_API_KEY")
    
if "llm" not in st.session_state:
    llm = ChatOpenAI(openai_api_key=st.session_state.openai_api_key, model='gpt-3.5-turbo-0125', temperature=0.5)
    st.session_state.llm = llm

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "recipient" not in st.session_state:
    st.session_state.recipient = ""

if "phone_number" not in st.session_state:
    st.session_state.phone_number = ""
    
if "reason" not in st.session_state:
    st.session_state.reason = ""

def submit_recipient():
    st.session_state.recipient = st.session_state.recipient_widget
    st.session_state.recipient_widget = ""
    
def submit_phone_number():
    st.session_state.phone_number = st.session_state.phone_number_widget
    st.session_state.phone_number_widget = ""

def submit_reason():
    st.session_state.reason = st.session_state.reason_widget
    st.session_state.reason_widget = ""

st.text_input(label = "Who are you calling?", key="recipient_widget", help = "Type the name of who you are calling", on_change=submit_recipient)
if st.session_state.recipient:
    st.write(f"Current Recipient: {st.session_state.recipient}")
    
st.text_input(label = "What is the recipient's phone number?", key="phone_number_widget", help = "Type the phone number of the recipient", on_change=submit_phone_number)
if st.session_state.phone_number:
    st.write(f"Current Phone Number: {st.session_state.phone_number}")
    
st.text_input(label = "What is the reason for the call?", key="reason_widget", help = "Type the reason for the call", on_change=submit_reason)
if st.session_state.reason:
    st.write(f"Current Reason: {st.session_state.reason}")

create_call_history_pdf(st.session_state.messages, st.session_state.recipient) #create empty call history PDF

st.subheader("Please fill out all the above settings before starting the call")
next_page = st.button(label = 'Start Call', key = 'switch_page')
if next_page:
    #start twilio call from here  
    st.switch_page("pages/📱_Call.py")
    
st.subheader("Please press here to end the call and download the call history as a PDF")
#End Call and download call history as PDF
with open("call_history.pdf", "rb") as file:
    download_call_history = st.download_button(
        label="End Call and Download Call History", 
        key="end_call", 
        help="Click to end the call and download call history",
        on_click=create_call_history_pdf(st.session_state.messages, st.session_state.recipient),
        data = file,
        file_name="call_history.pdf",
        mime="application/octet-stream"
    )
    
if download_call_history:
    st.session_state.messages = []
    st.session_state.recipient = ""
    st.session_state.phone_number = ""
    st.session_state.reason = ""
    st.session_state.llm = ChatOpenAI(openai_api_key=st.session_state.openai_api_key, model='gpt-3.5-turbo-0125', temperature=0.5)
    st.rerun()  
    
    



        