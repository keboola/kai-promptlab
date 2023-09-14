# fun_process_rating_input.py

def process_rating_input(df):

    result_strings = []

    for index, row in df.iterrows():
        row_string = []
        for index, value in enumerate(row):
            row_string.append(f'Text {index + 1}: "{value}"')
        result_strings.append('\n\n'.join(row_string))
    
    return result_strings
