# run_prompts_app.py

import streamlit as st
import re 
import math

from sentence_transformers import SentenceTransformer, util
from functions.prompt_output import get_prompts, prompts_out

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

def run_prompts_app(df):
    
    init_session_states()
    
    # Run prompts
    st.markdown(f'<h3 style="border-bottom: 2px solid #288CFC; ">{"Test"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    
    num_prompts = st.number_input("Select number of prompts:", min_value=1, value=2, max_value=3)
    st.write('To use values from your table, put the column name in double square brackets, e.g. "[[column_name]]".')
    
    prompts_list = get_prompts(num_prompts)
    placeholder_columns = re.findall(r'\[\[(.*?)\]\]', ''.join(prompts_list.values()))

    missing_cols = [col for col in placeholder_columns if col not in df.columns]
    if missing_cols:
        st.warning(f"The following columns are missing from the table: {', '.join(missing_cols)}")

    rows_to_use = int(st.number_input("Select how many rows of the table you want to use:", min_value=1, value=1, max_value=df.shape[0]))
    df_subset = df.head(rows_to_use)
    
    if st.button('OKaaaAAAaaAYYYy LETS GO 🎢'):
        prompt_output = prompts_out(df_subset, prompts_list)
        st.session_state["response_content"] = prompt_output
        
    # Display results 
    if st.session_state["response_content"] is not None:

        st.markdown(f'<h3 style="border-bottom: 2px solid #288CFC; ">{"Responses"}</h3>', unsafe_allow_html=True)
        st.text(" ")
        st.dataframe(st.session_state["response_content"], use_container_width=True)

        rate_button, get_button, reset_button = st.columns(3)
        with rate_button: 
            rate_click = st.button('Check responses similarity', use_container_width=True, disabled=(num_prompts == 1))
        with get_button: 
            prompts_download = str(prompts_list)
            st.download_button('Download prompts', prompts_download, use_container_width=True)
        with reset_button:
            reset_click = st.button('Reset app', use_container_width=True)
        
        # Rate reponses 
        if rate_click:
            
            rating_input = st.session_state["response_content"].copy()
            model = SentenceTransformer('paraphrase-MiniLM-L6-v2') 
            
            def compute_similarity_product(row, num_prompts):
                scores = []
                sentences = [f'prompt_{i+1}' for i in range(num_prompts)]
        
                for i in range(len(sentences)):
                    for j in range(i+1, len(sentences)):
                        
                        if row[sentences[i]] == "" or row[sentences[j]] == "":
                            scores.append(0)
                            continue

                        emb1 = model.encode(row[sentences[i]], convert_to_tensor=True)
                        emb2 = model.encode(row[sentences[j]], convert_to_tensor=True)
                        similarity = util.pytorch_cos_sim(emb1, emb2)
                        scores.append(similarity.item())
               
                #similarity_sum = sum(scores)
                #similarity_mean = similarity_sum / len(scores)
                
                similarity_product = 1
                for score in scores:
                    similarity_product *= score   
                geometric_mean = math.pow(similarity_product, 1.0/len(scores))
                
                return geometric_mean

            rating_input["similarity_score"] = rating_input.apply(lambda row: compute_similarity_product(row, num_prompts), axis=1)
            cols = ['similarity_score'] + [col for col in rating_input if col != 'similarity_score']
            
            rating_input = rating_input[cols]
            st.session_state['rating_content'] = rating_input
            
            if st.session_state['rating_content'] is not None:
                st.markdown(f'<h3 style="border-bottom: 2px solid #288CFC; ">{"Rating"}</h3>', unsafe_allow_html=True)
                st.text(" ")
                st.write("The closer the score is to 1, the higher the similarity between the responses.")
                st.dataframe(st.session_state['rating_content'], use_container_width=True)

        if reset_click:
            st.session_state.clear()
            st.experimental_rerun()