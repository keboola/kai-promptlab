import streamlit as st
import re 

from apply_prompt_to_row import apply_prompt_to_row
from get_parameters import get_parameters
from langchain.evaluation import load_evaluator

def final_prompts_section(df):
    st.subheader("Final Prompts")
    st.write('❗️ To use the values from your table, the column name must be included in the prompt as follows: [column]')
    num_prompts = st.number_input("Choose how many prompts you want to test on a sample of your dataset", min_value=0, value=3, max_value=5)

    prompts = [st.text_area("", 
                placeholder=f'Prompt {i+1}:', 
                label_visibility="collapsed") 
                for i in range(num_prompts)
                ]

    placeholder_columns = re.findall(r'\[(.*?)\]', ''.join(prompts))

    missing_cols = [col for col in placeholder_columns if col not in df.columns]

    if missing_cols:
        st.warning(f"Your dataset is missing the following columns: {', '.join(missing_cols)}")
        st.stop()

    if 'response_params' not in st.session_state:
        st.session_state.response_params = None

    with st.expander("__Response parameters setting__"):
        st.session_state.response_params = get_parameters("response_", n=1, disable_n=True)

    rows_to_use = int(st.number_input("Number of rows", min_value=0, value=3, max_value=df.shape[0]))
    df_subset = df.head(rows_to_use)
    
    if 'output_content' not in st.session_state:
            st.session_state.response_content = []

    if st.button('OKaaaAAAaaAYYYy LETS GO'):
        for idx, prompt in enumerate(prompts):
            if prompt:
                apply_prompt_state = st.text('Something is cooking...')
                df_subset = df_subset.apply(apply_prompt_to_row, args=(prompt, f'prompt_{idx+1}', placeholder_columns, st.session_state.response_params), axis=1)
                apply_prompt_state.text("Done! 👨‍🍳")
            
        st.session_state.response_content = df_subset
        if st.session_state.response_content is not None:
            st.subheader("Results")
            st.dataframe(df_subset)

            
            evaluator = load_evaluator("pairwise_string")
            
            eval_output = evaluator.evaluate_string_pairs(
                prediction=df_subset['prompt_1'],
                prediction_b=df_subset['prompt_2'],
                input=prompt
            )
            st.write(eval_output)



if __name__ == "__main__":
    final_prompts_section()