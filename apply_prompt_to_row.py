import openai

def apply_prompt_to_row(row, prompt, col_name, placeholder_columns, params):
    text_in = prompt
    for col in placeholder_columns:
        text_in = text_in.replace(f'[{col}]', str(row[col]))
    conversation = [{"role": "user", "content": f"{text_in}"}]
    response = openai.ChatCompletion.create(
        model=params['model'],
        messages=conversation,
        temperature=params['temperature'],
        max_tokens=params['max_tokens'],
        n=params['n'],
        top_p=params['top_p'],
        frequency_penalty=params['frequency_penalty'],
        presence_penalty=params['presence_penalty']
    )
    row[col_name] = response.choices[0].message.content
    return row



if __name__ == "__main__":
      apply_prompt_to_row()