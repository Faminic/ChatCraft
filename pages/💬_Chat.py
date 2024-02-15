import streamlit as st
import os
from langchain_openai import ChatOpenAI

st.title("ChatCraft")

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar="🧑‍💻"):
            st.markdown(f'You: {message["content"]}')
    else:
        with st.chat_message(message["role"], avatar="🤖"):
            st.markdown(f'{st.session_state.recipient}: {message["content"]}')
        
if prompt := st.chat_input('What do you want to say next?'):
    
    history = ''.join([message['role'] + ': ' + message['content'] + '\n ' for message in st.session_state.messages])
    
    full_prompt = f"""
Human is holding a sms conversation with: {st.session_state.recipient}

Human's relationship to {st.session_state.recipient} is: {st.session_state.relationship}

The context for the chat is: {st.session_state.context}

Specific instructions given to the AI: {st.session_state.specific_instructions}

Human provides this input: {prompt}

The current conversation history is:
{history}

Play the role of the human and respond to the recipient based on the input provided that is consistent with the conversation history and the context for the chat. Add more to the human's message if it helps achieve the goal of the conversation. Only return human's message without the role.
"""
    
    with st.spinner("Thinking what you should say..."):
        user_response = st.session_state.llm.invoke(full_prompt).content
        
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(f'You: {user_response}')
        
    st.session_state.messages.append({'role': 'user', 'content': user_response})
    
    recipient_prompt = f"""
Human is holding a sms conversation with: {st.session_state.recipient}

Human's relationship to {st.session_state.recipient} is: {st.session_state.relationship}

The context for the chat is: {st.session_state.context}

Specific instructions given to the AI: {st.session_state.specific_instructions}

Human just said this: {user_response}

The current conversation history is:
{history}

Play the role of the {st.session_state.recipient} and respond to the human based on the input provided that is consistent with the conversation history and the context for the chat. Respond according to their relationship and past context. Only return {st.session_state.recipient}'s message without the role.
"""

    with st.spinner("Thinking what the recipient should say..."):
        recipient_response = st.session_state.llm.invoke(recipient_prompt).content
        
    with st.chat_message("recipient", avatar="🤖"):
        st.markdown(f'{st.session_state.recipient}: {recipient_response}')
        
    st.session_state.messages.append({'role': 'recipient', 'content': recipient_response})