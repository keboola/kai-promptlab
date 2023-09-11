### DISCLAIMER: I never said it was good code, it just somehow works 🫠
 
import streamlit as st
import openai
import base64
import os
from data_info import show_data_info
from load_data import load_data
from prompt_improvement import improve_prompt_section
from final_prompts import final_prompts_section

# from src.keboola_storage_api.connection import add_keboola_table_selection
# from src.keboola_storage_api.upload import main as upload_to_keboola

st.set_page_config(
    page_title="Keboola PromptLab",
    page_icon="static/keboola.png",
    layout="wide"
    )

logo_image = "static/keboola_logo.png"
logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 150px; margin-left: -10px;"></div>'
st.markdown(f"{logo_html}", unsafe_allow_html=True)

st.title('PromptLab 👩🏻‍🔬')

openai.api_key = st.sidebar.text_input('Enter your OpenAI API Key:',
    help= """
    You can get your own OpenAI API key by following the following instructions:
    1. Go to https://platform.openai.com/account/api-keys.
    2. Click on the __+ Create new secret key__ button.
    3. Enter an identifier name (optional) and click on the __Create secret key__ button.
    """,
    type="password",
    )

os.environ["OPENAI_API_KEY"] = openai.api_key

uploaded_file = st.sidebar.file_uploader('Upload your dataset:', type='csv')

def main():

    if uploaded_file:
        df = load_data(uploaded_file)
        st.sidebar.success("The dataset has been successfully uploaded.")
        show_data_info(df)
        improve_prompt_section()
        final_prompts_section(df)

    else:
        st.write("Please upload a dataset.")

if __name__ == "__main__":
    main()