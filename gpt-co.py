### DISCLAIMER: I never said it was good code, it just somehow works 🫠

import streamlit as st
import pandas as pd
import openai
import re
import os

from langchain.evaluation import load_evaluator


import base64
import json
from src.keboola_storage_api.connection import add_keboola_table_selection
from src.keboola_storage_api.upload import main as upload_to_keboola

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

os.environ["OPENAI_API_KEY"] = openai_api_key

add_keboola_table_selection()


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
        conversation = [{"role": "user", 
                         "content": f"""Rephrase the following prompt to be more detailed and specific, setting the context for a more informed response, while retaining its original meaning: '{prompt}'. When rephrasing the prompt, utilize these best practices: {formatted_prompt}"""}]
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
        model = str(col1.selectbox("Model", ("gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4")))
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
            st.dataframe(df_subset)

            evaluator = load_evaluator("pairwise_string")
        
            eval_output = evaluator.evaluate_string_pairs(
                prediction = df_subset['prompt_1'],
                prediction_b = df_subset['prompt_2'],
                input = prompt
            )
        
            st.write(eval_output)

            



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
        improve_prompt_prompt = """How prompt engineering works:
    Due to the way the instruction-following models are trained or the data they are trained on, there are specific prompt formats that work particularly well and align better with the tasks at hand. Below we present a number of prompt formats we find work reliably well, but feel free to explore different formats, which may fit your task best.
    
    Rules of Thumb and Examples:
    Note: the "{{text input here}}" is a placeholder for actual text/context
    
    1. Use the latest model:
    For best results, we generally recommend using the latest, most capable models. As of November 2022, the best options are the “text-davinci-003” model for text generation, and the “code-davinci-002” model for code generation.
    
    2. Put instructions at the beginning of the prompt and use ### or \"\"\" to separate the instruction and context:
    Less effective ❌:
    Summarize the text below as a bullet point list of the most important points.
    {{text input here}}
    
    Better ✅:
    Summarize the text below as a bullet point list of the most important points.
    Text: \"\"\"
    {{text input here}}
    \"\"\"
    
    3. Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc:
    Be specific about the context, outcome, length, format, style, etc.
    
    Less effective ❌:
    Write a poem about OpenAI.
    
    Better ✅:
    Write a short inspiring poem about OpenAI, focusing on the recent DALL-E product launch (DALL-E is a text to image ML model) in the style of a {{famous poet}}.
    
    4. Articulate the desired output format through examples (example 1, example 2):
    Less effective ❌:
    Extract the entities mentioned in the text below. Extract the following 4 entity types: company names, people names, specific topics and themes.
    Text: {{text}}
    Show, and tell - the models respond better when shown specific format requirements. This also makes it easier to programmatically parse out multiple outputs reliably.
    
    Better ✅:
    Extract the important entities mentioned in the text below. First extract all company names, then extract all people names, then extract specific topics which fit the content and finally extract general overarching themes.
    Desired format:
    Company names: <comma_separated_list_of_company_names>
    People names: -||-
    Specific topics: -||-
    General themes: -||-
    Text: {{text}}
    
    5. Start with zero-shot, then few-shot (example), neither of them worked, then fine-tune:
    ✅ Zero-shot
    Extract keywords from the below text.
    Text: {{text}}
    Keywords:
    
    ✅ Few-shot - provide a couple of examples
    Extract keywords from the corresponding texts below.
    Text 1: Stripe provides APIs that web developers can use to integrate payment processing into their websites and mobile applications.
    Keywords 1: Stripe, payment processing, APIs, web developers, websites, mobile applications
    ##
    Text 2: OpenAI has trained cutting-edge language models that are very good at understanding and generating text. Our API provides access to these models and can be used to solve virtually any task that involves processing language.
    Keywords 2: OpenAI, language models, text processing, API.
    ##
    Text 3: {{text}}
    Keywords 3:
    
    ✅ Fine-tune: see fine-tune best practices here.
    
    6. Reduce “fluffy” and imprecise descriptions:
    Less effective ❌:
    The description for this product should be fairly short, a few sentences only, and not too much more.
    
    Better ✅:
    Use a 3 to 5 sentence paragraph to describe this product.
    
    7. Instead of just saying what not to do, say what to do instead:
    Less effective ❌:
    The following is a conversation between an Agent and a Customer. DO NOT ASK USERNAME OR PASSWORD. DO NOT REPEAT.
    Customer: I can’t log in to my account.
    Agent:
    
    Better ✅:
    The following is a conversation between an Agent and a Customer. The agent will attempt to diagnose the problem and suggest a solution, whilst refraining from asking any questions related to PII. Instead of asking for PII, such as username or password, refer the user to the help article www.samplewebsite.com/help/faq.
    Customer: I can’t log in to my account.
    Agent:
    
    8. Code Generation Specific - Use “leading words” to nudge the model toward a particular pattern:
    Less effective ❌:
    # Write a simple python function that
    # 1. Ask me for a number in mile
    # 2. It converts miles to kilometers
    
    In this code example below, adding “import” hints to the model that it should start writing in Python. (Similarly “SELECT” is a good hint for the start of a SQL statement.)
    
    Better ✅:
    # Write a simple python function that
    # 1. Ask me for a number in mile
    # 2. It converts miles to kilometers
    import
    
    Parameters:
    Generally, we find that model and temperature are the most commonly used parameters to alter the model output.
    
    model - Higher performance models are more expensive and have higher latency.
    
    temperature - A measure of how often the model outputs a less likely token. The higher the temperature, the more random (and usually creative) the output. This, however, is not the same as “truthfulness”. For most factual use cases such as data extraction, and truthful Q&A, the temperature of 0 is best.
    
    max_tokens (maximum length) - Does not control the length of the output, but a hard cutoff limit for token generation. Ideally you won’t hit this limit often, as your model will stop either when it thinks it’s finished, or when it hits a stop sequence you defined.
    
    stop (stop sequences) - A set of characters (tokens) that, when generated, will cause the text generation to stop.
    """
        conversation = {
            "role": "user", 
            "content": f"Rephrase the following prompt to be more specific, descriptive and detailed, setting the context for a more informed response, while retaining its original meaning: '{user_input}'. When rephrasing the prompt, utilize these best practices: {improve_prompt_prompt}"}
        
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
        
        upload_to_keboola()
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
