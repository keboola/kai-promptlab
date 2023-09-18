# prompt_output.py

import streamlit as st
import pandas as pd
import re

from functions.get_parameters import get_parameters
from functions.prompt_input import prompt_input

def get_prompts(num_prompts):
    prompts_list = {}
    for i in range(num_prompts):
        prompt_input = st.text_area(
            "", 
            placeholder=f'Prompt {i+1}:', 
            label_visibility="collapsed"
        )
        prompts_list[f"prompt_{i+1}"] = prompt_input

        with st.expander(f"__Prompt {i+1} parameters setting__"):
            response_params = get_parameters(f"prompt_{i+1}")
            st.session_state[f"response_params_{i+1}"] = response_params

    return prompts_list

def prompts_out(df, dict):
    prompt_output = pd.DataFrame(index=df.index)
    
    for idx, prompt_key in enumerate(dict.keys()):
        if dict[prompt_key]:
            apply_prompt_state = st.text('Something is cooking...')
            placeholder_columns = re.findall(r'\[\[(.*?)\]\]', dict[prompt_key])
            result_series = df.apply(
                prompt_input, 
                args=(dict[prompt_key], prompt_key, placeholder_columns, st.session_state[f"response_params_{idx+1}"]),
                axis=1
            )
            prompt_output[prompt_key] = result_series[prompt_key]
            apply_prompt_state.text("Done! 👨‍🍳")
        
    return prompt_output