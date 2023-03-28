import requests
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
apiKey = os.getenv('IMBD_API_KEY')
if not apiKey:
    raise ValueError('IMBD_API_KEY not found in environment variables')

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

        # Send a GET request to the IMBD API to search for movies
        response = requests.get(search_url, params=params).json()

        # Extract the ID and title of all movies that match the search
        imdb_data = []
        for result in response.get('results', []):
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
            'id': response.get('results')[0].get('id')
        }
        return imbd_data

    except (IndexError, KeyError) as e:
        print('Error getting IMBD data: ', e)
        raise ValueError('Could not find IMBD data for given movie title.')
        
    except Exception as e:
        print('Unknown error occurred while getting IMBD data: ', e)
        raise ValueError('An unknown error occurred while getting IMBD data.')

""" This function uses the returned movieID and gets the plot summary of that movie """
def get_wikipedia_data(id):
    try:
        # Set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'id': id
        }

        response = requests.get(wikipedia_url, params=params)
        data = response.json()

        # Send a GET request to the IMBD API to get the plot summary of a movie
        response = requests.get(wikipedia_url, params=params).json()


        # Extract the plot summary of the movie
        wikiedia_summary = {
            "plotShort": response.get('plotShort').get('plainText')
        }
        return wikiedia_summary

    except KeyError as e:
        print(f'Error occurred while parsing Wikipedia response: {str(e)}')
        raise Exception('Error occurred while parsing Wikipedia response.')

    except Exception as e:
        print(f'Unknown error occurred while fetching Wikipedia data: {str(e)}')
        raise Exception('Unknown error occurred while fetching Wikipedia data.')


def main():
    name = "The Godfather"
    imdb_data = get_imbd_data(name)
    wikipedia_data = get_wikipedia_data(imdb_data['id'])
    print(wikipedia_data)

if __name__ == '__main__':
    main()

