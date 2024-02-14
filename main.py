import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

openai_api_key = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key, model='gpt-3.5-turbo-0125', temperature=0.5)

chain = ConversationChain(
    llm = llm,
    memory = ConversationBufferMemory(),
    verbose=True
)

st.title("ComfortCall")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    st.session_state.chain = chain
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input('What do you want to say next?'):
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    with st.spinner("Thinking what you should say..."):
        response = st.session_state.chain.invoke(input = prompt)['response']
        
    with st.chat_message("Recipient"):
        st.markdown(response)
        
    st.session_state.messages.append({'role': 'recipient', 'content': response})


        