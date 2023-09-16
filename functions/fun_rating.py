# fun_rating.py

import streamlit as st
import time
import openai

def rating(row, col_name, text_strings):

    for text_string in text_strings:
        prompt = f"""
        HEREA ARE THE TEXTS: 
        {text_string}

        YOUR RESPONSE:
        """
        text_in = prompt.replace("{text_string}", text_string)
        
        conversation = [
                {"role": "system", "content": """
                You are an evaluator. 
                1. Evaluate the similarity score between each pair of given texts. Calculate the score on a range of 0 to 1, where 0 indicates complete contradiction and 1 indicates nearly identical texts. 
                 
                2. Multiply those scores between each other.
                 
                3. Return only the multiplied number as a response, anything else, no explanation. 
             
                """},
                {"role": "user", "content": text_in}
        ]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=conversation,
                temperature=.5,
                max_tokens=50,
            )
            time.sleep(0.5)
            row[col_name] = response.choices[0].message.content
        except Exception as e:
            st.write(f"An error occurred: {e}")
    return row

if __name__ == "__main__":
    rating()

        
    
    
    #if 'rating_content' not in st.session_state:
     #   st.session_state.rating_content = []

    #rating_output = llm(prompt.format(text_string = [df]))

   # for text_string in df:
   # rating_output = llm(prompt.format(text_string=text_string))
                
    #st.session_state.rating_content = rating_output
                #for prompt in st.session_state.improved_content:
    #st.write(st.session_state.rating_content)

