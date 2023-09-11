import streamlit as st
from get_parameters import get_parameters
from improve_prompt import improve_prompt

def improve_prompt_section():

    st.subheader("Improve my prompt")
    st.write('Already have ideas but still not sure about the wording of your prompt?')
    input_prompt = st.text_area("", label_visibility="collapsed")
    
    if 'improve_params' not in st.session_state:
        st.session_state.improve_params = None

    with st.expander("__Prompt parameters setting__"):
        st.session_state.improve_params = get_parameters("improve_")
    
    if 'improved_content' not in st.session_state:
        st.session_state.improved_content = []

    if st.button("Improve"):
        improved_output = improve_prompt(input_prompt, st.session_state.improve_params)
        st.session_state.improved_content = improved_output
    
    if  st.session_state.improved_content:
        st.write("🕺🏻 __Here's an improved version of your prompt:__")
        for prompt in  st.session_state.improved_content:
            st.write(prompt)