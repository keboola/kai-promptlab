import streamlit as st

def show_data_info(df):
    st.header("📊 Explore") 
    col1, col2 = st.columns(2)
    
    #st.subheader("Data")
    with col1:
        st.metric("Total rows:", df.shape[0])
        #df_num_show = st.number_input("Show:", min_value=0, value=5)
    #st.dataframe(df.head(df_num_show))

    with col2:
        st.metric("Total columns:", df.shape[1])
        column_names = ', '.join([f'[{col}]' for col in df.columns])

    #st.write(f'Detected columns: {column_names}')



if __name__ == "__main__":
      show_data_info()