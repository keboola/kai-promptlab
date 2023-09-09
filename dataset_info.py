import streamlit as st

def show_dataset_info(df):
    st.subheader("Dataset")
    st.write("Total rows:", df.shape[0])
    df_num_show = st.number_input("Show:", min_value=0, value=5)
    st.dataframe(df.head(df_num_show))

    st.write("Total columns:", df.shape[1])
    column_names = ', '.join([f'[{col}]' for col in df.columns])
    st.write(f'Detected columns: {column_names}')



if __name__ == "__main__":
      show_dataset_info()