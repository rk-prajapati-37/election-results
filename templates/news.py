import pandas as pd

# URL of the Google Sheets CSV
url = 'https://docs.google.com/spreadsheets/d/18Z0HOYlHqjOAHOV55JaUiHiidDvNPqkbMlqDuFBEGWQ/export?format=csv&id=18Z0HOYlHqjOAHOV55JaUiHiidDvNPqkbMlqDuFBEGWQ'

# Load the CSV data into a pandas DataFrame
news_df = pd.read_csv(url)

# Function to filter news by city
def filter_news_by_city(news, city_name):
    filtered_news = news[news['City'].str.lower() == city_name.lower()]
    if filtered_news.empty:
        print(f"No news found for city: {city_name}")
    else:
        for index, row in filtered_news.iterrows():
            print(f"News ID: {row['News Id']}")
            print(f"Heading: {row['Heading']}")
            print(f"Date Of Publish: {row['Date Of Publish']}")
            print(f"URL: {row['URL']}")
            print(f"Author: {row['Author']}")
            print(f"Editor: {row['Editor']}")
            print(f"Reviewer: {row['Reviewer']}")
            print(f"Category: {row['Category']}")
            print(f"Tags: {row['Tags']}")
            print(f"GA Views: {row['GA Views']}")
            print(f"Image: {row['Image']}")
            print(f"Display Story As Fast Check: {row['Display Story As Fast Check']}")
            print(f"Select Review: {row['Select Review']}")
            print(f"Text Caption: {row['Text Caption']}")
            print(f"Caption: {row['Caption']}")
            print(f"Language: {row['language']}")
            print(f"Article Type: {row['Article Type']}")
            print(f"Claim Review: {row['Claim Review']}")
            print(f"Claimed By: {row['Claimed By']}")
            print(f"Claim Source: {row['Claim Source']}")
            print(f"City: {row['City']}")
            print('-'*50)

# Example usage
city_name = input("Enter the city name to filter news: ")
filter_news_by_city(news_df, city_name)
