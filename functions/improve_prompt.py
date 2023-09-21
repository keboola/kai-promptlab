# improve_prompt.py


import streamlit as st

from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

from functions.best_practices import best_practices_var

def improve_prompt():

    if 'improved_content' not in st.session_state:
        st.session_state.improved_content = ""
    
    if 'last_user_input' not in st.session_state:
        st.session_state.last_user_input = ""

    template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=best_practices_var    
        ),
        HumanMessagePromptTemplate.from_template("'{text}'"),
    ])
    
    st.markdown(f'<h3 style="border-bottom: 2px solid #288CFC; ">{"Improve"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    st.markdown("🛠️ Already have ideas but still unsure about the wording of your current prompt? Enter your idea, hit the __'Improve'__ button and voilà! You'll get an improved version that follows prompt engineering best practices.")
    
    with st.chat_message("user", avatar="💬"):
        col1, col2 = st.columns([7, 1])
        with col1: 
            user_input = st.text_input("", label_visibility="collapsed")
        with col2: 
            improve = st.button("Improve", use_container_width=True)
        
        with st.expander("__Set the temperature__"):
            col1, _, _ = st.columns(3)
            temp_prompt = col1.slider("Temperature", min_value=0.0, max_value=1.0, value=0.25) 
        
        if improve:
            if user_input:
                llm = ChatOpenAI(model="gpt-4", temperature=temp_prompt, max_tokens=2000)
                improved_input = llm(template.format_messages(text=user_input))
                
                st.session_state.improved_content = improved_input.content
                st.session_state.last_user_input = user_input
            
        if "improved_content" in st.session_state:
            st.code(st.session_state.improved_content, language="json")
