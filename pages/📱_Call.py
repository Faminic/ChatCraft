import streamlit as st
import os
from langchain_openai import ChatOpenAI

st.title("ComfortCall")

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"]):
            st.markdown(f'You: {message["content"]}')
    else:
        with st.chat_message(message["role"]):
            st.markdown(f'{st.session_state.recipient}: {message["content"]}')
        
if prompt := st.chat_input('What do you want to say next?'):
    
    history = ''.join([message['role'] + ': ' + message['content'] + '\n ' for message in st.session_state.messages])
    
    full_prompt = f"""
Human is holding a phone conversation with: {st.session_state.recipient}

The reason for the call is: {st.session_state.reason}

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
        st.markdown(f'{st.session_state.recipient}: {recipient_response}')
        
    st.session_state.messages.append({'role': 'recipient', 'content': recipient_response})