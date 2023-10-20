# improve_prompt.py

import streamlit as st
import openai 

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from functions.best_practices import best_practices_var

MODEL_NAME = ["gpt-4", "gpt-3.5-turbo-16k", "gpt-3.5-turbo"]
MAX_TOKENS = 2000
DEFAULT_TEMP = 0.25

def clear_text():
    st.session_state["text_improve"] = ""

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text="", display_method='code'):
        self.container = container
        self.text = initial_text
        self.display_method = display_method

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token 
        display_function = getattr(self.container, self.display_method, None)
        if display_function is not None:
            display_function(self.text)
        else:
            raise ValueError(f"Invalid display_method: {self.display_method}")

# Get user input and return improved
def improve_prompt_ui():
    st.markdown(f'<h3 style="border-bottom: 2px solid #3ca0ff; ">{"Improve"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    st.info("""
        🛠️ Here you can get an improved version of your prompt. You should include the relevant column names in double square brackets: [[col_name]].
            
        Once you get the new version of your prompt and you are happy with the wording and examples given, simply copy it in the top right corner and use it in the _Test_ section.
            """)
    

    with st.chat_message("ai"):
        chat_box = st.text("Heyo! I'm here to help you improve the wording of your prompt. Simply type it in the area below and I'll do the rest. 🦾")
        instructions = st.empty()
    
    with st.container():
        col1, col2 = st.columns([7, 1])
        with col1: 
            with st.chat_message("user"):
                query = st.text_area("User input", placeholder="Example: You are a marketer. Create a fun short message for the customer informing them that the [[product]] will be back in stock on [[date]].", label_visibility="collapsed", key="text_improve")
        with col2: 
            ask_button = st.button("Improve", use_container_width=True)
            reset = st.button("Reset", use_container_width=True, on_click=clear_text)
        with st.expander("__Parameter Settings__"):
            col1, col2, _ = st.columns(3)
            model_prompt = col1.selectbox("Model", MODEL_NAME, help='For best results, the "gpt-4" model is recommended.')
            temp_prompt = col2.slider("Temperature", min_value=0.0, max_value=1.0, value=DEFAULT_TEMP, 
                                        help="Lower values for temperature result in more consistent outputs, while higher values generate more diverse and creative results. Select a temperature value based on the desired trade-off between coherence and creativity for your specific application.", 
            )    
    messages = [
    SystemMessage(
        content=best_practices_var    
    ),
    HumanMessage(
        content=query
        ),
    ]

    stream_handler = StreamHandler(chat_box, display_method='code')
    chat = ChatOpenAI(model=model_prompt, temperature=temp_prompt, max_tokens=MAX_TOKENS, streaming=True, callbacks=[stream_handler])

    if query and ask_button:
        response = chat(messages)
        st.session_state.improved_content = response.content
    
    if reset:   
        st.session_state.improved_content = ""

    if st.session_state.improved_content:
        chat_box.code(st.session_state.improved_content, language="http") 

def improve_prompt():
    if 'improved_content' not in st.session_state:
        st.session_state.improved_content = ""
    
    improve_prompt_ui()