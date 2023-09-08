### DISCLAIMER: I never said it was good code, it just somehow works 🫠

import streamlit as st
import pandas as pd
import openai
import re
import base64
import json
# from langchain.llms import OpenAI
# from kbcstorage.client import Client

st.set_page_config(page_title="Keboola PromptLab", page_icon="")

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

uploaded_file = st.sidebar.file_uploader('Upload your dataset:', type='csv')

# file_path = "/data/in/tables/full.csv"
# df = pd.read_csv(file_path)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Read me", "Playground", "Improve my prompt (adv)", "Docs"])

with tab1:
    st.write("""
             Heyo 👋 Welcome to Keboola PromptLab! 
             
             This app was created as a playground where you can try out different variations of your prompts and find the best one for your dataset. 
             
             """
    )
    st.subheader("Where to:")
    st.write("""
                           
            🤹‍♂️ __Playground__ – Try up to 3 different prompts on a sample of your dataset, have an improved version of your prompt generated or look at the output quality rating.
             
            🐙 __Improve your prompt__ – Some might call it advanced prompting – rephrase your prompt to be more specific and contextual, see how it changes with different parameters.

            📚 __Docs__ – Useful links that might come in handy.

            Your data should be uploaded from Keboola, if not you can also upload it in the left sidebar. Also fill in your OpenAI API key there, be sure to do that before you start testing your prompts.
            
             """
    )

with tab2:    

    def load_data(uploaded_file):
        df = pd.read_csv(uploaded_file)
        return df
    
    if 'improved_content' not in st.session_state:
            st.session_state.improved_content = ""

    def improve_prompt(prompt):
        create_prompt_state = st.text('Thinking... 🤯')
        conversation = [{"role": "user", "content": f"Rephrase the following prompt to be more detailed and specific, setting the context for a more informed response, while retaining its original meaning: '{prompt}'."}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.7,
            max_tokens=150
        )
        create_prompt_state.text("") 

        return response.choices[0].message.content

    if 'output_content' not in st.session_state:
            st.session_state.output_content = ""

    def apply_prompt_to_row(row, prompt, col_name, placeholder_columns, model, temperature, tokens):
        text_in = prompt
        for col in placeholder_columns:
            text_in = text_in.replace(f'[{col}]', str(row[col]))
        conversation = [{"role": "user", "content": text_in}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation,
            temperature=temperature,
            max_tokens=tokens
        )
        row[col_name] = response.choices[0].message.content
        return row

    def create(uploaded_file):
        st.sidebar.success("The dataset has been successfully uploaded.") 
        df = load_data(uploaded_file)

        st.subheader("Dataset")
        st.write("Total rows:", df.shape[0])
        df_num_show = st.number_input("Show:", min_value=0, value=5)
        st.dataframe(df.head(df_num_show))

        st.write("Total columns:", df.shape[1])
        column_names = ', '.join([f'[{col}]' for col in df.columns])
        st.write(f'Detected columns: {column_names}')

        # Improve prompt section
        st.subheader("Improve my prompt")
        st.write('Already have ideas but still not sure about the wording of your prompt?')
        input_prompt = st.text_input("", placeholder="Fill your prompt in here and click the button below :) ", label_visibility="collapsed")

        if st.button("Improve"):
            improved_output = improve_prompt(input_prompt)
            st.session_state.improved_content = improved_output

            st.write("🕺🏻 __Here's an improved version of your prompt:__")
            st.write(improved_output)

        st.subheader("Final Prompts")
        st.write('To use the values from your table, the column name must be included in the prompt as follows: [column]')
        prompts = [
            st.text_input("", placeholder='Prompt 1:', label_visibility="collapsed"),
            st.text_input("", placeholder='Prompt 2:', label_visibility="collapsed"),
            st.text_input("", placeholder='Prompt 3:', label_visibility="collapsed")
        ]

        # Extract placeholder columns from prompts
        placeholder_columns = re.findall(r'\[(.*?)\]', ''.join(prompts))

        # Check required columns in dataset
        missing_cols = [col for col in placeholder_columns if col not in df.columns]
        if missing_cols:
            st.warning(f"Your dataset is missing the following columns: {', '.join(missing_cols)}")
            st.stop()

        st.subheader("Response parameters setting")
        col1, col2, col3, col4 = st.columns(4)
        model = str(col1.selectbox("Model", ("gpt-3.5-turbo", "gpt-4")))
        temperature = float(col2.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7))
        tokens = int(col3.number_input("Max tokens", value=150))
        rows_to_use = int(col4.number_input("Number of rows", min_value=0, value=3, max_value=df.shape[0]))

        df_subset = df.head(rows_to_use)

        # Apply prompts
        if st.button('OKaaaAAAaaAYYYy LETS GO'):
            for idx, prompt in enumerate(prompts):
                if prompt:
                    apply_prompt_state = st.text('Something is cooking...')
                    df_subset = df_subset.apply(apply_prompt_to_row, args=(prompt, f'prompt_{idx+1}', placeholder_columns, model, temperature, tokens), axis=1)
                    apply_prompt_state.text("Done! 👨‍🍳")
            st.subheader("Results")
            st.table(df_subset)
        st.session_state.output_content = df_subset

    if uploaded_file:
        create(uploaded_file)
    
    else:
        st.write("Please upload a dataset.")

        
with tab3:

    def get_parameters():
        st.subheader("Parameters")

        models = [
            "gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", 
            "gpt-4", "gpt-4-0613"
        ]
        adv_model = st.selectbox("Model", models, key="set_model")

        col1, col2, col3 = st.columns(3)

        adv_max_tokens = int(col1.number_input(
            "Max tokens", min_value=0, value=150,
            help="The maximum number of [tokens](https://platform.openai.com/tokenizer) to generate in the chat completion.", 
            key="set_tokens"
        ))
        
        adv_temperature = float(col2.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.7, 
            help="Lower values for temperature result in more consistent outputs, while higher values generate more diverse and creative results. Select a temperature value based on the desired trade-off between coherence and creativity for your specific application.", 
            key="set_temp"
        ))
        
        adv_n = int(col3.number_input(
            "How many responses you want", min_value=1, value=1, 
            help="How many chat completion choices to generate for each input message.",
            key="set_n"
        ))

        col11, col12, col13 = st.columns(3)
        
        adv_top_p = float(col11.slider(
            "Top p", min_value=0.0, max_value=1.0, value=1.0, 
            help="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
            key="set_top_p"
            ))
        
        adv_presence_penalty = float(col12.slider(
            "Presence penalty", min_value=-2.0, max_value=2.0, value=0.0, 
            help="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.",
            key="set_p_penalty"
        ))

        adv_frequency_penalty = float(col13.slider(
            "Frequency penalty", min_value=-2.0, max_value=2.0, value=0.0,
            help="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
            key="set_f_penalty"
            ))
        
        return {
            'model': adv_model,
            'max_tokens': adv_max_tokens,
            'temperature': adv_temperature,
            'n': adv_n,
            'top_p': adv_top_p,
            'presence_penalty': adv_presence_penalty,
            'frequency_penalty': adv_frequency_penalty        
        }

    def get_user_input():
        return st.text_area(
            "Your current prompt:", 
            label_visibility="collapsed", 
            placeholder="Your current promp goes here.."
        )
    
    def get_new_prompt(user_input, params):
        if not user_input:
            st.warning("Please enter your current prompt.", icon='⚠️')
            return
        
        conversation = {
            "role": "user", 
            "content": f"Rephrase the following prompt to be more specific, descriptive and detailed, setting the context for a more informed response, while retaining its original meaning: '{user_input}'."}
        
        create_prompt_state = st.text('Thinking... 🤯')
        response = openai.ChatCompletion.create(
                    model=params['model'],
                    messages=[
                        {"role": "system", "content": "You are a prompt engineer."},
                        conversation
                    ],
                    temperature=params['temperature'],
                    max_tokens=params['max_tokens'],
                    n=params['n'],
                    frequency_penalty=params['frequency_penalty'],
                    presence_penalty=params['presence_penalty'],
                    top_p=params['top_p']
                )
        create_prompt_state.text("Here you go 🤓")

        for i in range(params['n']):
            st.write(response.choices[i].message.content)


    def main():
        st.subheader("Want to test your prompt even more?")
        st.write("See how your current prompt changes with different parameters. If you're not sure which parameter does what, the little question marks will help. :)")

        user_input = get_user_input()
        params = get_parameters()

        if st.button("Create a new promptx"):
            get_new_prompt(user_input, params)
            
    if __name__ == "__main__":
        main()

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
