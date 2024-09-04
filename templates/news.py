import pandas as pd
import streamlit as st

# Google Sheets CSV URL
url = 'https://docs.google.com/spreadsheets/d/18Z0HOYlHqjOAHOV55JaUiHiidDvNPqkbMlqDuFBEGWQ/export?format=csv&gid=1785908724'

# Manually specifying column names
columns = [
    "Sr No", "News Id", "City", "Heading", "Date Of Publish", "URL",
    "Author", "Editor", "Reviewer", "Category", "Tags", "GA Views",
    "Image", "Display Story As Fast Check", "Select Review", "Text Caption",
    "Caption", "language", "Article Type", "Claim Review", "Claimed By",
    "Claim Source"
]

# Load CSV file, skip first 3 rows, and specify column names
news_df = pd.read_csv(url, skiprows=3, names=columns, header=None)

# Function to filter news by city


def filter_news_by_city(news, city_name):
    filtered_news = news[news['City'].str.lower() == city_name.lower()]
    if filtered_news.empty:
        st.write(f"{city_name} ke liye koi news nahi mili.")
    else:
        for index, row in filtered_news.iterrows():
            st.write(f"**News ID:** {row['News Id']}")
            st.write(f"**Heading:** {row['Heading']}")
            st.write(f"**Date Of Publish:** {row['Date Of Publish']}")
            st.write(f"**URL:** [Link]({row['URL']})")
            st.write(f"**Author:** {row['Author']}")
            st.write(f"**Editor:** {row['Editor']}")
            st.write(f"**Reviewer:** {row['Reviewer']}")
            st.write(f"**Category:** {row['Category']}")
            st.write(f"**Tags:** {row['Tags']}")
            st.write(f"**GA Views:** {row['GA Views']}")
            st.write(f"**Image:** ![Image]({row['Image']})")
            st.write(
                f"**Display Story As Fast Check:** {row['Display Story As Fast Check']}")
            st.write(f"**Select Review:** {row['Select Review']}")
            st.write(f"**Text Caption:** {row['Text Caption']}")
            st.write(f"**Caption:** {row['Caption']}")
            st.write(f"**Language:** {row['language']}")
            st.write(f"**Article Type:** {row['Article Type']}")
            st.write(f"**Claim Review:** {row['Claim Review']}")
            st.write(f"**Claimed By:** {row['Claimed By']}")
            st.write(f"**Claim Source:** {row['Claim Source']}")
            st.write(f"**City:** {row['City']}")
            st.write('-' * 50)

# Function to render the news page in Streamlit app


def news_page():
    st.title("News by City")

    # User input for city name
    city_name = st.text_input("City ka naam daalein:")

    # If a city is provided, filter and display news
    if city_name:
        filter_news_by_city(news_df, city_name)
