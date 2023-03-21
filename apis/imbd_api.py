import requests
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
apiKey = os.getenv('IMBD_API_KEY')

# Define the API endpoints
search_url = "https://imdb-api.com/en/API/SearchMovie"
wikipedia_url = 'https://imdb-api.com/en/API/Wikipedia/'

""" This function gets the movieID of what we're searching """
def get_imbd_data(name):
    try:
        # Set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'expression': name
        }
        # Send a GET request to the IMBD API to search for movies
        response = requests.get(search_url, params=params).json()

        # Extract the ID of the first movie that matches the search
        imbd_data = {
            'id': response.get('results')[0].get('id')
        }
        return imbd_data

    except Exception as e:
        print('Unable to get imbd data', e)

""" This function uses the returned movieID and gets the plot summary of that movie """
def get_wikipedia_data(id):
    try:
        # Set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'id': id
        }
        # Send a GET request to the IMBD API to get the plot summary of a movie
        response = requests.get(wikipedia_url, params=params).json()

        # Extract the plot summary of the movie
        wikiedia_summary = {
            "plotShort": response.get('plotShort').get('plainText')
        }
        return wikiedia_summary

    except Exception as e:
        print('Unable to get imbd data', e)
