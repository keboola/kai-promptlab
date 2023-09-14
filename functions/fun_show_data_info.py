# fun_show_data_info.py

import streamlit as st

def show_data_info(df):
    #st.subheader("📊 Explore") 

    color_hex = "#288CFC"
    subheader_html_hex = f"""
<h3 style="border-bottom: 2px solid {color_hex}; margin-bottom: 10px;">
    Explore
</h3>
"""
    st.markdown(subheader_html_hex, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total rows:", df.shape[0])
        
    with col2:
        st.metric("Total columns:", df.shape[1])


if __name__ == "__main__":
      show_data_info()