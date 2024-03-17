import os
import json
import plotly.express as px
from pprint import pprint
import pandas as pd
import streamlit as st
import pymysql
from sqlalchemy import create_engine

#Connection_With_MySQL:
db_connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="phonepeanalytics_db")

engine = create_engine('mysql+pymysql://root:@localhost/phonepeanalytics_db')

#Aggregated_Transactions:
base_path_at = r'C:\Users\Asus\Downloads\Bala prac_Anaconda\Phonepe_project\pulse\data\aggregated\transaction\country\india\state'

state_list_at  = os.listdir(base_path_at )

at_columns = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}

for state_name_at in state_list_at:
    state_path_at = os.path.join(base_path_at, state_name_at) 
    year_list_at = os.listdir(state_path_at)

    for year_name_at in year_list_at:
        year_path_at = os.path.join(state_path_at, year_name_at)
        quarter_list_at = os.listdir(year_path_at)

        for quarter_name_at in quarter_list_at:
            file_path_at = os.path.join(year_path_at, quarter_name_at)
            data_at = open(file_path_at, "r")
            transaction_data_at = json.load(data_at)

            for i in transaction_data_at["data"]["transactionData"]:
                Name = i["name"]
                Name_cleaned = Name.replace('&','and').replace('-', '')
                Count_at = i["paymentInstruments"][0]["count"]
                Amount_at  = i["paymentInstruments"][0]["amount"]
                at_columns["Transaction_type"].append(Name_cleaned)
                at_columns["Transaction_count"].append(Count_at)
                at_columns["Transaction_amount"].append(Amount_at)
                at_columns["Year"].append(year_name_at)
                at_columns["State"].append(state_name_at)
                at_columns["Quarter"].append(int(quarter_name_at.strip('.json')))

df1_at  = pd.DataFrame(at_columns)
df1_at["State"] = df1_at["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df1_at["State"] = df1_at["State"].str.replace("-"," ")
df1_at["State"] = df1_at["State"].str.title()
df1_at['State'] = df1_at['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

#For_Aggregated_User:                
base_path_au = r'C:\Users\Asus\Downloads\Bala prac_Anaconda\Phonepe_project\pulse\data\aggregated\user\country\india\state'

agg_user_list_au = os.listdir(base_path_au)

at_columns2 = {'State': [], 'Year': [], 'Quarter': [], 'User_brand': [], 'User_count': [], 'User_percentage': []}

for state_name_au in state_list_at:
    state_path_au = os.path.join(base_path_au, state_name_au) 
    year_list_au = os.listdir(state_path_au)
    
    for year_name_au in year_list_au:
        year_path_au = os.path.join(state_path_au, year_name_au)
        quarter_list_au = os.listdir(year_path_au)
        
        for quarter_name_au in quarter_list_au:
            file_path_au = os.path.join(year_path_au, quarter_name_au)
            data_au = open(file_path_au, "r")
            user_data_au = json.load(data_au)

            try:
                
                for i_au in user_data_au["data"]["usersByDevice"]:
                    Brand_au = i_au["brand"]
                    Count_au = i_au["count"]
                    Percentage_au = "{:.2f}%".format(i_au["percentage"]* 100)
                    at_columns2["User_brand"].append(Brand_au)
                    at_columns2["User_count"].append(Count_au)
                    at_columns2["User_percentage"].append(Percentage_au)
                    at_columns2["Year"].append(year_name_au)
                    at_columns2["State"].append(state_name_au)
                    at_columns2["Quarter"].append(int(quarter_name_au.strip('.json')))
                    
            except:
                pass

df2_au = pd.DataFrame(at_columns2)
df2_au["State"] = df2_au["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df2_au["State"] = df2_au["State"].str.replace("-"," ")
df2_au["State"] = df2_au["State"].str.title()
df2_au['State'] = df2_au['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")


#For_Map_Transactions:
base_path_mt = r'C:\Users\Asus\Downloads\Bala prac_Anaconda\Phonepe_project\pulse\data\map\transaction\hover\country\india\state'
map_transaction_mt = os.listdir(base_path_mt)

at_columns3 = {'State': [], 'Year': [], 'Quarter': [], 'District_name': [], 'Transaction_count': [], 'Transaction_amount': []}

for state_name_mt in map_transaction_mt:
    state_path_mt = os.path.join(base_path_mt, state_name_mt)
    year_list_mt = os.listdir(state_path_mt)
    
    
    for year_name_mt in year_list_mt:
        year_path_mt = os.path.join(state_path_mt, year_name_mt)
        quarter_list_mt = os.listdir(year_path_mt)
        
        
        for quarter_name_mt in quarter_list_mt:
            file_path_mt = os.path.join(year_path_mt, quarter_name_mt)
            data_mt = open(file_path_mt, "r")
            map_transaction_data_mt = json.load(data_mt)

            for i_mt in map_transaction_data_mt["data"]["hoverDataList"]:
                Name_mt = i_mt["name"]
                Count_mt = i_mt["metric"][0]["count"]
                Amount_mt = i_mt["metric"][0]["amount"]
                at_columns3["District_name"].append(Name_mt)
                at_columns3["Transaction_count"].append(Count_mt)
                at_columns3["Transaction_amount"].append(Amount_mt)
                at_columns3["Year"].append(year_name_mt)
                at_columns3["State"].append(state_name_mt)
                at_columns3["Quarter"].append(int(quarter_name_mt.strip('.json')))

df3_mt = pd.DataFrame(at_columns3)
df3_mt["State"] = df3_mt["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df3_mt["State"] = df3_mt["State"].str.replace("-"," ")
df3_mt["State"] = df3_mt["State"].str.title()
df3_mt['State'] = df3_mt['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

#For_Map_User:
base_path_mu = r'C:\Users\Asus\Downloads\Bala prac_Anaconda\Phonepe_project\pulse\data\map\user\hover\country\india\state'
map_user_mu = os.listdir(base_path_mu)

at_columns4 = {'State': [], 'Year': [], 'Quarter': [], 'District_name': [], 'Registerted_users': [], 'App_opens': []}

for state_name_mu in map_user_mu:
    state_path_mu = os.path.join(base_path_mu, state_name_mu)
    year_list_mu = os.listdir(state_path_mu)
    
    
    for year_name_mu in year_list_mu:
        year_path_mu = os.path.join(state_path_mu, year_name_mu)
        quarter_list_mu = os.listdir(year_path_mu)
        
        
        for quarter_name_mu in quarter_list_mu:
            file_path_mu = os.path.join(year_path_mu, quarter_name_mu)
            data_mu = open(file_path_mu, "r")
            map_user_data_mu = json.load(data_mu)
            #pprint(map_user_data_mu["data"]["hoverData"])
            
            for i_mu in map_user_data_mu["data"]["hoverData"].items():
                District_mu = i_mu[0]
                Registerted_users_mu = i_mu[1]["registeredUsers"]
                App_opens_mu = i_mu[1]["appOpens"]
                at_columns4["District_name"].append(District_mu)
                at_columns4["Registerted_users"].append(Registerted_users_mu)
                at_columns4["App_opens"].append(App_opens_mu)
                at_columns4["Year"].append(year_name_mu)
                at_columns4["State"].append(state_name_mu)
                at_columns4["Quarter"].append(int(quarter_name_mu.strip('.json')))


df4_mu = pd.DataFrame(at_columns4)
df4_mu["State"] = df4_mu["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df4_mu["State"] = df4_mu["State"].str.replace("-"," ")
df4_mu["State"] = df4_mu["State"].str.title()
df4_mu['State'] = df4_mu['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

#For_top_Transactions:
base_path_tt = r'C:\Users\Asus\Downloads\Bala prac_Anaconda\Phonepe_project\pulse\data\top\transaction\country\india\state'
top_transaction_tt = os.listdir(base_path_tt)

at_columns5 = {'State': [], 'Year': [], 'Quarter': [], "District_name":[], 'Transaction_count': [], 'Transaction_amount': []}

for state_name_tt in top_transaction_tt:
    state_path_tt = os.path.join(base_path_tt, state_name_tt)
    year_list_tt = os.listdir(state_path_tt)
    
    
    for year_name_tt in year_list_tt:
        year_path_tt = os.path.join(state_path_tt, year_name_tt)
        quarter_list_tt = os.listdir(year_path_tt)
        
        
        for quarter_name_tt in quarter_list_tt:
            file_path_tt = os.path.join(year_path_tt, quarter_name_tt)
            data_tt = open(file_path_tt, "r")
            top_transaction_data_tt = json.load(data_tt)
            #pprint(top_transaction_data_tt)
            
            
            for i_tt in top_transaction_data_tt["data"]["districts"]:
                Name_tt = i_tt["entityName"]
                Count_tt = i_tt["metric"]["count"]
                Amount_tt = i_tt["metric"]["amount"]
                at_columns5["District_name"].append(Name_tt)  
                at_columns5["Transaction_count"].append(Count_tt)
                at_columns5["Transaction_amount"].append(Amount_tt)
                at_columns5["Year"].append(year_name_tt)
                at_columns5["State"].append(state_name_tt)
                at_columns5["Quarter"].append(int(quarter_name_tt.strip('.json')))
                

df5_tt = pd.DataFrame(at_columns5)
df5_tt["State"] = df5_tt["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df5_tt["State"] = df5_tt["State"].str.replace("-"," ")
df5_tt["State"] = df5_tt["State"].str.title()
df5_tt['State'] = df5_tt['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

#For_top_Users:
base_path_tu = r'C:\Users\Asus\Downloads\Bala prac_Anaconda\Phonepe_project\pulse\data\top\user\country\india\state'
top_transaction_tu = os.listdir(base_path_tu)

at_columns6 = {'State': [], 'Year': [], 'Quarter': [], 'City_name': [], 'Registerted_users': [],}

for state_name_tu in top_transaction_tu:
    state_path_tu = os.path.join(base_path_tu, state_name_tu)
    year_list_tu = os.listdir(state_path_tu)
    
    
    for year_name_tu in year_list_tu:
        year_path_tu = os.path.join(state_path_tu, year_name_tu)
        quarter_list_tu = os.listdir(year_path_tu)
        
        
        for quarter_name_tu in quarter_list_tu:
            file_path_tu = os.path.join(year_path_tu, quarter_name_tu)
            data_tu = open(file_path_tu, "r")
            top_user_data_tu = json.load(data_tu)
            #pprint(top_user_data_tu["data"]["districts"])
            
            
            for i_tu in top_user_data_tu["data"]["districts"]:
                Name_tu = i_tu["name"]
                Registerted_users_tu = i_tu["registeredUsers"]
                at_columns6["City_name"].append(Name_tu)  
                at_columns6["Registerted_users"].append(Registerted_users_tu)
                at_columns6["Year"].append(year_name_tu)
                at_columns6["State"].append(state_name_tu)
                at_columns6["Quarter"].append(int(quarter_name_tu.strip('.json')))

df6_tu = pd.DataFrame(at_columns6)
df6_tu["State"] = df6_tu["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
df6_tu["State"] = df6_tu["State"].str.replace("-"," ")
df6_tu["State"] = df6_tu["State"].str.title()
df6_tu['State'] = df6_tu['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")


def insert_data_to_mysql():
    df1_at.to_sql(name='aggregated_transactions', con=engine, if_exists='replace', index=False)
    df2_au.to_sql(name='aggregated_users', con=engine, if_exists='replace', index=False)
    df3_mt.to_sql(name='map_transactions', con=engine, if_exists='replace', index=False)
    df4_mu.to_sql(name='map_users', con=engine, if_exists='replace', index=False)
    df5_tt.to_sql(name='top_transactions', con=engine, if_exists='replace', index=False)
    df6_tu.to_sql(name='top_users', con=engine, if_exists='replace', index=False)    
    
def main():
    insert_data_to_mysql()
    
if __name__ == "__main__":
    main()
