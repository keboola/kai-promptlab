# sec_rating_responses.py

import streamlit as st

from functions.fun_process_rating_input import process_rating_input
from functions.fun_rating import rating


def rating_responses(df):
    col1, col2 = st.columns(2)
    if col1.button("Rate your results"):
        var = process_rating_input(df)
        prompt_output_w_rating = df.apply(rating, args=("similarity score", var), axis=1)
        rated_results = prompt_output_w_rating
        st.subheader("Rated results")
        st.dataframe(rated_results)
    if col2.button("Get results to Keboola"):
        st.write("Not yet possible, sorry:))")