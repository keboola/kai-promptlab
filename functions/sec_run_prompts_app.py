# sec_run_prompts_app.py

import streamlit as st
import re 
import pandas as pd

from functions.fun_get_parameters import get_parameters
from functions.fun_run_prompt import run_prompt
from functions.fun_process_rating_input import process_rating_input
from functions.fun_rating import rating

def run_prompts_app(df):
    
    def init_session_states():
        default_params = {
            "response_params_1": {},
            "response_params_2": {},
            "response_params_3": {},
            'response_content': None
        }

        for key, value in default_params.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def get_prompts(num_prompts):
        prompts_dict = {}
        for i in range(num_prompts):
            prompt_input = st.text_area(
                "", 
                placeholder=f'Prompt {i+1}:', 
                label_visibility="collapsed"
            )
            prompts_dict[f"prompt_{i+1}"] = prompt_input

            with st.expander(f"__Prompt {i+1} parameters setting__"):
                response_params = get_parameters(f"prompt_{i+1}")
                st.session_state[f"response_params_{i+1}"] = response_params

        return prompts_dict

    def apply_and_show_prompts(df, dict):
        prompt_output = pd.DataFrame(index=df_subset.index)
        
        for idx, prompt_key in enumerate(dict.keys()):
            if dict[prompt_key]:
                apply_prompt_state = st.text('Something is cooking...')
                placeholder_columns = re.findall(r'\[(.*?)\]', dict[prompt_key])
                result_series = df.apply(
                    run_prompt, 
                    args=(dict[prompt_key], prompt_key, placeholder_columns, st.session_state[f"response_params_{idx+1}"]),
                    axis=1
                )
            prompt_output[prompt_key] = result_series[prompt_key]
            apply_prompt_state.text("Done! 👨‍🍳")
        st.session_state["response_content"] = prompt_output
        

    init_session_states()

    #st.subheader("👨‍💻 Test")
    
    color_hex = "#288CFC"
    subheader_html_hex = f"""
    <h3 style="border-bottom: 2px solid {color_hex}; margin-bottom: 10px;">
    Test
    </h3>
    """
    st.markdown(subheader_html_hex, unsafe_allow_html=True)
    
    num_prompts = st.number_input("Select how many prompts you want to test:", min_value=1, value=2, max_value=3)
    st.write('To use values from your table, you must specify the desired column within the prompt using square brackets, e.g. "[column]"')
    
    prompts_dict = get_prompts(num_prompts)
    placeholder_columns = re.findall(r'\[(.*?)\]', ''.join(prompts_dict.values()))

    missing_cols = [col for col in placeholder_columns if col not in df.columns]
    if missing_cols:
        st.warning(f"Your data is missing the following columns: {', '.join(missing_cols)}")
        st.stop()

    rows_to_use = int(st.number_input("Select how many rows of the table you want to use:", min_value=1, value=5, max_value=df.shape[0]))
    df_subset = df.head(rows_to_use)
    
    if st.button('OKaaaAAAaaAYYYy LETS GO 🎢'):
        apply_and_show_prompts(df_subset, prompts_dict)

    if "response_content" in st.session_state and st.session_state["response_content"] is not None:
        #st.subheader("Results")
        
        color_hex = "#288CFC"
        subheader_html_hex = f"""
        <h3 style="border-bottom: 2px solid {color_hex}; margin-bottom: 10px;">
        Results
        </h3>
        """
        st.markdown(subheader_html_hex, unsafe_allow_html=True)
    
        st.dataframe(st.session_state["response_content"])
        rating_input = process_rating_input(st.session_state["response_content"])
        
        col1, col2, col3 = st.columns(3)
        with col1: 
            rate_button = st.button('Rate Results', use_container_width=True)
        with col2: 
            st.button('Get Data to Keboola', use_container_width=True)
        with col3:
            reset_button = st.button('Reset App', use_container_width=True)
        
        if rate_button:
            #st.write(rating_input)
            rating_out = st.session_state["response_content"].apply(rating, 
                    args=("similarity score", rating_input),
                    axis=1
                )
            st.dataframe(rating_out, use_container_width=True,)
            
        if reset_button:
            st.session_state.clear()
            st.experimental_rerun() 
        