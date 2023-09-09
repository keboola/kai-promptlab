import streamlit as st

from prompt_improvement import get_new_prompt


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
    


def main():
    st.subheader("Want to test your prompt even more?")
    st.write("See how your current prompt changes with different parameters. If you're not sure which parameter does what, the little question marks will help. :)")
    user_input = get_user_input()
    params = get_parameters()
    if st.button("Create a new promptx"):
        get_new_prompt(user_input, params)
    
if __name__ == "__main__":
    main()