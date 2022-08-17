from ctypes import alignment
import streamlit as st 
import pandas as pd
import os
import matplotlib.pyplot as plt

if 'df' not in st.session_state:
    st.title("Upload Data in page_1")
else:
    final_df = st.session_state['final_df']
    #st.dataframe(final_df.head())
    base_quantity_name = st.session_state['base_quantity_name']
    base_price_name = st.session_state['base_price_name']
    comparing_quantity_name = st.session_state['comparing_quantity_name']
    comparing_price_name = st.session_state['comparing_price_name']
    data_t = st.session_state['comp_basis']
    #st.write(base_quantity_name)
    
    data_filter = st.radio("Comparision Basis ",('Quantity','Revenue'))
    if data_t == 'NS':
        filt = st.selectbox('Filter by NEED STATE',final_df['NS'].unique())
        chart_data = final_df[(final_df['NS'] == filt)]
    else:
        filt = st.selectbox('Filter by Category',final_df['Category'].unique())
        chart_data = final_df[(final_df['Category'] == filt)]
    #st.dataframe(chart_data)
    
    if data_filter == 'Quantity':
        chart_data_1 = chart_data[[base_quantity_name,comparing_quantity_name]]
        chart_data_1 = chart_data_1.T.reset_index()
        chart_data_1.columns = ['Name','quantity']
        #st.dataframe(chart_data_1)
        fig = plt.figure(figsize=(10,5))
        plt.bar(chart_data_1['Name'],chart_data_1['quantity'])
        st.pyplot(fig)
    else:
        chart_data_1 = chart_data[[base_price_name,comparing_price_name]]
        chart_data_1 = chart_data_1.T.reset_index()
        chart_data_1.columns = ['Name','Price']
        #st.dataframe(chart_data_1)
        fig = plt.figure(figsize=(10,5))
        plt.bar(chart_data_1['Name'],chart_data_1['Price'])
        st.pyplot(fig)