import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests

# NewsAPI endpoint and API key
api_key = '81f6e15f6aac4f3dba784e67a50e8265'  # Replace with your NewsAPI key
news_url = 'https://newsapi.org/v2/everything?domains=wsj.com&apiKey=' + api_key

# Fetch news data from NewsAPI
def fetch_news_data():
    response = requests.get(news_url)
    news_data = response.json()
    if news_data['status'] == 'ok':
        return news_data['articles']
    else:
        st.error("Failed to fetch news data.")
        return []

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

# Function to filter news by city (assumes city is mentioned in the article description)
# Function to filter news by city (assumes city is mentioned in the article description)
def filter_news_by_city(news, city_name):
    filtered_news = [article for article in news if article.get('description') and city_name.lower() in article['description'].lower()]

    if not filtered_news:
        st.write(f"{city_name} ke liye koi news nahi mili.")
    else:
        for article in filtered_news:
            # Display each news item in a card layout
            st.markdown(
                f"""
                <div class="art-card-box">
                    <!-- Full-Width Heading Section -->
                    <div style="width: 100%; margin-bottom: 10px;">
                        <a href="{article['url']}" target="_blank" class="heading-link">
                            <h3 class="main-heading-txt">{article['title']}</h3>
                        </a>
                    </div>
                    <!-- Flex Layout for Image and Details -->
                    <div style="display: flex;">
                        <!-- Left Image Section -->
                        <div class="future-img" style="flex: 1; margin-right: 10px;">
                            <a href="{article['url']}" target="_blank" class="image-link">
                                <img src="{article['urlToImage']}" alt="News Image" style="width: 100%; height: auto; border-radius: 8px;">
                            </a>
                        </div>
                        <!-- Right Text Section -->
                        <div style="flex: 2;">
                            <p style="margin: 0 0 10px 0; color: #555;">{article['description']}</p>
                            <p style="margin: 0 0 5px 0; color: #777;">By <strong>{article['author']}</strong> | {article['publishedAt']}</p>
                            <a class="more-btn" href="{article['url']}" target="_blank" style="color: white; background-color: #007BFF; padding: 8px 12px; text-decoration: none; border-radius: 5px;">Read More</a>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


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
            popup=city,  # City name will show in the popup
            tooltip=f"Click for news from {city}",
            icon=folium.Icon(color='blue')
        ).add_to(m)

    return m

# Function to render the news page in Streamlit app
def news_page():
    st.title("City News with WSJ Articles")

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
        news_articles = fetch_news_data()  # Fetch news articles from NewsAPI

        if city_name:
            st.write(f"**Selected City: {city_name}**")  # Show selected city
            filter_news_by_city(news_articles, city_name)  # Filter and display news for the selected city
        else:
            st.write("Map par kisi city ko click karein ya search karein.")

# Run the app
if __name__ == '__main__':
    news_page()
