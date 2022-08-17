from ctypes import alignment
import streamlit as st 
import pandas as pd
import os

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

        st.title("MOM Comparision City Wise")

        st.sidebar.header('User Input Features')
        select_base_month = st.sidebar.selectbox("Compare Month",dates_range[::-1])

        select_other_month = st.sidebar.selectbox("With Month",dates_range[::-1][1:])

        select_city = st.sidebar.selectbox('City',city)

        @st.cache
        def dfs_comp(m1,m2,data,city):
            """_summary_

            Args:
                m1 (Month 1, base month): Month which is to be compared against other months 
                m2 (Month 2, comparing month): Month against which the comparision will happen
                data (DataFrame): Data in the form of DataFrame
                city (Str): _description_

            Returns:
                2 DataFrames: Returns 2 dfs for the month to be compared against the month 
                comparing with respectively
                base_month: Returns Base Month in str
                comparing_month: Returns Comparing Month in str
            """
            base_month = m1
            comparing_month = m2
            data['month_year'] = pd.to_datetime(data['trans_date']).dt.strftime('%b-%Y')
            if city == 'National':
                m1 = data[(data['month_year'] == base_month)]
                m2 = data[(data['month_year'] == comparing_month)]
            else:
                m1 = data[(data['month_year'] == base_month) & (data['City'] == city)]
                m2 = data[(data['month_year'] == comparing_month) & (data['City'] == city)]
            return m1, m2, base_month, comparing_month
        df1, df2, m1, m2 = dfs_comp(select_base_month,select_other_month,sales_data,select_city)
        
        @st.cache
        def dfs_comp_cal(m1,m2,base_month,comparing_month,overall_filt):
            """_summary_

            Args:
                m1 (DataFrame): DataFrame of Month we want to compare
                m2 (DataFrame): DataFrame of Month we want to compare against
                base_month(Str) : Base month
                comparing_month(Str) : Comparing month
            
            Returns:
                DataFrame with %Change in Quantity and Revenue
                base_quantity_name
                base_price_name
                comparing_quantity_name
                comparing_price_name
            """
            base_price_name = base_month + ' Revenue'
            base_quantity_name =  base_month + ' Quantity'
            comparing_price_name = comparing_month + ' Revenue'
            comparing_quantity_name = comparing_month + ' Quantity'
            if overall_filt == 'NS':
                m1 = m1.groupby(['month_year','NS']).agg({'quantity':'sum','final_price':'sum'}).reset_index()
                m2 = m2.groupby(['month_year','NS']).agg({'quantity':'sum','final_price':'sum'}).reset_index()
                m1.rename(columns = {'quantity':base_quantity_name,'final_price':base_price_name},inplace=True)
                m2.rename(columns = {'quantity':comparing_quantity_name,'final_price':comparing_price_name},inplace=True)
                df_final = m1.merge(m2,on='NS')
                df_final['% Change in Quantity'] = round(((df_final[base_quantity_name] - df_final[comparing_quantity_name])/df_final[comparing_quantity_name])*100,2)
                df_final['% Change in Revenue'] = round(((df_final[base_price_name] - df_final[comparing_price_name])/df_final[comparing_price_name])*100,2)
                df_final = df_final[['NS',base_quantity_name,base_price_name,comparing_quantity_name,comparing_price_name,'% Change in Quantity','% Change in Revenue']]
            else:
                m1 = m1.groupby(['month_year','Category']).agg({'quantity':'sum','final_price':'sum'}).reset_index()
                m2 = m2.groupby(['month_year','Category']).agg({'quantity':'sum','final_price':'sum'}).reset_index()
                m1.rename(columns = {'quantity':base_quantity_name,'final_price':base_price_name},inplace=True)
                m2.rename(columns = {'quantity':comparing_quantity_name,'final_price':comparing_price_name},inplace=True)
                df_final = m1.merge(m2,on='Category')
                df_final['% Change in Quantity'] = round(((df_final[base_quantity_name] - df_final[comparing_quantity_name])/df_final[comparing_quantity_name])*100,2)
                df_final['% Change in Revenue'] = round(((df_final[base_price_name] - df_final[comparing_price_name])/df_final[comparing_price_name])*100,2)
                df_final = df_final[['Category',base_quantity_name,base_price_name,comparing_quantity_name,comparing_price_name,'% Change in Quantity','% Change in Revenue']]
                
            
            return df_final, base_quantity_name,base_price_name,comparing_quantity_name,comparing_price_name
        
        data_t = st.radio("Comparision Basis ",('NS','Category'))
        final_df,base_quantity_name,base_price_name,comparing_quantity_name,comparing_price_name = dfs_comp_cal(df1,df2,m1,m2,data_t)
        st.session_state['final_df'] = final_df
        st.session_state['base_quantity_name'] = base_quantity_name
        st.session_state['base_price_name'] = base_price_name
        st.session_state['comparing_quantity_name'] = comparing_quantity_name
        st.session_state['comparing_price_name'] = comparing_price_name
        st.session_state['comp_basis'] = data_t
        if data_t == 'NS':
            filt = st.multiselect('Filter by NEED STATE',final_df['NS'].unique(),final_df['NS'].unique()[:3])
            filtered_data = final_df[(final_df.NS.isin(filt))]
        else:
            filt = st.multiselect('Filter by Category',final_df['Category'].unique(),final_df['Category'].unique()[:5])
            filtered_data = final_df[(final_df.Category.isin(filt))]
        styler = filtered_data.style.hide_index().format(decimal='.', precision=2)
        st.write(styler.to_html(), unsafe_allow_html=True)