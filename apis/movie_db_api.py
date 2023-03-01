import requests
import os
from dotenv import load_dotenv

load_dotenv()

search_url = 'https://api.themoviedb.org/3/search/movie'
MOVIE_API_KEY = os.getenv('MOVIE_API_KEY')


def get_overview(name):
    """ This function gets details about the movie by title - like release-date, overview and other useful information """
    try:
        params = {
            'query' : name,
            'api_key' : MOVIE_API_KEY
        }
        response = requests.get(search_url, params=params).json()
        overview = response['results'][0]['overview']
        id = response['results'][0]['id'] # can be used to query more info
        original_title = response['results'][0]['original_title']
        release_date = response['results'][0]['release_date']
        title = response['results'][0]['title']
        return overview, release_date,id,original_title,title
    except Exception as e:
        print('Unable to fetch data', e)

def get_image(id):
    """ This function generates the image of the movie using the movie id """
    image_url = f'https://api.themoviedb.org/3/movie/{id}/images'
    try:
        params = {
            'api_key' : MOVIE_API_KEY
        }
        image_response = requests.get(image_url, params=params).json()
        image_url_list = []
        for i in range(5):
            image_path = image_response['backdrops'][i]['file_path']
            image_path = 'https://image.tmdb.org/t/p/w500/' + image_path
            image_url_list.append(image_path)
        return image_url_list
    except Exception as e:
        print('Unable to fetch image', e)    
    
        
        
    
    
        


