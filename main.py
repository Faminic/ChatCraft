import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate

openai_api_key = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key, model='gpt-3.5-turbo-0125', temperature=0.5)
template = """
{input}

The current conversation history is: {history}

You will play the role of the human and respond to the recipient based on the input provided that is consistent with the conversation history and the reason for the call.
"""
prompt_template = PromptTemplate(input_variables=["history", "input"], template=template)

chain = ConversationChain(
    llm = llm,
    memory = ConversationBufferMemory(return_messages=True),
    verbose=True,
    prompt=prompt_template
)

recipient = "Dominos Pizza"
reason = "ordering pizza"

st.title("ComfortCall")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    st.session_state.chain = chain
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input('What do you want to say next?'):
    
    updated_prompt = f"""
    Human is holding a phone conversation with: {recipient}
    The reason for the call is: {reason}
    Human provides this input: {prompt}
    """
    
    with st.spinner("Thinking what you should say..."):
        user_response = st.session_state.chain.invoke(input = updated_prompt)['response']
        
    with st.chat_message("user"):
        st.markdown(user_response)
        
    st.session_state.messages.append({'role': 'user', 'content': user_response})
    
    recipient_response = 'Yup I got it'
        
    with st.chat_message("Recipient"):
        st.markdown(recipient_response)
        
    st.session_state.messages.append({'role': 'recipient', 'content': recipient_response})


        