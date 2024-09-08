import streamlit as st
import os
from pathlib import Path
from templates.home import home_page
from templates.pandas_page import pandas_page
from templates.news import news_page

# Page layout settings
st.set_page_config(page_title="Home Page", layout="wide")

# Function to load custom CSS
def load_css():
    css_path = "assets/main.css"
    if os.path.exists(css_path):
        with open(css_path) as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.error("CSS file not found.")

# Load custom CSS
load_css()

# Sidebar menu for navigation
menu = st.sidebar.radio("Select a Page", ["Home", "State Results", "News"])

# Container to manage the layout
with st.container():
    # Render the selected page
    if menu == "Home":
        home_page()
    elif menu == "State Results":
        pandas_page()
    elif menu == "News":
        news_page()
