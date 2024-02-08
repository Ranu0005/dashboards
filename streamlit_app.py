import pandas as pd
import streamlit as st
import plotly.express as px
import pyodbc
import argparse

def get_connection():
    cnxn_str = (
        "Driver={SQL Server};"
        "Server=INPTSE11\\SQLEXPRESS;"
        "Database=MB1TH01Q;"
        "UID=SA;"
        "PWD=sa@1234;"
    )
    return pyodbc.connect(cnxn_str)

# Function to update line chart
def update_line_chart(selected_servers):
    cnxn = get_connection()
    if "all" in selected_servers:
        query = f"SELECT Date1, AVG(DATEDIFF(SECOND, '00:00:00', End_Time)) as Average_End_Time FROM [RPA_SB1_Prod] GROUP BY Date1 ORDER BY Date1 asc"
        data = pd.read_sql(query, cnxn)
    else:
        placeholders = ', '.join('?' for _ in selected_servers)
        query = f"SELECT Date1, AVG(DATEDIFF(SECOND, '00:00:00', End_Time)) as Average_End_Time FROM [RPA_SB1_Prod] WHERE Server1 IN ({placeholders}) GROUP BY Date1 ORDER BY Date1 asc"
        data = pd.read_sql(query, cnxn, params=selected_servers)
    cnxn.close()
    # Convert the Date1 column to datetime format and sort by it
    data['Date1'] = pd.to_datetime(data['Date1'], format='%d.%m.%Y')
    data = data.sort_values(by='Date1')
    fig = px.line(data, x="Date1", y="Average_End_Time", title="Date vs End TIme(line1 Chart)", markers=True)
    return fig

# Function to update another line chart
def update_another_line_chart(selected_servers):
    cnxn = get_connection()
    if "all" in selected_servers:
        query = f"SELECT Date1, B1_open_or_From_citrix_Application_Server_Or_Citrix_Server, AVG(DATEDIFF(SECOND, '00:00:00', End_Time)) as Average_End_Time FROM [RPA_SB1_Prod] GROUP BY Date1, B1_open_or_From_citrix_Application_Server_Or_Citrix_Server ORDER BY Date1 asc"
        data = pd.read_sql(query, cnxn)
    else:
        placeholders = ', '.join('?' for _ in selected_servers)
        query = f"SELECT Date1, B1_open_or_From_citrix_Application_Server_Or_Citrix_Server, AVG(DATEDIFF(SECOND, '00:00:00', End_Time)) as Average_End_Time FROM [RPA_SB1_Prod] WHERE Server1 IN ({placeholders}) GROUP BY Date1, B1_open_or_From_citrix_Application_Server_Or_Citrix_Server ORDER BY Date1 asc"
        data = pd.read_sql(query, cnxn, params=selected_servers)
    cnxn.close()
    # Convert the Date1 column to datetime format and sort by it
    data['Date1'] = pd.to_datetime(data['Date1'], format='%d.%m.%Y')
    data = data.sort_values(by='Date1')
    fig = px.line(data, x="Date1", y="Average_End_Time", color="B1_open_or_From_citrix_Application_Server_Or_Citrix_Server", title="Date vs End time", markers=True, height=600, width=1000)
    return fig

# Streamlit App
def main():
    st.title('PERFORMANCE TIME TESTING DASHBOARD')
    selected_servers = st.multiselect('Select Servers', ['all'], ['all'])

    line_chart = update_line_chart(selected_servers)
    st.plotly_chart(line_chart)

    another_line_chart = update_another_line_chart(selected_servers)
    st.plotly_chart(another_line_chart)
    if __name__ == '__main__': 
     parser = argparse.ArgumentParser(description="Streamlit app for performance time testing dashboard.")
     parser.add_argument('--selected_servers', nargs='+', default=['all'], help='Selected servers for analysis.')
     args = parser.parse_args()
     st.write("Arguments:", args)
     main(args.selected_servers)

