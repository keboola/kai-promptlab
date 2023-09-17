# improve_prompt.py

import streamlit as st

from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

def improve_prompt():

    if 'improved_content' not in st.session_state:
        st.session_state.improved_content = ""
    
    if 'last_user_input' not in st.session_state:
        st.session_state.last_user_input = ""

    template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a prompt engineer."
            )
        ),
        HumanMessagePromptTemplate.from_template("""
Given the original input below, please rephrase it in a more detailed and comprehensive manner, emphasizing key points and insights, while retaining its original meaning.

Original Input: '{text}'
    """),
    ])

    models = [
        "gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", 
        "gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613"
    ]
    
    st.markdown(f'<h3 style="border-bottom: 2px solid #288CFC; ">{"Improve"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    st.write('Already have ideas but still not sure about the wording of your current prompt?')
    
    with st.chat_message("user", avatar="💬"):
        col1, col2 = st.columns([7, 1])
        with col1: 
            user_input = st.text_input("", label_visibility="collapsed")
        with col2: 
            improve = st.button("Improve", use_container_width=True)
        
        with st.expander("__Improve prompt parameters setting__"):
            col1,col2,col3 = st.columns(3) 
            model_prompt = col1.selectbox("Model", models)
            tokens_prompt = col2.number_input("Max tokens", min_value=0, value=150)
            temp_prompt = col3.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7) 
        
        if improve:
            if user_input:
                llm = ChatOpenAI(model=model_prompt, temperature=temp_prompt, max_tokens=tokens_prompt)
                improved_input = llm(template.format_messages(text=user_input))
                
                st.session_state.improved_content = improved_input.content
                st.session_state.last_user_input = user_input
            
        if "improved_content" in st.session_state:
            st.write(st.session_state.improved_content)
