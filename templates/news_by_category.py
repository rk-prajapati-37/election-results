# news_by_category.py

import streamlit as st
import pandas as pd

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

# Function to filter news by category
def filter_news_by_category(news, category_name):
    filtered_news = news[news['Category'].str.lower() == category_name.lower()]  # Case-insensitive match
    
    if filtered_news.empty:
        st.write(f"{category_name} ke liye koi news nahi mili.")
    else:
        for index, row in filtered_news.iterrows():
            # Display each news item in a card layout
            st.markdown(
                f"""
                <div class="art-card-box">
                    <!-- Full-Width Heading Section -->
                    <div style="width: 100%; margin-bottom: 10px;">
                        <a href="{row['URL']}" target="_blank" class="heading-link">
                            <h3 class="main-heading-txt">{row['Heading']}</h3>
                        </a>
                    </div>
                    <!-- Flex Layout for Image and Details -->
                    <div style="display: flex;">
                        <!-- Left Image Section -->
                        <div class="future-img" style="flex: 1; margin-right: 10px;">
                            <a href="{row['URL']}" target="_blank" class="image-link">
                                <img src="{row['Image']}" alt="News Image" style="width: 100%; height: auto; border-radius: 8px;">
                            </a>
                        </div>
                        <!-- Right Text Section -->
                        <div style="flex: 2;">
                            <!-- Author and Date Information -->
                            <p style="margin: 0 0 5px 0; color: #777;">By <strong>{row['Author']}</strong> | {row['Date Of Publish']}</p>
                            <!-- Category and City Information with Links -->
                            <p style="margin: 10px 0; color: #555;">
                                <p >Category: <strong  style="color: #007BFF;">{row['Category']}</strong></p> | 
                                <p >City: <strong style="color: #007BFF;">{row['City']}</strong></p>
                            </p>
                            <a class="more-btn" href="{row['URL']}" target="_blank" style="color: white; background-color: #007BFF; padding: 8px 12px; text-decoration: none; border-radius: 5px;">Read More</a>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Function to render the news page in Streamlit app
def news_page():
    st.title("Category News")

    # Extract query parameters
    query_params = st.experimental_get_query_params()
    selected_category = query_params.get('category', [None])[0]

    st.subheader("Selected Category News:")
    if selected_category:
        st.write(f"**Selected Category: {selected_category}**")  # Show selected category
        filter_news_by_category(news_df, selected_category)  # Filter and display news for the selected category
    else:
        st.write("Category select karein ya link par click karein.")

# Run the app
if __name__ == '__main__':
    news_page()
