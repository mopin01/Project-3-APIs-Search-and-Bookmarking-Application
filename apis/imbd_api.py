import requests
import os
from dotenv import load_dotenv

load_dotenv()

apiKey  = os.getenv('IMBD_API_KEY')
search_url = "https://imdb-api.com/en/API/SearchMovie"
wikipedia_url = 'https://imdb-api.com/en/API/Wikipedia/'

""" This function gets the movieID of what we're searching """ 
def get_imbd_data(name):
    try:
        # set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'expression': name
        }
        response = requests.get(search_url, params=params).json()

        imbd_data = {
            'id': response.get('results')[0].get('id')
        }
        return imbd_data

    except Exception as e:
        print('Unable to get imbd data', e)

""" This function uses the returned movieID and gets the plot summary of that movie """ 
def get_wikipedia_data(id):
    try:
        # set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'id': id
        }

        response = requests.get(wikipedia_url, params=params).json()

        wikiedia_summary = {
            "plotShort": response.get('plotShort').get('plainText')
        }
        return wikiedia_summary

    except Exception as e:
        print('Unable to get imbd data', e)