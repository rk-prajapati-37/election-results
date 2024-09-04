import streamlit as st
from templates.home import home_page
from templates.pandas_page import pandas_page
from templates.news import news_page 

# Sidebar menu for navigation
menu = st.sidebar.radio("Select a Page", ["Home", "State Results", "News"])

# Render the selected page
if menu == "Home":
    home_page()
elif menu == "State Results":
    pandas_page()
elif menu == "News":
    news_page()
