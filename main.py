import streamlit as st
import os
from langchain_openai import ChatOpenAI

openai_api_key = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key, model='gpt-3.5-turbo-0125', temperature=0.5)

recipient = "Dominos Pizza"
reason = "ordering pizza"

st.title("ComfortCall")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm" not in st.session_state:
    st.session_state.llm = llm
    
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"]):
            st.markdown(f'You: {message["content"]}')
    else:
        with st.chat_message(message["role"]):
            st.markdown(f'{recipient}: {message["content"]}')
        
if prompt := st.chat_input('What do you want to say next?'):
    
    history = ''.join([message['role'] + ': ' + message['content'] + '\n ' for message in st.session_state.messages])
    
    full_prompt = f"""
Human is holding a phone conversation with: {recipient}

The reason for the call is: {reason}

Human provides this input: {prompt}

The current conversation history is:
{history}

You will play the role of the human and respond to the recipient based on the input provided that is consistent with the conversation history and the reason for the call. Only return what the human will say out loud, nothing else.
    """
    
    with st.spinner("Thinking what you should say..."):
        user_response = st.session_state.llm.invoke(full_prompt).content
        
    with st.chat_message("user"):
        st.markdown(f'You: {user_response}')
        
    st.session_state.messages.append({'role': 'user', 'content': user_response})
    
    recipient_response = input("Recipient: ")
        
    with st.chat_message("recipient"):
        st.markdown(f'{recipient}: {recipient_response}')
        
    st.session_state.messages.append({'role': 'recipient', 'content': recipient_response})


        