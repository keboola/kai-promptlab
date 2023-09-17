# prompt_input.py

import streamlit as st
import openai
import time

def prompt_input(row, prompt, col_name, placeholder_columns, params):
    
    text_in = prompt
    for col in placeholder_columns:
        text_in = text_in.replace(f'[[{col}]]', str(row[col]))

    conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text_in}]
    
    try:
        response = openai.ChatCompletion.create(
            model=params['model'],
            messages=conversation,
            temperature=params['temperature'],
            max_tokens=params['max_tokens'],
            top_p=params['top_p'],
            frequency_penalty=params['frequency_penalty'],
            presence_penalty=params['presence_penalty']
        )
        time.sleep(0.5)
        row[col_name] = response.choices[0].message.content
    
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
        row[col_name] = ""
    
    return row
