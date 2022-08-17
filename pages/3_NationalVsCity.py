from ctypes import alignment
import streamlit as st 
import pandas as pd
import os
import matplotlib.pyplot as plt


if 'df' not in st.session_state:
    st.title("Upload Data in page_1")
else:
    sales_data = st.session_state['df']
    if sales_data is not None:
        #file_details = {"filename":data_file.name, "filetype":data_file.type,"filesize":data_file.size}
        #st.write(file_details)
        #sales_data = pd.read_csv(data_file)
        city = ['Bengaluru','Chennai','Delhi','Hyderabad','Kolkata','Mumbai','National']
        dates = sales_data['trans_date'].unique()
        dates.sort()
        dates_range = pd.date_range(dates[0],dates[-1],freq='MS').strftime("%b-%Y").tolist()
        st.title("City vs National")

        st.sidebar.header('User Input Features')
        month_to_comp = st.sidebar.selectbox("Select Month",dates_range[::-1])
        select_city_1 = st.sidebar.selectbox('City',city)
        select_city_2 = st.sidebar.selectbox('Second City',city)
        if select_city_1 != select_city_2:
            data_filter = st.radio("Comparision Basis ",('NS','Category'))
            @st.cache
            def dfs_comp_nat(month,select_city_1,select_city_2,data,data_filter):
                data['month_year'] = pd.to_datetime(data['trans_date']).dt.strftime('%b-%Y')
                data =data[data['Category'].notna()]
                data =data[data['NS'].notna()]
                if select_city_1 == 'National':
                    df1 = data[(data['month_year'] == month)]
                    df2 = data[(data['month_year'] == month) & (data['City'] == select_city_2)]
                else:
                    df1 = data[(data['month_year'] == month) & (data['City'] == select_city_1)]
                    df2 = data[(data['month_year'] == month) & (data['City'] == select_city_2)]
                
                if data_filter == 'NS':
                    df1 = df1.groupby('NS').agg({'quantity':'sum','final_price':'sum'}).reset_index()
                    df2 = df2.groupby('NS').agg({'quantity':'sum','final_price':'sum'}).reset_index()
                    df1.columns = ['NS',select_city_1 +' Quantity',select_city_1 +' Revenue']
                    df2.columns = ['NS',select_city_2+' Quantity',select_city_2 +' Revenue']
                    final_df = df1.merge(df2,on='NS')
                
                else:
                    df1 = df1.groupby('Category').agg({'quantity':'sum','final_price':'sum'}).reset_index()
                    df2 = df2.groupby('Category').agg({'quantity':'sum','final_price':'sum'}).reset_index()    
                    df1.columns = ['Category',select_city_1 +' Quantity',select_city_1 +' Revenue']
                    df2.columns = ['Category',select_city_2+' Quantity',select_city_2 +' Revenue']
                    final_df = df1.merge(df2,on='Category')
                
                base_city_quantity = select_city_1 + ' Quantity'
                base_city_revenue = select_city_1 + ' Revenue'
                comp_city_quantity = select_city_2 + ' Quantity'
                comp_city_revenue = select_city_2 + ' Revenue'    
                
                return final_df, base_city_quantity,base_city_revenue,comp_city_quantity,comp_city_revenue
            
            final_data,base_city_quantity,base_city_revenue,comp_city_quantity,comp_city_revenue = dfs_comp_nat(month_to_comp,select_city_1,select_city_2,sales_data,data_filter)
            if data_filter == 'NS':
                filt = st.selectbox('Filter by NEED STATE',final_data['NS'].unique())
                chart_data = final_data[(final_data['NS'] == filt)]
            else:
                filt = st.selectbox('Filter by Category',final_data['Category'].unique())
                chart_data = final_data[(final_data['Category'] == filt)]
                
            data_fil = st.radio("Comparision By ",('Quantity','Revenue'))
            if filt:
                if data_fil == 'Quantity':
                    chart_data = chart_data[[base_city_quantity,comp_city_quantity]]
                    chart_data_1 = chart_data.T.reset_index()
                    chart_data_1.columns = ['Name','quantity']
                    #st.dataframe(chart_data_1)
                    fig = plt.figure(figsize=(10,5))
                    plt.bar(chart_data_1['Name'],chart_data_1['quantity'])
                    st.pyplot(fig)
                else:
                    chart_data = chart_data[[base_city_revenue,comp_city_revenue]]
                    chart_data_1 = chart_data.T.reset_index()
                    chart_data_1.columns = ['Name','Revenue']
                    #st.dataframe(chart_data_1)
                    fig = plt.figure(figsize=(10,5))
                    plt.bar(chart_data_1['Name'],chart_data_1['Revenue'])
                    st.pyplot(fig)