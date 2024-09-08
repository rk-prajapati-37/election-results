import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

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

# City location data (Latitude and Longitude)
city_locations = {
    'Mumbai': [19.0760, 72.8777],
    'Delhi': [28.7041, 77.1025],
    'Kolkata': [22.5726, 88.3639],
    'Surat': [21.1702, 72.8311],
    'Pune': [18.5204, 73.8567]
}

# Fetch India's states GeoJSON data (URL points to a repository with India's state borders)
geojson_url = 'https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson'
geojson_data = requests.get(geojson_url).json()

# Function to filter news by city
def filter_news_by_city(news, city_name):
    filtered_news = news[news['City'].str.lower() == city_name.lower()]  # Case-insensitive match
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
            st.write(f"**City:** {row['City']}")
            st.write('-' * 50)

# Function to create map with hover effect and state borders using GeoJSON
def create_map_with_hover(city_locations, geojson_data):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    # Add the GeoJSON layer for state borders with hover effect
    folium.GeoJson(
        geojson_data,
        name='geojson',
        style_function=lambda x: {
            'fillColor': 'gray',
            'color': 'black',  # State border color
            'weight': 1,
            'fillOpacity': 0.1,
        },
        highlight_function=lambda x: {
            'weight': 3,  # Highlight border on hover
            'fillOpacity': 0.5,
            'color': 'blue'  # Border color changes to blue on hover
        },
        tooltip=folium.GeoJsonTooltip(fields=['NAME_1'], aliases=['State: '])
    ).add_to(m)

    # Add city markers
    for city, coords in city_locations.items():
        marker = folium.Marker(
            location=coords,
            popup=city,
            tooltip=f"Click for news from {city}",
            icon=folium.Icon(color='blue')
        ).add_to(m)

    return m

# Function to render the news page in Streamlit app
def news_page():
    st.title("City News with State Borders")

    # Create two columns layout: left for the map (33%), right for the news details (66%)
    col1, col2 = st.columns([2, 1])  # 33% width for the map and 66% for the news details

    with col1:
        st.subheader("City ka naam daalein ya map se choose karein:")

        # Display the map with hover effect
        m = create_map_with_hover(city_locations, geojson_data)
        map_output = st_folium(m, width=500, height=500)  # Adjust map size

        # Extract clicked city name if available
        city_name = ""
        if map_output and 'last_object_clicked_popup' in map_output:
            city_name = map_output['last_object_clicked_popup']  # Extract clicked city name

    with col2:
        st.subheader("Selected City News:")
        if city_name:
            filter_news_by_city(news_df, city_name)  # Filter and display news for the selected city
        else:
            st.write("Map par kisi city ko click karein ya search karein.")

# Run the app
if __name__ == '__main__':
    news_page()
