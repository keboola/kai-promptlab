import streamlit as st
import pandas as pd
import re

from prompt_improvement import improve_prompt
from prompt_application import apply_prompt_to_row

from langchain.evaluation import load_evaluator

def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

if 'improved_content' not in st.session_state:
        st.session_state.improved_content = ""
if 'output_content' not in st.session_state:
        st.session_state.output_content = ""

def playground(uploaded_file):
    st.sidebar.success("The dataset has been successfully uploaded.") 
    df = load_data(uploaded_file)
    st.subheader("Dataset")
    st.write("Total rows:", df.shape[0])
    df_num_show = st.number_input("Show:", min_value=0, value=5)
    st.dataframe(df.head(df_num_show))
    st.write("Total columns:", df.shape[1])
    column_names = ', '.join([f'[{col}]' for col in df.columns])
    st.write(f'Detected columns: {column_names}')
    # Improve prompt section
    st.subheader("Improve my prompt")
    st.write('Already have ideas but still not sure about the wording of your prompt?')
    input_prompt = st.text_input("", placeholder="Fill your prompt in here and click the button below :) ", label_visibility="collapsed")
    if st.button("Improve"):
        improved_output = improve_prompt(input_prompt)
        st.session_state.improved_content = improved_output
        st.write("🕺🏻 __Here's an improved version of your prompt:__")
        st.write(improved_output)
    st.subheader("Final Prompts")
    st.write('To use the values from your table, the column name must be included in the prompt as follows: [column]')
    prompts = [
        st.text_input("", placeholder='Prompt 1:', label_visibility="collapsed"),
        st.text_input("", placeholder='Prompt 2:', label_visibility="collapsed"),
        st.text_input("", placeholder='Prompt 3:', label_visibility="collapsed")
    ]
    # Extract placeholder columns from prompts
    placeholder_columns = re.findall(r'\[(.*?)\]', ''.join(prompts))
    # Check required columns in dataset
    missing_cols = [col for col in placeholder_columns if col not in df.columns]
    if missing_cols:
        st.warning(f"Your dataset is missing the following columns: {', '.join(missing_cols)}")
        st.stop()
    st.subheader("Response parameters setting")
    col1, col2, col3, col4 = st.columns(4)
    model = str(col1.selectbox("Model", ("gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4")))
    temperature = float(col2.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7))
    tokens = int(col3.number_input("Max tokens", value=150))
    rows_to_use = int(col4.number_input("Number of rows", min_value=0, value=3, max_value=df.shape[0]))
    df_subset = df.head(rows_to_use)
    # Apply prompts
    if st.button('OKaaaAAAaaAYYYy LETS GO'):
        for idx, prompt in enumerate(prompts):
            if prompt:
                apply_prompt_state = st.text('Something is cooking...')
                df_subset = df_subset.apply(apply_prompt_to_row, args=(prompt, f'prompt_{idx+1}', placeholder_columns, model, temperature, tokens), axis=1)
                apply_prompt_state.text("Done! 👨‍🍳")
                
        st.subheader("Results")
        st.dataframe(df_subset)
        evaluator = load_evaluator("pairwise_string")
    
        eval_output = evaluator.evaluate_string_pairs(
            prediction = df_subset['prompt_1'],
            prediction_b = df_subset['prompt_2'],
            input = prompt
        )
    
        st.write(eval_output)
        
    st.session_state.output_content = df_subset



if __name__ == "__main__":
    playground()
