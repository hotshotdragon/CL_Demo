import streamlit as st
import pandas as pd

uploaded_f = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])


if uploaded_f is not None:
    df = pd.read_csv(uploaded_f)
    st.session_state['df'] = df