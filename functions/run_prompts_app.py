# run_prompts_app.py

import streamlit as st
import re 
import math
import json 

from sentence_transformers import SentenceTransformer, util
from functions.prompt_output import get_prompts, get_response

def init_session_states():
        default_params = {
            "response_params_1": {},
            "response_params_2": {},
            "response_params_3": {},
            'response_content': None,
            'rating_content': None
        }

        for key, value in default_params.items():
            if key not in st.session_state:
                st.session_state[key] = value

def check_missing_cols(df, prompts_list):
    placeholder_columns = re.findall(r'\[\[(.*?)\]\]', ''.join(prompts_list.values()))
    missing_cols = [col for col in placeholder_columns if col not in df.columns]
    
    if missing_cols:
        st.warning(f"The following columns are missing from the table: {', '.join(missing_cols)}")

# Get similarity score
def compute_similarity_product(row, num_prompts, model):
    scores = []
    sentences = [f'prompt_{i + 1}' for i in range(num_prompts)]

    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            if row[sentences[i]] == "" or row[sentences[j]] == "":
                scores.append(0)
                continue

            emb1 = model.encode(row[sentences[i]], convert_to_tensor=True)
            emb2 = model.encode(row[sentences[j]], convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(emb1, emb2)
            scores.append(similarity.item())
    
            #similarity_sum = sum(scores)
            #similarity_mean = similarity_sum / len(scores)
    
    similarity_product = math.prod(scores)        
    return math.pow(similarity_product, 1.0/len(scores))

def run_prompts_app(df):
    # Initialize session states
    init_session_states()
    
    # Run prompts UI
    st.markdown(f'<h3 style="border-bottom: 2px solid #3ca0ff; ">{"Test"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    st.info('🤹 This is your playground. Try up to 3 different prompts, or the same prompt with three different settings, it\'s up to you. However, there are some important things to keep in mind:\n1. Prompts run horizontally, you get a response(s) for each row of your table.\n2. To include data from your table, prompts must include the relevant column names in double square brackets.\n3. In the last step, don\'t forget to select how many rows of your table you want to use. ')
    
    num_prompts = st.number_input("Select number of prompts:", min_value=1, value=2, max_value=3)
    
    prompts_dict = get_prompts(num_prompts)
    check_missing_cols(df, prompts_dict)

    rows_to_use = int(st.number_input("Select how many rows of the table you want to use:", min_value=1, value=1, max_value=df.shape[0]))
    df_subset = df.head(rows_to_use)
    
    # Get responses
    if st.button('OKaaaAAAaaAYYYy LETS GO 🎢'):
        prompt_output = get_response(df_subset, prompts_dict)
        st.session_state["response_content"] = prompt_output
        
    # Show responses
    if st.session_state["response_content"] is not None:

        st.markdown(f'<h3 style="border-bottom: 2px solid #3ca0ff; ">{"Responses"}</h3>', unsafe_allow_html=True)
        st.text(" ")
        st.info("🔍 Check out the responses and see which prompt fits your data best. You can also check the responses similarity score to pinpoint areas where prompts might seem contradictory. This is a great way to refine your prompts and understand potential model challenges.")
        st.dataframe(st.session_state["response_content"], use_container_width=True, hide_index=True)
    
    # Rate, download, reset
        rate_button, get_button, reset_button = st.columns(3)
        with rate_button: 
            rate_click = st.button('Check responses similarity', use_container_width=True, disabled=(num_prompts == 1))
        
        with get_button: 
            prompts_list = [{"name": key, "message": value} for key, value in prompts_dict.items()]
            params_list = []
            for i in range(num_prompts):
                param_key = f"response_params_{i+1}"
                if param_key in st.session_state:
                    params_list.append(st.session_state[param_key])
            combined_strings = []
            for prompt_dict, param_dict in zip(prompts_list, params_list):
                combined_data = {**prompt_dict, **param_dict}
                combined_strings.append(json.dumps(combined_data, indent=2))
            prompts_download = '\n\n'.join(combined_strings)
            st.download_button('Download prompts', prompts_download, use_container_width=True)
    
        with reset_button:
            reset_click = st.button('Reset app', use_container_width=True)
        
        # Rate reponses 
        if rate_click:
            rating_input = st.session_state["response_content"].copy()
            model = SentenceTransformer('paraphrase-MiniLM-L6-v2') 
            rating_input["similarity_score"] = rating_input.apply(lambda row: compute_similarity_product(row, num_prompts, model), axis=1)
            cols = ['similarity_score'] + [col for col in rating_input if col != 'similarity_score']
            rating_input = rating_input[cols]
            st.session_state['rating_content'] = rating_input

            st.markdown(f'<h3 style="border-bottom: 2px solid #3ca0ff; ">{"Similarity"}</h3>', unsafe_allow_html=True)
            st.text(" ")
            st.info("🥇 The closer the score is to 1, the higher the similarity between the responses.")
            st.dataframe(st.session_state['rating_content'], use_container_width=True, hide_index=True)

        if reset_click:
            st.session_state.clear()
            st.experimental_rerun()