### DISCLAIMER: I never said it was good code, it just somehow works 🫠
import streamlit as st
import openai
import os
from src.keboola_storage_api.connection import add_keboola_table_selection
from src.keboola_storage_api.upload import main as upload_to_keboola

st.set_page_config(page_title="Keboola PromptLab", page_icon="")

from prompt_improvement import improve_prompt, get_new_prompt
from tabs.readme import page1
from tabs.playground import playground
from tabs.playground_adv import main as playground_adv
# from langchain.llms import OpenAI
# from kbcstorage.client import Client

#logo_image = "/Users/andreanovakova/Downloads/keboolalogox.png"
#logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 100px; margin-left: -10px;"></div>'
#st.markdown(f"{logo_html}", unsafe_allow_html=True)

if not "valid_inputs_received" in st.session_state:
    st.session_state["valid_inputs_received"] = False

st.title('PromptLab 👩🏻‍🔬' )

# Use client secrets
# client = Client(st.secrets.kbc_url, st.secrets.kbc_token)

openai_api_key = st.sidebar.text_input('Enter your OpenAI API Key:',
    help= """
    You can get your own OpenAI API key by following the following instructions:
    1. Go to https://platform.openai.com/account/api-keys.
    2. Click on the __+ Create new secret key__ button.
    3. Enter an identifier name (optional) and click on the __Create secret key__ button.
    """,
    type="password",
)

openai.api_key = openai_api_key
os.environ["OPENAI_API_KEY"] = openai_api_key

#add_keboola_table_selection()

uploaded_file = st.sidebar.file_uploader('Upload your dataset:', type='csv')

# file_path = "/data/in/tables/full.csv"
# df = pd.read_csv(file_path)

tab1, tab2, tab3, tab4 = st.tabs(["Read me", 
                                  "Playground", 
                                  "Improve my prompt (adv)", 
                                  "Docs"])

with tab1:
    page1()

with tab2:    
    if uploaded_file:
        playground(uploaded_file)
    else:
        st.write("Please upload a dataset.")

with tab3:
    playground_adv()

# f"Based on prompt engineering best practices, rephrase my prompt to get more detailed and structured response. My prompt: {user_input}"
# f"Take the basic prompt '{user_input}'. Now, frame it in a more detailed and comprehensive manner, setting the context for a more informed response."
# f"Rephrase the following prompt to be more detailed and specific, setting the context for a more informed response, while retaining its original meaning: '{user_input}'."

with tab4:
    st.subheader("Documentation")
    st.write("""
            – OpenAI's [Best practices for prompt engineering](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

            – OpenAI's [Tokenizer](https://platform.openai.com/tokenizer)
             
            –

             """)
    st.write("This app was made with 💙 by [Keboola](https://www.keboola.com/) using [Streamlit](https://streamlit.io/) & [OpenAI](https://openai.com/)'s [ChatGPT](https://chat.openai.com/).")
