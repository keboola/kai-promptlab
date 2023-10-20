# show_data_info.py

import streamlit as st

def show_data_info(df):
    st.markdown(f'<h3 style="border-bottom: 2px solid #3ca0ff; ">{"Explore"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    st.info("📊 Take a look at the table you are working with. The column names are the most important – you'll need to include them in your prompts to get a response that contains your data.")

    rows, cols = st.columns(2)
    
    with rows:
        st.metric("Total rows:", df.shape[0])
        
    with cols:
        st.metric("Total columns:", df.shape[1])