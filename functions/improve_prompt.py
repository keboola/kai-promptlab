# improve_prompt.py

import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate

from functions.best_practices import best_practices_var

MODEL_NAME = ["gpt-4", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"]
MAX_TOKENS = 2000
DEFAULT_TEMP = 0.25

# Improve user input
def get_improved_input(user_input, model, temperature):
    template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(f'{best_practices_var}'
                
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)
    
    llm = ChatOpenAI(model=model, temperature=temperature, max_tokens=MAX_TOKENS)

    return llm(template.format_messages(text=user_input))

def clear_text():
    st.session_state["text_improve"] = ""

# Get user input and return improved
def improve_prompt_ui():
    st.markdown(f'<h3 style="border-bottom: 2px solid #288CFC; ">{"Improve"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    st.markdown("""
    🛠️ Already have ideas but still unsure about the wording of your current prompt? Enter your idea, hit the __'Improve'__ button and check out the improved version that follows prompt engineering best practices. Put your input data (column names) in double square brackets, e.g. "[[col_name]]".
                """)
    
    with st.chat_message("user", avatar="💬"):
        col1, col2 = st.columns([7, 1])
        with col1: 
            user_input = st.text_area("User input", label_visibility="collapsed", key="text_improve")
        with col2: 
            improve = st.button("Improve", use_container_width=True)
            reset = st.button("Reset", use_container_width=True, on_click=clear_text)
        
        with st.expander("__Parameter Settings__"):
            col1, col2, _ = st.columns(3)
            model_prompt = col1.selectbox("Model", MODEL_NAME, help='For best results, the "gpt-4" model is recommended.')
            temp_prompt = col2.slider("Temperature", min_value=0.0, max_value=1.0, value=DEFAULT_TEMP, 
                                        help="Lower values for temperature result in more consistent outputs, while higher values generate more diverse and creative results. Select a temperature value based on the desired trade-off between coherence and creativity for your specific application.", 
    ) 
    
        if improve and user_input:
            improve_state = st.text("")
            improved_input = get_improved_input(user_input, model_prompt, temp_prompt)
            st.session_state.improved_content = improved_input.content
            improve_state.warning("The best practice is to place your input data after the backticks.", icon="💡")
                
        if reset: 
            st.session_state.improved_content = ""
            
        if "improved_content" in st.session_state:
            st.code(st.session_state.improved_content, language="http")

def improve_prompt():
    if 'improved_content' not in st.session_state:
        st.session_state.improved_content = ""
    
    improve_prompt_ui()