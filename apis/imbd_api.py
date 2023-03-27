import asyncio
import os
from dotenv import load_dotenv
import aiohttp

# Load the environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
apiKey = os.getenv('IMBD_API_KEY')

# Define the API endpoints
search_url = "https://imdb-api.com/en/API/SearchMovie"
wikipedia_url = 'https://imdb-api.com/en/API/Wikipedia/'

def search_movies(name):
    try:
        # Set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'expression': name
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, params=params) as response:
                data = await response.json()

        # Extract the ID and title of all movies that match the search
        imdb_data = []
        for result in data.get('results', []):
            imdb_data.append({
                'title': result.get('title')
            })
        return imdb_data

    except Exception as e:
        print('Unable to get search movies', e)

def get_imbd_data(name):
    try:
        # Set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'expression': name
        }
        response = requests.get(search_url, params=params)
        data = response.json()

        # Extract the ID of the first movie that matches the search
        imbd_data = {
            'id': data.get('results')[0].get('id')
        }
        return imbd_data

    except Exception as e:
        print('Unable to get imbd data', e)

def get_wikipedia_data(id):
    try:
        # Set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'id': id
        }
        response = requests.get(wikipedia_url, params=params)
        data = response.json()

        # Extract the plot summary of the movie
        wikiedia_summary = {
            "plotShort": data.get('plotShort').get('plainText')
        }
        return wikiedia_summary

    except Exception as e:
        print('Unable to get imbd data', e)

def main():
    name = "The Godfather"
    imdb_data = get_imbd_data(name)
    wikipedia_data = get_wikipedia_data(imdb_data['id'])
    print(wikipedia_data)

if __name__ == '__main__':
    main()
