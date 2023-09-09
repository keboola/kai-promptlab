import pandas as pd

def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)