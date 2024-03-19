import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(layout="wide")
engine = create_engine('mysql+pymysql://root:@localhost/phonepeanalytics_db')

def get_unique_state(table_name):
    state_query = f"SELECT DISTINCT State FROM {table_name}"
    state_df = pd.read_sql(state_query, engine)
    return state_df['State'].tolist()

def get_unique_year(table_name):
    year_query = f"SELECT DISTINCT Year FROM {table_name}"
    years_df = pd.read_sql(year_query, engine)
    return years_df['Year'].tolist()

def get_unique_quarter(table_name):
    quarter_query = f"SELECT DISTINCT Quarter FROM {table_name}"
    quarter_df = pd.read_sql(quarter_query, engine)
    return quarter_df['Quarter'].tolist()

def fetch_data(table_name, column_name, value):
    query = f"SELECT * FROM {table_name} WHERE {column_name} = '{value}'"
    df = pd.read_sql(query, engine)
    return df

def home_page():
    image = "https://logolook.net/wp-content/uploads/2022/12/PhonePe-Logo.png"
    st.image(image, width=400)
    st.markdown("# Data Visualization and Exploration")
    st.markdown("## :grey[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.markdown("### :grey[Technologies used : ]:blue[Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.]")
        st.markdown("### :grey[Overview : ]:blue[In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.]")
        st.write(" ")
        st.write(" ")


def data_exploration():
    selected_option = st.selectbox("Select an option", ["Transaction", "User", "Geo Analysis"])

    if selected_option=="Transaction":
        total_transaction_query = "SELECT SUM(Transaction_amount) AS Total_Transaction_Amount,SUM(Transaction_count) AS Total_Transaction  FROM aggregated_transactions"
        total_transaction_df = pd.read_sql(total_transaction_query, engine)
        total_transaction_amount = total_transaction_df.iloc[0]['Total_Transaction_Amount']
        average_transaction_value = total_transaction_amount / total_transaction_df.iloc[0]['Total_Transaction']

        
        st.write("**Transactions**")
        st.write("**All PhonePe transactions (UPI + Cards + Wallets)**")
        st.write(f"{total_transaction_amount:,.2f}", unsafe_allow_html=True)
        st.write(f"₹{total_transaction_amount / 1e9:.2f} Cr")
        st.write("**Avg. transaction value**")
        st.write(f"{'₹' + str(int(average_transaction_value))}")

        tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

        with tab1:
            st.subheader("Aggregate Data")
            agg_years = get_unique_year("aggregated_transactions")
        
            Year = st.selectbox("Select Year for aggregiater", agg_years)
            df = fetch_data('aggregated_transactions','Year',Year)
            filtered_agg_df = df[df['Year'] == Year]

            transaction_type_year = filtered_agg_df.groupby(['Transaction_type'])[['Transaction_amount','Transaction_count']].sum().reset_index()
            
            agg_trans_fig1 = px.bar(transaction_type_year, x='Transaction_type', y='Transaction_count', color='Transaction_type',
                        title='Transaction type and Transaction Count  for Each Year',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            agg_trans_fig2 = px.bar(transaction_type_year, x='Transaction_type', y='Transaction_amount', color='Transaction_type',
                        title='Transaction type and Transaction Amount for Each Year',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)

            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(agg_trans_fig1,use_container_width=True)
            with col2:
                st.plotly_chart(agg_trans_fig2,use_container_width=True)


            quarter_list = get_unique_quarter('aggregated_transactions')

            selected_quarter = st.selectbox("Select Quarter for aggregiater", quarter_list)
            qua = fetch_data('aggregated_transactions','Quarter',selected_quarter)
            filtered_qua = qua[qua['Quarter'] == selected_quarter]

            
            transaction_type_quarter = filtered_qua.groupby(['Transaction_type'])[['Transaction_amount','Transaction_count']].sum().reset_index()
            
            fig3 = px.bar(transaction_type_quarter, x='Transaction_type', y='Transaction_count', color='Transaction_type',
                        title='Transaction type and Transaction Count for Each Quarter',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            fig4 = px.bar(transaction_type_quarter, x='Transaction_type', y='Transaction_count', color='Transaction_type',
                        title='Transaction type and Transaction Amount for Each Quarter',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(fig3,use_container_width=True)
            with col4:
                st.plotly_chart(fig4,use_container_width=True)

            state_list = get_unique_state('aggregated_transactions')
            selected_state = st.selectbox("Select state for aggregiater", state_list)
            sta = fetch_data('aggregated_transactions','State',selected_state)
            filtered_sta = sta[sta['State'] == selected_state]

            transaction_type_state = filtered_sta.groupby(['Transaction_type'])[['Transaction_amount','Transaction_count']].sum().reset_index()
            

            fig5 = px.pie(transaction_type_state, values='Transaction_count', names='Transaction_type',
                title='Transaction Count by State for Each Quarter', width=700)
            
            fig6 = px.pie(transaction_type_state, values='Transaction_amount', names='Transaction_type',
                title='Transaction Amount by State for Each Quarter', width=700)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(fig5,use_container_width=True)
            with col6:
                st.plotly_chart(fig6,use_container_width=True)


        with tab2:
            st.subheader("Map Data")
            map_years = get_unique_year('map_transactions')

            year = st.selectbox("Select Year for map", map_years)
            map = fetch_data('map_transactions','Year',year)
            filtered_map = map[map['Year'] == year]

            map_transaction_amount = filtered_map.groupby(['Year', 'State'])[['Transaction_amount','Transaction_count']].sum().reset_index()
            
            map_fig1 = px.bar(map_transaction_amount, x='State', y='Transaction_amount', color='State',
              title='Transaction Amount for Each Year',
              labels={'Transaction_amount': 'Transaction Amount', 'State': 'State'},
              width=700)

            map_fig2 = px.bar(map_transaction_amount, x='State', y='Transaction_count', color='State',
                        title='Transaction Count for Each Year',
                        labels={'Transaction_count': 'Transaction Count', 'State': 'State'},
                        width=700)            
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(map_fig1,use_container_width=True)
            with col2:
                st.plotly_chart(map_fig2,use_container_width=True)

            quarter1_list = get_unique_quarter('map_transactions')

            selected_quarter1 = st.selectbox("Select Quarter for map", quarter1_list)
            qua1 = fetch_data('map_transactions','Quarter',selected_quarter1)
            filtered_qua1 = qua1[qua1['Quarter'] == selected_quarter1]

            
            map_transaction_amount = filtered_qua1.groupby(['Quarter', 'State'])['Transaction_amount'].sum().reset_index()
            map_transaction_count = filtered_qua1.groupby(['Quarter', 'State'])['Transaction_count'].sum().reset_index()

            
            map3 = px.bar(map_transaction_amount, x='State', y='Transaction_amount', color='Quarter',
                        title='Transaction_amount by map for Each Quarter',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            map4 = px.bar(map_transaction_count, x='State', y='Transaction_count', color='Quarter',
                        title='Transaction_count by map for Each Quarter',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(map3,use_container_width=True)
            with col4:
                st.plotly_chart(map4,use_container_width=True)

            state_list1 = get_unique_state('map_transactions')
            selected_state1 = st.selectbox("Select state for map", state_list1)
            stae = fetch_data('map_transactions','State',selected_state1)
            filtered_sta1 = stae[stae['State'] == selected_state1]

            map_transaction_amount = filtered_sta1.groupby(['Quarter', 'State'])['Transaction_amount'].sum().reset_index()
            map_transaction_count = filtered_sta1.groupby(['Quarter', 'State'])['Transaction_count'].sum().reset_index()

            map5 = px.pie(map_transaction_amount, values='Transaction_amount', names='Quarter',
                title='Transaction_amount by map for Each Quarter', width=700)
            
            map6 = px.pie(map_transaction_count, values='Transaction_count', names='Quarter',
                title='Transaction_count by map for Each Quarter', width=700)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(map5,use_container_width=True)
            with col6:
                st.plotly_chart(map6,use_container_width=True)


        with tab3:
            st.subheader("Top Data")
            top_year = get_unique_year('top_transactions')
            year = st.selectbox("Select Year for tp", top_year)
            top = fetch_data('top_transactions','Year',year)
            filtered_top = top[top['Year'] == year]

            top_transaction_amount = filtered_top.groupby(['Year', 'State'])['Transaction_amount'].sum().reset_index()
            top_transaction_count = filtered_top.groupby(['Year', 'State'])['Transaction_count'].sum().reset_index()

            top_fig1 = px.bar(top_transaction_amount, x='State', y='Transaction_amount', color='Year',
                        title='Transaction_amount for Each Year',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            top_fig2 = px.bar(top_transaction_count, x='State', y='Transaction_count', color='Year',
                        title='Transaction_count for Each Year',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(top_fig1,use_container_width=True)
            with col2:
                st.plotly_chart(top_fig2,use_container_width=True) 

            quarter2_list = get_unique_quarter('top_transactions')

            selected_quarter2 = st.selectbox("Select Quarter for top", quarter2_list)
            qua2 = fetch_data('top_transactions','Quarter',selected_quarter2)
            filtered_qua2 = qua2[qua2['Quarter'] == selected_quarter2]

           
            top_transaction_amount = filtered_qua2.groupby(['Quarter', 'State'])['Transaction_amount'].sum().reset_index()
            top_transaction_count = filtered_qua2.groupby(['Quarter', 'State'])['Transaction_count'].sum().reset_index()

            
            top3 = px.bar(top_transaction_amount, x='State', y='Transaction_amount', color='Quarter',
                        title='Transaction_amount by map for Each Quarter',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            top4 = px.bar(top_transaction_count, x='State', y='Transaction_count', color='Quarter',
                        title='Transaction_count by map for Each Quarter',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(top3,use_container_width=True)
            with col4:
                st.plotly_chart(top4,use_container_width=True)   

            state_list2 = get_unique_state('top_transactions')
            selected_state2 = st.selectbox("Select state for top", state_list2)
            staes = fetch_data('top_transactions','State',selected_state2)
            filtered_sta2 = staes[staes['State'] == selected_state2]

            top_transaction_amount = filtered_sta2.groupby(['Quarter', 'State'])['Transaction_amount'].sum().reset_index()
            top_transaction_count = filtered_sta2.groupby(['Quarter', 'State'])['Transaction_count'].sum().reset_index()

            top5 = px.pie(top_transaction_amount, values='Transaction_amount', names='Quarter',
                title='Transaction_amount by top for Each Quarter', width=700)
            
            top6 = px.pie(top_transaction_count, values='Transaction_count', names='Quarter',
                title='Transaction_count by top for Each Quarter', width=700)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(top5,use_container_width=True)
            with col6:
                st.plotly_chart(top6,use_container_width=True)

    elif selected_option=="User":
        total_users_query = "SELECT SUM(User_count) AS User_count FROM aggregated_users"
        total_users_df = pd.read_sql(total_users_query, engine)
        total_User_count = total_users_df.iloc[0]['User_count']
        
        st.write("All PhonePe users ")
        st.write(f"{total_User_count}")
        tab4, tab5, tab6= st.tabs(["Aggregated user Analysis", "Map user Analysis", "Top user Analysis"])
        
        with tab4:
            st.subheader("Aggregate user Data")
            agg_user_year = get_unique_year("aggregated_users")
        
            selected_year = st.selectbox("Select Year for ag user", agg_user_year)
            agr_users = fetch_data('aggregated_users','Year',selected_year)
            filtered_agr_users = agr_users[agr_users['Year'] == selected_year]
            state_user_counts = filtered_agr_users.groupby(['Year', 'State'])['User_count'].sum().reset_index()
            state_total_users = filtered_agr_users.groupby(['Year'])['User_count'].sum().reset_index()
            state_user_counts = state_user_counts.merge(state_total_users, on='Year', suffixes=('_state', '_total'))

            state_user_counts['User_percentage'] = (state_user_counts['User_count_state'] / state_user_counts['User_count_total']) * 100

            user1 = px.line(state_user_counts, x='State', y='User_percentage', color='Year',
                title='User Percentage by State for Each Year',
                labels={'User_percentage': 'User Percentage', 'State': 'State'}, width=700)
            
            state_user_count = filtered_agr_users.groupby(['Year', 'State'])['User_count'].sum().reset_index()
            user2 = px.bar(state_user_count, x='State', y='User_count', color='Year',
                        title='User_count by State for Each Year',
                        labels={'User_count': 'User_count', 'State': 'State'},width=700)

            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(user1,use_container_width=True)
            with col2:
                st.plotly_chart(user2,use_container_width=True)

            agg_quarter_list = get_unique_quarter('aggregated_users')

            agg_user_selected_quarter = st.selectbox("Select Quarter for aggregated users", agg_quarter_list)
            agg_user_df = fetch_data('aggregated_users','Quarter',agg_user_selected_quarter)
            filtered_qua = agg_user_df[agg_user_df['Quarter'] == agg_user_selected_quarter]

            
            state_user_coun = filtered_agr_users.groupby(['Quarter', 'State'])['User_count'].sum().reset_index()
            state_total_user = filtered_agr_users.groupby(['Quarter'])['User_count'].sum().reset_index()
            state_user_coun = state_user_coun.merge(state_total_user, on='Quarter', suffixes=('_state', '_total'))

            
            state_user_coun['User_percentage'] = (state_user_coun['User_count_state'] / state_user_coun['User_count_total']) * 100

            
            agg_user_fig1 = px.bar(state_user_coun, x='State', y='User_percentage',
                title='User Percentage by State for Each Quarter',
                labels={'User_percentage': 'User Percentage', 'State': 'State'}, width=700)
            
            
            state_transaction_count1 = filtered_qua.groupby(['Quarter', 'State'])['User_count'].sum().reset_index()
            agg_user_fig2 = px.bar(state_transaction_count1, x='State', y='User_count',
                title='User_count by State for Each Quarter',
                labels={'Transaction_count': 'User_count', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)

            with col3:
                st.plotly_chart(agg_user_fig1,use_container_width=True)
            with col4:
                st.plotly_chart(agg_user_fig2,use_container_width=True)

            state_list = get_unique_state('aggregated_users')
            selected_state = st.selectbox("Select state for aggregiater users", state_list)
            sta = fetch_data('aggregated_users','State',selected_state)
            filtered_sta = sta[sta['State'] == selected_state]

            state_transaction_amount = filtered_sta.groupby(['Quarter', 'State'])['User_percentage'].sum().reset_index()
            state_transaction_count = filtered_sta.groupby(['Quarter', 'State'])['User_count'].sum().reset_index()

            fig5 = px.pie(state_transaction_amount, values='User_percentage', names='Quarter',
                title='User Percentage by State for Each Quarter', width=700)
            fig6 = px.pie(state_transaction_count, values='User_count', names='Quarter',
                title='User_count by State for Each Quarter', width=700)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(fig5,use_container_width=True)
            with col6:
                st.plotly_chart(fig6,use_container_width=True)



        with tab5:
            st.subheader("Map user Analysis")
            map_user_year = get_unique_year("map_users")

            map_year = st.selectbox("Select Year for map", map_user_year)
            map = fetch_data('map_users','Year',map_year)
            filtered_map = map[map['Year'] == map_year]

            state_registered_user = filtered_map.groupby(['Year', 'State'])['Registerted_users'].sum().reset_index()
            state_app_open = filtered_map.groupby(['Year', 'State'])['App_opens'].sum().reset_index()

            map1 = px.bar(state_registered_user, x='State', y='Registerted_users', color='Year',
                        title='Registerted_users for Each Year',
                        labels={'Registerted_users': 'Registerted_users', 'State': 'State'},width=700)
            
            map2 = px.bar(state_app_open, x='State', y='App_opens', color='Year',
                        title='App_opens for Each Year',
                        labels={'App_opens': 'App_opens', 'State': 'State'},width=700)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(map1,use_container_width=True)
            with col2:
                st.plotly_chart(map2,use_container_width=True)

            
            map_quarter_list = get_unique_quarter('map_users')

            map_selected_quarter = st.selectbox("Select Quarter for map", map_quarter_list)
            filtered_map_users_df = fetch_data('map_users','Quarter',map_selected_quarter)
            filtered_map_users= filtered_map_users_df[filtered_map_users_df['Quarter'] == map_selected_quarter]

            map_registered_user = filtered_map_users.groupby(['Quarter', 'State'])['Registerted_users'].sum().reset_index()
            map_registered_count = filtered_map_users.groupby(['Quarter', 'State'])['App_opens'].sum().reset_index()

            map_user_fig1 = px.bar(map_registered_user, x='State', y='Registerted_users', 
                        title='Registered_users by map for Each Quarter',
                        labels={'Registerted_users': 'Registerted_users', 'State': 'State'},width=700)
            
            map_user_fig2 = px.bar(map_registered_count, x='State', y='App_opens',
                        title='App_opens by map for Each Quarter',
                        labels={'App_opens': 'App_opens', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(map_user_fig1,use_container_width=True)
            with col4:
                st.plotly_chart(map_user_fig2,use_container_width=True)

            state_list1 = get_unique_state('map_users')
            selected_state1 = st.selectbox("Select state for map", state_list1)
            stae = fetch_data('map_users','State',selected_state1)
            filtered_sta1 = stae[stae['State'] == selected_state1]

            map_user = filtered_sta1.groupby(['Quarter', 'State'])['Registerted_users'].sum().reset_index()
            map_count = filtered_sta1.groupby(['Quarter', 'State'])['App_opens'].sum().reset_index()

            map5 = px.pie(map_user, values='Registerted_users', names='Quarter',
                title='Registerted_users by map for Each Quarter', width=700)
            
            map6 = px.pie(map_count, values='App_opens', names='Quarter',
                title='App_opens by map for Each Quarter', width=700)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(map5,use_container_width=True)
            with col6:
                st.plotly_chart(map6,use_container_width=True)

        with tab6:
            st.subheader("Top user Analysis")
            top_user_year= get_unique_year("top_users")
            top_year = st.selectbox("Select Year for top user", top_user_year)
            top = fetch_data('top_users','Year',top_year)
            filtered_top = top[top['Year'] == top_year]

            top_registerd_users = filtered_top.groupby(['Year', 'State'])['Registerted_users'].sum().reset_index()
            top_District_name = filtered_top.groupby(['Year', 'City_name'])['Registerted_users'].sum().reset_index()

            top_fig1 = px.bar(top_registerd_users, x='State', y='Registerted_users', color='Year',
                        title='Registerted_users for Each Year',
                        labels={'Registerted_users': 'Registerted_users', 'State': 'State'},width=700)
            
            top_fig2 = px.bar(top_District_name, x='City_name', y='Registerted_users', color='Year',
                        title='District_name for Each Year',
                        labels={'City_name': 'City_name', 'State': 'State'},width=700)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(top_fig1,use_container_width=True)
            with col2:
                st.plotly_chart(top_fig2,use_container_width=True) 


            quarter2_list = get_unique_quarter('top_users')

            selected_quarter2 = st.selectbox("Select Quarter for top users", quarter2_list)
            qua2 = fetch_data('top_users','Quarter',selected_quarter2)
            filtered_qua2 = qua2[qua2['Quarter'] == selected_quarter2]

            
            top_user_state = filtered_qua2.groupby(['Quarter', 'State'])['Registerted_users'].sum().reset_index()
            top_user_district = filtered_qua2.groupby(['Quarter', 'City_name'])['Registerted_users'].sum().reset_index()

            
            top3 = px.bar(top_user_state, x='State', y='Registerted_users',
                        title='Registerted_users by map for Each Quarter',
                        labels={'Registerted_users': 'Registerted_users', 'State': 'State'},width=700)
            
            top4 = px.bar(top_user_district, x='City_name', y='Registerted_users',
                        title='Registerted_users by map for Each Quarter',
                        labels={'Registerted_users': 'Registerted_users', 'City_name': 'City_name'},width=700)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(top3,use_container_width=True)
            with col4:
                st.plotly_chart(top4,use_container_width=True)   

            state_list2 = get_unique_state('top_users')
            selected_state2 = st.selectbox("Select state for top", state_list2)
            staes = fetch_data('top_users','State',selected_state2)
            filtered_sta2 = staes[staes['State'] == selected_state2]

            top_ud = filtered_sta2.groupby(['Quarter', 'State'])['Registerted_users'].sum().reset_index()
            top_dc= filtered_sta2.groupby(['Quarter', 'City_name'])['Registerted_users'].sum().reset_index()

            top5 = px.pie(top_ud, values='Registerted_users', names='Quarter',
                title='Transaction_amount by top for Each Quarter', width=700)
            
            top6 = px.pie(top_dc, values='Registerted_users', names='Quarter',
                title='Transaction_count by top for Each Quarter', width=700)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(top5,use_container_width=True)
            with col6:
                st.plotly_chart(top6,use_container_width=True)

    else:
        st.title("Geo Map")
        st.subheader("Total Tansaction Amount State wise")
        generate_choropleth("SELECT SUM(Transaction_amount) as TransactionAmount, State FROM aggregated_transactions GROUP BY State", 'State', 'TransactionAmount')

        st.subheader("Total User Count State wise")
        generate_choropleth("SELECT sum(User_count) as User, User_brand as Brand, State FROM `aggregated_users` GROUP BY User_brand, State", 'State', 'User')

        st.subheader("Total Register User Count State wise")
        generate_choropleth("SELECT SUM(Registerted_users) AS Users, State, District_name  FROM `map_users` GROUP BY State, District_name", 'State', 'Users', {'State': True, 'District_name': True, 'Users': True})

        st.subheader("Top transaction amount State wise")
        generate_choropleth("SELECT State, SUM(Transaction_amount) AS TranactionAmount, SUM(Transaction_count) AS TransactionCount FROM `top_transactions` GROUP BY State", 'State', 'TranactionAmount', {'State': True, 'TranactionAmount': True, 'TransactionCount': True})

def generate_choropleth(query, location_column, color_column, hover_data=None):
    df = pd.read_sql(query, engine)
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations=location_column,
        color=color_column,
        color_continuous_scale='Blues',
        hover_data=hover_data
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True, width=800, height=600)
    
def question1():
    query = "SELECT State, Year, SUM(Transaction_amount) AS TransactionAmount FROM aggregated_transactions WHERE Year IN (2020, 2023) GROUP BY State, Year ORDER BY TransactionAmount DESC LIMIT 10"
    highest_transaction_state = pd.read_sql(query, engine)
    a = highest_transaction_state.groupby(['Year', 'State'])['TransactionAmount'].sum().reset_index()        
    ans1 = px.bar(a, x='State', y='TransactionAmount', color='Year',
                title='Highest Transaction States',
                labels={'TransactionAmount': 'Transaction Amount', 'State': 'State'}, width=700)
    
    return st.plotly_chart(ans1, use_container_width=True)

def question2():
    query1 = "SELECT State, Year, Transaction_type, SUM(Transaction_amount) AS TransactionAmount FROM aggregated_transactions WHERE Year IN (2020, 2023) GROUP BY State, Year, Transaction_type ORDER BY TransactionAmount DESC LIMIT 10"
    highest_transactions_state = pd.read_sql(query1, engine)
    
    ans2 = px.bar(highest_transactions_state, x='State', y='TransactionAmount', color='Transaction_type',facet_col='Year', facet_col_wrap=1,
                title='Top 10 Transaction Amount by State and Type',
                labels={'TransactionAmount': 'Transaction Amount', 'State': 'State'}, width=700)
    
    return st.plotly_chart(ans2, use_container_width=True) 

def question3():
    query2 = "SELECT State,User_brand as Mobile,SUM(User_count) as User FROM `aggregated_users` WHERE YEAR IN (2020,2023) GROUP BY State ORDER BY User DESC LIMIT 10"
    highest_mobile = pd.read_sql(query2, engine)

    ans3 = px.bar(highest_mobile, x='State', y='User', color='Mobile',
                title='Top 10 state Mobile barnd',
                labels={'User_count': 'User Count', 'State': 'State'}, width=700)
    return st.plotly_chart(ans3, use_container_width=True) 

def question4():
    query3 = "SELECT State, SUM(Transaction_amount) as Transaction_amount FROM `aggregated_transactions` GROUP BY State"
    highest_mobile = pd.read_sql(query3, engine)

    ans4 = px.bar(highest_mobile, x='State', y='Transaction_amount', color='Transaction_amount',
                title='Top 10 state Mobile barnd',
                labels={'Transaction_amount': 'Transaction amount', 'State': 'State'}, width=700)
    return st.plotly_chart(ans4, use_container_width=True) 


def question5():
   
    query = "SELECT City_name as City, State, sum(Registerted_users) AS UserCount FROM top_users GROUP BY City_name, State ORDER BY Registerted_users DESC"
    top_users_by_city = pd.read_sql(query, engine)
    top_users_by_city_state = top_users_by_city.groupby(['State', 'City'])['UserCount'].sum().reset_index()
    selected_state = st.selectbox('Select State', top_users_by_city_state['State'].unique())
    filtered_data = top_users_by_city_state[top_users_by_city_state['State'] == selected_state]
    pivot_data = filtered_data.pivot(index='City', columns='State', values='UserCount')
    
    fig = px.imshow(pivot_data, labels=dict(x="State", y="City", color="Number of Users"),
                    x=pivot_data.columns, y=pivot_data.index, color_continuous_scale='Viridis',
                    title=f'Registered Users by City in {selected_state}')
    
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig, use_container_width=True)

def question6():

    query = "SELECT State, Year, SUM(Transaction_amount) AS TransactionAmount FROM aggregated_transactions WHERE State = 'Tamil Nadu' GROUP BY Year,State ORDER BY TransactionAmount DESC"
    
    highest_transaction_state = pd.read_sql(query, engine)
    
    fig = px.bar(highest_transaction_state, x='Year', y='TransactionAmount', color='State',
                 title='Top 15 Transaction Amounts in Tamil Nadu',
                 labels={'TransactionAmount': 'Transaction Amount', 'Year': 'Year'})
    
    st.plotly_chart(fig, use_container_width=True)

def question7():
    query7 = "SELECT State, SUM(Transaction_amount) AS TotalTransactionAmount FROM aggregated_transactions GROUP BY State ORDER BY TotalTransactionAmount DESC LIMIT 10"
    top_states_transactions = pd.read_sql(query7, engine)

    fig = px.pie(top_states_transactions, values='TotalTransactionAmount', names='State',
                 title='Top 10 States by Total Transaction Amount',
                 hole=0.6)
    
    st.plotly_chart(fig, use_container_width=True)

def question8():
    query8 = "SELECT Transaction_type, SUM(Transaction_amount) AS TotalTransactionAmount FROM aggregated_transactions GROUP BY Transaction_type"
    transaction_type_amounts = pd.read_sql(query8, engine)

    fig = px.pie(transaction_type_amounts, values='TotalTransactionAmount', names='Transaction_type',
                 title='Total Transaction Amounts by Transaction Type')
    
    st.plotly_chart(fig, use_container_width=True)

def question9():
    query9 = "SELECT Quarter, SUM(Registerted_users) AS TotalUsers FROM map_users GROUP BY Quarter"
    users_by_quarter = pd.read_sql(query9, engine)

    fig = px.pie(users_by_quarter, values='TotalUsers', names='Quarter',
                 title='Distribution of Registered Users by Quarter')
    
    st.plotly_chart(fig, use_container_width=True)

def question10():
    query10 = "SELECT District_name, SUM(Registerted_users) AS TotalUsers FROM map_users GROUP BY District_name ORDER BY TotalUsers DESC LIMIT 10"
    top_districts_users = pd.read_sql(query10, engine)

    fig = px.bar(top_districts_users, x='District_name', y='TotalUsers',
                 title='Top 10 Districts by Registered Users',
                 labels={'TotalUsers': 'Number of Users', 'District_name': 'District'})
    
    st.plotly_chart(fig, use_container_width=True)
def pre_analysis():
    st.title("Query Analysis")
    query_options = {
        "1). List most highest amount of transaction states in year 2020 and 2023": question1,
        "2). List of Top 10 Transaction Amount by State and Type": question2,
        "3). Top 10 state Mobile brand": question3,
        "4). List of transaction Amount's in all State": question4,
        "5). List of Registerd user's in all Cities": question5,
        "6). Transcation from Tamil Nadu around the years": question6,
        "7). Top 10 States by Total Transaction Amount": question7,
        "8). Total Transaction Amounts by Transaction Type": question8,
        "9). List of Registered Users by Quarter": question9,
        "10). Top 10 Districts by Registered Users": question10
    }

    query_selection = st.selectbox("Select a query to run:", list(query_options.keys()))

    if query_selection in query_options:
        query_options[query_selection]()

def main():

    if 'Home_page' not in st.session_state:
        st.session_state.Home_page = True
    if 'show_total_transaction_amount' not in st.session_state:
        st.session_state.show_total_transaction_amount = False

    if st.sidebar.button("Home"):
        st.session_state.Home_page = True
        st.session_state.show_total_transaction_amount = False
    if st.sidebar.button("Data Exploration"):
        st.session_state.Home_page = False
        st.session_state.show_total_transaction_amount = True
    if st.sidebar.button("Pre Analysis"):
        st.session_state.Home_page = False
        st.session_state.show_total_transaction_amount = False
    tab1, tab2= st.sidebar.tabs(["Districts", "State"])

    with tab1:
        top_districts_query = "SELECT District_name FROM map_transactions GROUP BY District_name ORDER BY SUM(Transaction_amount) DESC LIMIT 10"
        top_districts_df = pd.read_sql(top_districts_query, engine)

        district_texts = []
        for idx, row in top_districts_df.iterrows():
            dis_text = f"{idx + 1}) {row['District_name']}"
            district_texts.append(dis_text)
        dis_text = "\n".join(district_texts)
        st.write("Top 10 Districts by Transaction Amount:")
        st.write(dis_text)
    with tab2:
        
        top_state_query = "SELECT State, Transaction_amount FROM `aggregated_transactions` GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;"
        top_state_df = pd.read_sql(top_state_query, engine)

        state_texts = []
        for idx, row in top_state_df.iterrows():
            state_text = f"{idx + 1}) {row['State']}"
            state_texts.append(state_text)
        state_text = "\n".join(state_texts)
        st.write("Top 10 State by Transaction Amount:")
        st.write(state_text)
    
    if st.session_state.Home_page:
        home_page()
    elif st.session_state.show_total_transaction_amount:
        data_exploration()
    else:
        pre_analysis()
if __name__ == "__main__":
    main()
