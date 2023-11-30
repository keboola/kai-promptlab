# show_data_info.py

import streamlit as st

def show_data_info(df):
    st.markdown(f'<h3 style="border-bottom: 2px solid #3ca0ff; ">{"Explore"}</h3>', 
                unsafe_allow_html=True)
    st.text(" ")
    
    test_info = "📊 Take a look at the table you are working with. The column names are the most important – you'll need to include them in your prompts to get a response that contains your data."
    st.markdown(f'<p style="background-color:rgba(244,249,254,255);color:#283338;font-size:16px;border-radius:10px;padding:15px;">{test_info}</p>', unsafe_allow_html=True)

    rows, cols = st.columns(2)
    
    with rows:
        st.metric("Total rows:", df.shape[0])
        
    with cols:
        st.metric("Total columns:", df.shape[1])