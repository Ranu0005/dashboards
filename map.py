import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("D:\\Data science with streamlit\\code\\streamlit\\data\\airbnb.csv")
    return df

df = load_data()

# Create pie chart
def pie_chart():
    st.header("Pie Chart")
    dff = df.groupby("signup_method")["secs_elapsed"].sum().reset_index()
    fig = px.pie(dff, values='secs_elapsed', names='signup_method', 
                 title='Signup Methods Distribution')
    st.plotly_chart(fig)

# Main function
def main():
    pie_chart()

if __name__ == "__main__":
    main()
