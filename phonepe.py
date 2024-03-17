import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
st.set_page_config(layout="wide")
# Connection_With_MySQL:
engine = create_engine('mysql+pymysql://root:@localhost/phonepeanalytics_db')

def fetch_total_transaction_amount():
    query = "SELECT SUM(Transaction_amount) AS Total_Transaction_Amount FROM aggregated_transactions"
    total_transaction_amount = pd.read_sql(query, engine)
    return total_transaction_amount['Total_Transaction_Amount'][0]

def aggreagte_transaction_plotly(year):
    query = f"SELECT * FROM aggregated_transactions WHERE Year={year}"
    df = pd.read_sql(query, engine)
    return df
def aggreagte_quarter_plotly(quarter):
    query = f"SELECT * FROM aggregated_transactions WHERE Quarter={quarter}"
    df = pd.read_sql(query, engine)
    return df

def aggreagte_state_plotly(state):
    query = f"SELECT * FROM aggregated_transactions WHERE State='{state}'"
    df = pd.read_sql(query, engine)
    return df

def map_transaction_plotly(year):
    query = f"SELECT * FROM map_transactions WHERE Year={year}"
    map = pd.read_sql(query, engine)
    return map

def map_transaction_quarter_plotly(quarter1):
    query = f"SELECT * FROM map_transactions WHERE Quarter={quarter1}"
    df = pd.read_sql(query, engine)
    return df

def map_state_plotly(state1):
    query = f"SELECT * FROM map_transactions WHERE State='{state1}'"
    df = pd.read_sql(query, engine)
    return df

def top_transaction_plotly(year):
    query = f"SELECT * FROM top_transactions WHERE Year={year}"
    top = pd.read_sql(query, engine)
    return top

def top_transaction_quarter_plotly(quarter2):
    query = f"SELECT * FROM top_transactions WHERE Quarter={quarter2}"
    df = pd.read_sql(query, engine)
    return df

def top_state_plotly(state2):
    query = f"SELECT * FROM top_transactions WHERE State='{state2}'"
    df = pd.read_sql(query, engine)
    return df

def aggreate_users(year):
    query = f"SELECT * FROM aggregated_users WHERE Year={year}"
    df = pd.read_sql(query, engine)
    return df

def aggreagte_userquarter_plotly(quarter):
    query = f"SELECT * FROM aggregated_users WHERE Quarter={quarter}"
    df = pd.read_sql(query, engine)
    return df

def aggreagteuser_state_plotly(state):
    query = f"SELECT * FROM aggregated_users WHERE State='{state}'"
    df = pd.read_sql(query, engine)
    return df

def map_user_plotly(year):
    query = f"SELECT * FROM map_users WHERE Year={year}"
    map = pd.read_sql(query, engine)
    return map

def map_user_quarter_plotly(quarter1):
    query = f"SELECT * FROM map_users WHERE Quarter={quarter1}"
    df = pd.read_sql(query, engine)
    return df

def map_user_state_plotly(state1):
    query = f"SELECT * FROM map_users WHERE State='{state1}'"
    df = pd.read_sql(query, engine)
    return df

def top_user_plotly(year):
    query = f"SELECT * FROM top_users WHERE Year={year}"
    top = pd.read_sql(query, engine)
    return top

def top_user_quarter_plotly(quarter2):
    query = f"SELECT * FROM top_users WHERE Quarter={quarter2}"
    df = pd.read_sql(query, engine)
    return df

def top_user_state_plotly(state2):
    query = f"SELECT * FROM top_users WHERE State='{state2}'"
    df = pd.read_sql(query, engine)
    return df

def analytics(year):
    query = f"SELECT State, Transaction_amount FROM `aggregated_transactions` WHERE Year={year} GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10"
    df = pd.read_sql(query, engine)
    return df

def home_page():
    image = "https://logolook.net/wp-content/uploads/2022/12/PhonePe-Logo.png"  # Replace this URL with your image URL
    st.image(image, width=400)

    st.title("Phonepe Pulse Data Visualization and Exploration")
    
    st.header("Project Details")
    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
    Nulla nec leo purus. Curabitur lacinia nunc nec libero convallis fermentum.
    """)

def data_exploration():
    selected_option = st.selectbox("Select an option", ["Transaction", "User"])

    if selected_option=="Transaction":
        # Execute query to get total transaction amount
        total_transaction_query = "SELECT SUM(Transaction_amount) AS Total_Transaction_Amount,SUM(Transaction_count) AS Total_Transaction  FROM aggregated_transactions"
        total_transaction_df = pd.read_sql(total_transaction_query, engine)
        total_transaction_amount = total_transaction_df.iloc[0]['Total_Transaction_Amount']
        Total_Transaction = total_transaction_df.iloc[0]['Total_Transaction']
        # Calculate average transaction value
        average_transaction_value = total_transaction_amount / total_transaction_df.iloc[0]['Total_Transaction']

        # Display the statistics
        # Display the statistics in a single row
        st.write("Transactions")
        st.write("All PhonePe transactions (UPI + Cards + Wallets)")
        st.write(f"{total_transaction_amount:,.2f}", unsafe_allow_html=True)  # Display total transaction amount with commas
        st.write("Total payment value")
        st.write(f"₹{total_transaction_amount / 1e9:.2f} Cr")
        st.write(f"{'Avg. transaction value':>30}")
        st.write(f"{'₹' + str(int(average_transaction_value)):<30}")

        tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

        with tab1:
            st.subheader("Aggregate Data")
            query = "SELECT DISTINCT Year FROM aggregated_transactions"
            years_df = pd.read_sql(query, engine)
            years = years_df['Year'].tolist()
        
            selected_year = st.selectbox("Select Year for aggregiater", years)
            df = aggreagte_transaction_plotly(selected_year)
            filtered_df = df[df['Year'] == selected_year]



            # Group by 'Year' and 'State' and calculate transaction counts
            state_transaction_amount = filtered_df.groupby(['Year', 'State'])['Transaction_amount'].sum().reset_index()
            state_transaction_count = filtered_df.groupby(['Year', 'State'])['Transaction_count'].sum().reset_index()

            # Plot bar chart
            fig1 = px.bar(state_transaction_amount, x='State', y='Transaction_amount', color='Year',
                        title='Transaction_amount by State for Each Year',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            fig2 = px.bar(state_transaction_count, x='State', y='Transaction_count', color='Year',
                        title='Transaction_count by State for Each Year',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)

            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig1,use_container_width=True)
            with col2:
                st.plotly_chart(fig2,use_container_width=True)


            quarter ="SELECT DISTINCT Quarter FROM aggregated_transactions"
            quarter_df = pd.read_sql(quarter, engine)
            quarter_list = quarter_df['Quarter'].tolist()

            selected_quarter = st.selectbox("Select Quarter for aggregiater", quarter_list)
            qua = aggreagte_quarter_plotly(selected_quarter)
            filtered_qua = qua[qua['Quarter'] == selected_quarter]

            # Group by 'Year' and 'State' and calculate transaction counts
            state_transaction_amount = filtered_qua.groupby(['Quarter', 'State'])['Transaction_amount'].sum().reset_index()
            state_transaction_count = filtered_qua.groupby(['Quarter', 'State'])['Transaction_count'].sum().reset_index()

            # Plot bar chart
            fig3 = px.bar(state_transaction_amount, x='State', y='Transaction_amount', color='Quarter',
                        title='Transaction_amount by State for Each Quarter',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            fig4 = px.bar(state_transaction_count, x='State', y='Transaction_count', color='Quarter',
                        title='Transaction_count by State for Each Quarter',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(fig3,use_container_width=True)
            with col4:
                st.plotly_chart(fig4,use_container_width=True)

            
            state ="SELECT DISTINCT State FROM aggregated_transactions"
            state_df = pd.read_sql(state, engine)
            state_list = state_df['State'].tolist()
            selected_state = st.selectbox("Select state for aggregiater", state_list)
            sta = aggreagte_state_plotly(selected_state)
            filtered_sta = sta[sta['State'] == selected_state]

            state_transaction_amount = filtered_sta.groupby(['Quarter', 'State'])['Transaction_amount'].sum().reset_index()
            state_transaction_count = filtered_sta.groupby(['Quarter', 'State'])['Transaction_count'].sum().reset_index()

            fig5 = px.pie(state_transaction_amount, values='Transaction_amount', names='Quarter',
                title='Transaction_amount by State for Each Quarter', width=700)
            
            fig6 = px.pie(state_transaction_count, values='Transaction_count', names='Quarter',
                title='Transaction_count by State for Each Quarter', width=700)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(fig5,use_container_width=True)
            with col6:
                st.plotly_chart(fig6,use_container_width=True)


        with tab2:
            st.subheader("Map Data")
            query1 = "SELECT DISTINCT Year FROM map_transactions"
            years1_df = pd.read_sql(query1, engine)
            years1 = years1_df['Year'].tolist()

            selected_year1 = st.selectbox("Select Year for map", years1)
            map = map_transaction_plotly(selected_year1)
            filtered_map = map[map['Year'] == selected_year1]

            map_transaction_amount = filtered_map.groupby(['Year', 'State'])['Transaction_amount'].sum().reset_index()
            map_transaction_count = filtered_map.groupby(['Year', 'State'])['Transaction_count'].sum().reset_index()

            map1 = px.bar(map_transaction_amount, x='State', y='Transaction_amount', color='Year',
                        title='Transaction_amount for Each Year',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            map2 = px.bar(map_transaction_count, x='State', y='Transaction_count', color='Year',
                        title='Transaction_count for Each Year',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(map1,use_container_width=True)
            with col2:
                st.plotly_chart(map2,use_container_width=True)

            quarter1 ="SELECT DISTINCT Quarter FROM map_transactions"
            quarter_df1 = pd.read_sql(quarter1, engine)
            quarter1_list = quarter_df1['Quarter'].tolist()

            selected_quarter1 = st.selectbox("Select Quarter for map", quarter1_list)
            qua1 = map_transaction_quarter_plotly(selected_quarter1)
            filtered_qua1 = qua1[qua1['Quarter'] == selected_quarter1]

            # Group by 'Year' and 'State' and calculate transaction counts
            map_transaction_amount = filtered_qua1.groupby(['Quarter', 'State'])['Transaction_amount'].sum().reset_index()
            map_transaction_count = filtered_qua1.groupby(['Quarter', 'State'])['Transaction_count'].sum().reset_index()

            # Plot bar chart
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

            state1 ="SELECT DISTINCT State FROM map_transactions"
            state1_df = pd.read_sql(state1, engine)
            state_list1 = state1_df['State'].tolist()
            selected_state1 = st.selectbox("Select state for map", state_list1)
            stae = map_state_plotly(selected_state1)
            filtered_sta1 = stae[stae['State'] == selected_state]

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



            # Plot map using df

        with tab3:
            st.subheader("Top Data")
            query2 = "SELECT DISTINCT Year FROM top_transactions"
            years2_df = pd.read_sql(query2, engine)
            years2 = years2_df['Year'].tolist()
            selected_year2 = st.selectbox("Select Year for tp", years2)
            top = top_transaction_plotly(selected_year2)
            filtered_top = top[top['Year'] == selected_year2]

            top_transaction_amount = filtered_top.groupby(['Year', 'State'])['Transaction_amount'].sum().reset_index()
            top_transaction_count = filtered_top.groupby(['Year', 'State'])['Transaction_count'].sum().reset_index()

            top1 = px.bar(top_transaction_amount, x='State', y='Transaction_amount', color='Year',
                        title='Transaction_amount for Each Year',
                        labels={'Transaction_amount': 'Transaction_amount', 'State': 'State'},width=700)
            
            top2 = px.bar(top_transaction_count, x='State', y='Transaction_count', color='Year',
                        title='Transaction_count for Each Year',
                        labels={'Transaction_count': 'Transaction_count', 'State': 'State'},width=700)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(top1,use_container_width=True)
            with col2:
                st.plotly_chart(top2,use_container_width=True) 


            quarter2 ="SELECT DISTINCT Quarter FROM top_transactions"
            quarter_df2 = pd.read_sql(quarter2, engine)
            quarter2_list = quarter_df2['Quarter'].tolist()

            selected_quarter2 = st.selectbox("Select Quarter for top", quarter2_list)
            qua2 = top_transaction_quarter_plotly(selected_quarter2)
            filtered_qua2 = qua2[qua2['Quarter'] == selected_quarter2]

            # Group by 'Year' and 'State' and calculate transaction counts
            top_transaction_amount = filtered_qua2.groupby(['Quarter', 'State'])['Transaction_amount'].sum().reset_index()
            top_transaction_count = filtered_qua2.groupby(['Quarter', 'State'])['Transaction_count'].sum().reset_index()

            # Plot bar chart
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

            state2 ="SELECT DISTINCT State FROM top_transactions"
            state2_df = pd.read_sql(state2, engine)
            state_list2 = state2_df['State'].tolist()
            selected_state2 = st.selectbox("Select state for top", state_list2)
            staes = top_state_plotly(selected_state2)
            filtered_sta2 = staes[staes['State'] == selected_state]

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

    else:
        total_users_query = "SELECT SUM(User_count) AS User_count FROM aggregated_users"
        total_users_df = pd.read_sql(total_users_query, engine)
        total_User_count = total_users_df.iloc[0]['User_count']
        
        st.write("All PhonePe users ")
        st.write(f"{total_User_count}")
        tab4, tab5, tab6= st.tabs(["Aggregated user Analysis", "Map user Analysis", "Top user Analysis"])
        
        with tab4:
            st.subheader("Aggregate user Data")
            au = "SELECT DISTINCT Year FROM aggregated_users"
            aguy = pd.read_sql(au, engine)
            uy = aguy['Year'].tolist()
        
            selected_year = st.selectbox("Select Year for ag user", uy)
            agr_users = aggreate_users(selected_year)
            filtered_agr_users = agr_users[agr_users['Year'] == selected_year]



            # Group by 'Year' and 'State' and calculate transaction counts
            state_user_percentage = filtered_agr_users.groupby(['Year', 'State'])['User_percentage'].sum().reset_index()
            state_user_count = filtered_agr_users.groupby(['Year', 'State'])['User_count'].sum().reset_index()

            # Plot bar chart
            user1 = px.bar(state_user_percentage, x='State', y='User_percentage', color='Year',
                        title='User_percentage by State for Each Year',
                        labels={'User_percentage': 'User_percentage', 'State': 'State'},width=700)
            
            user2 = px.bar(state_user_count, x='State', y='User_count', color='Year',
                        title='User_count by State for Each Year',
                        labels={'User_count': 'User_count', 'State': 'State'},width=700)

            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(user1,use_container_width=True)
            with col2:
                st.plotly_chart(user2,use_container_width=True)

            quarter ="SELECT DISTINCT Quarter FROM aggregated_users"
            quarter_df = pd.read_sql(quarter, engine)
            quarter_list = quarter_df['Quarter'].tolist()

            selected_quarter = st.selectbox("Select Quarter for aggregated users", quarter_list)
            qua = aggreagte_userquarter_plotly(selected_quarter)
            filtered_qua = qua[qua['Quarter'] == selected_quarter]

            # Group by 'Year' and 'State' and calculate transaction counts
            state_user_percentage1 = filtered_qua.groupby(['Quarter', 'State'])['User_percentage'].sum().reset_index()
            state_transaction_count1 = filtered_qua.groupby(['Quarter', 'State'])['User_count'].sum().reset_index()

            # Plot bar chart
            user3 = px.bar(state_user_percentage1, x='State', y='User_percentage', color='Quarter',
                        title='User percentage by State for Each Quarter',
                        labels={'Transaction_amount': 'User_percentage', 'State': 'State'},width=700)
            
            user4 = px.bar(state_transaction_count1, x='State', y='User_count', color='Quarter',
                        title='User_count by State for Each Quarter',
                        labels={'Transaction_count': 'User_count', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)

            with col3:
                st.plotly_chart(user3,use_container_width=True)
            with col4:
                st.plotly_chart(user4,use_container_width=True)

            state ="SELECT DISTINCT State FROM aggregated_users"
            state_df = pd.read_sql(state, engine)
            state_list = state_df['State'].tolist()
            selected_state = st.selectbox("Select state for aggregiater users", state_list)
            sta = aggreagteuser_state_plotly(selected_state)
            filtered_sta = sta[sta['State'] == selected_state]

            state_transaction_amount = filtered_sta.groupby(['Quarter', 'State'])['User_percentage'].sum().reset_index()
            state_transaction_count = filtered_sta.groupby(['Quarter', 'State'])['User_count'].sum().reset_index()
            filtered_sta['User_percentage'] = filtered_sta['User_percentage'].str.rstrip('%').astype(float)

            # Plot the pie chart
            fig5 = px.pie(filtered_sta, values='User_percentage', names='Quarter',
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
            query1 = "SELECT DISTINCT Year FROM map_users"
            years1_df = pd.read_sql(query1, engine)
            years1 = years1_df['Year'].tolist()

            selected_year1 = st.selectbox("Select Year for map", years1)
            map = map_user_plotly(selected_year1)
            filtered_map = map[map['Year'] == selected_year1]

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

            quarter1 ="SELECT DISTINCT Quarter FROM map_users"
            quarter_df1 = pd.read_sql(quarter1, engine)
            quarter1_list = quarter_df1['Quarter'].tolist()

            selected_quarter1 = st.selectbox("Select Quarter for map", quarter1_list)
            qua1 = map_user_quarter_plotly(selected_quarter1)
            filtered_qua1 = qua1[qua1['Quarter'] == selected_quarter1]

            # Group by 'Year' and 'State' and calculate transaction counts
            map_registered_user = filtered_qua1.groupby(['Quarter', 'State'])['Registerted_users'].sum().reset_index()
            map_registered_count = filtered_qua1.groupby(['Quarter', 'State'])['App_opens'].sum().reset_index()

            # Plot bar chart
            map3 = px.bar(map_registered_user, x='State', y='Registerted_users', color='Quarter',
                        title='Registerted_users by map for Each Quarter',
                        labels={'Registerted_users': 'Registerted_users', 'State': 'State'},width=700)
            
            map4 = px.bar(map_registered_count, x='State', y='App_opens', color='Quarter',
                        title='App_opens by map for Each Quarter',
                        labels={'App_opens': 'App_opens', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(map3,use_container_width=True)
            with col4:
                st.plotly_chart(map4,use_container_width=True)

            state1 ="SELECT DISTINCT State FROM map_users"
            state1_df = pd.read_sql(state1, engine)
            state_list1 = state1_df['State'].tolist()
            selected_state1 = st.selectbox("Select state for map", state_list1)
            stae = map_user_state_plotly(selected_state1)
            filtered_sta1 = stae[stae['State'] == selected_state]

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
            query2 = "SELECT DISTINCT Year FROM top_users"
            years2_df = pd.read_sql(query2, engine)
            years2 = years2_df['Year'].tolist()
            selected_year2 = st.selectbox("Select Year for top user", years2)
            top = top_user_plotly(selected_year2)
            filtered_top = top[top['Year'] == selected_year2]

            top_registerd_users = filtered_top.groupby(['Year', 'State'])['Registerted_users'].sum().reset_index()
            top_District_name = filtered_top.groupby(['Year', 'State'])['City_name'].sum().reset_index()

            top1 = px.bar(top_registerd_users, x='State', y='Registerted_users', color='Year',
                        title='Registerted_users for Each Year',
                        labels={'Registerted_users': 'Registerted_users', 'State': 'State'},width=700)
            
            top2 = px.bar(top_District_name, x='State', y='City_name', color='Year',
                        title='District_name for Each Year',
                        labels={'District_name': 'District_name', 'State': 'State'},width=700)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(top1,use_container_width=True)
            with col2:
                st.plotly_chart(top2,use_container_width=True) 


            quarter2 ="SELECT DISTINCT Quarter FROM top_users"
            quarter_df2 = pd.read_sql(quarter2, engine)
            quarter2_list = quarter_df2['Quarter'].tolist()

            selected_quarter2 = st.selectbox("Select Quarter for top users", quarter2_list)
            qua2 = top_user_quarter_plotly(selected_quarter2)
            filtered_qua2 = qua2[qua2['Quarter'] == selected_quarter2]

            # Group by 'Year' and 'State' and calculate transaction counts
            top_user_state = filtered_qua2.groupby(['Quarter', 'State'])['Registerted_users'].sum().reset_index()
            top_user_district = filtered_qua2.groupby(['Quarter', 'State'])['City_name'].sum().reset_index()

            # Plot bar chart
            top3 = px.bar(top_user_state, x='State', y='Registerted_users', color='Quarter',
                        title='Registerted_users by map for Each Quarter',
                        labels={'Registerted_users': 'Registerted_users', 'State': 'State'},width=700)
            
            top4 = px.bar(top_user_district, x='State', y='City_name', color='Quarter',
                        title='District_name by map for Each Quarter',
                        labels={'District_name': 'District_name', 'State': 'State'},width=700)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(top3,use_container_width=True)
            with col4:
                st.plotly_chart(top4,use_container_width=True)   

            state2 ="SELECT DISTINCT State FROM top_users"
            state2_df = pd.read_sql(state2, engine)
            state_list2 = state2_df['State'].tolist()
            selected_state2 = st.selectbox("Select state for top", state_list2)
            staes = top_user_state_plotly(selected_state2)
            filtered_sta2 = staes[staes['State'] == selected_state]

            top_ud = filtered_sta2.groupby(['Quarter', 'State'])['Registerted_users'].sum().reset_index()
            top_dc= filtered_sta2.groupby(['Quarter', 'State'])['City_name'].sum().reset_index()

            top5 = px.pie(top_ud, values='Registerted_users', names='Quarter',
                title='Transaction_amount by top for Each Quarter', width=700)
            
            top6 = px.pie(top_dc, values='City_name', names='Quarter',
                title='Transaction_count by top for Each Quarter', width=700)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(top5,use_container_width=True)
            with col6:
                st.plotly_chart(top6,use_container_width=True)



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
    if st.sidebar.button("pre analysis"):
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
            state_text = f"{idx + 1}) {row['State']}: {row['Transaction_amount']}"
            state_texts.append(state_text)
        state_text = "\n".join(state_texts)
        st.write("Top 10 State by Transaction Amount:")
        st.write(state_text)
        

    if st.session_state.Home_page:
        home_page()
    elif st.session_state.show_total_transaction_amount:
        data_exploration()

if __name__ == "__main__":
    main()
