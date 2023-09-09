# prompt_application.py
import openai
import streamlit as st

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



if __name__ == "__main__":
      apply_prompt_to_row()