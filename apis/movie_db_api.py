import requests
import os
from dotenv import load_dotenv

load_dotenv()

search_url = 'https://api.themoviedb.org/3/search/movie'
base_image_url = 'https://image.tmdb.org/t/p/w500/'
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
    """ This function generates the images of the movie using the movie id """
    image_url = f'https://api.themoviedb.org/3/movie/{id}/images'
    try:
        params = {
            'api_key' : MOVIE_API_KEY
        }
        image_response = requests.get(image_url, params=params).json()
        image_url_list = []
        for i in range(5):
            image_path = image_response['backdrops'][i]['file_path']
            image_path = base_image_url + image_path
            image_url_list.append(image_path)
        return image_url_list
    except Exception as e:
        print('Unable to fetch image', e)
    
def more_info(id):
    base_url = f'https://api.themoviedb.org/3/movie/{id}'
    try:
        params = {
           'api_key' : MOVIE_API_KEY 
        }
        response_data = requests.get(base_url, params=params).json()
        genre_info = response_data['genres']
        genre_list = []
        for genre in genre_info:
            genre_list.append(genre['name'])
        budget = response_data['budget']
        revenue = response_data['revenue']
        status = response_data['status']
        production_companies = response_data['production_companies']
        production_companies_list = []
        for company in production_companies:
            production_companies_list.append(company['name'])            
        return genre_list, budget, revenue, status, production_companies_list
    except Exception as e:
        print('Unable to fetch genre data', e)
        
        
    
        
        
    
    
        


