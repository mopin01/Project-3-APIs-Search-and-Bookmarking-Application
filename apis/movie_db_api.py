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
        response = get_json_response(search_url,params)
        overview_data = load_overview_data(response)
        return overview_data
    except Exception as e:
        print('Unable to fetch data', e)

def load_overview_data(response):
    """ This methods gets the overview data dictionary required from the response json data"""
    try:
        sub_response = response.get('results')[0]
        overview_data = {
                'overview' : sub_response.get('overview'),
                'id': sub_response.get('id'),
                'release_date' : sub_response.get('release_date'),
                'original_title' : sub_response.get('original_title'),
                'title' : sub_response.get('title')
            }
        return overview_data
    except Exception as e:
        print('Unable to fetch data', e)
    
    

def get_image(id):
    """ This function generates the images of the movie using the movie id """
    image_url = f'https://api.themoviedb.org/3/movie/{id}/images'
    try:
        params = {
            'api_key' : MOVIE_API_KEY
        }
        #image_response = requests.get(image_url, params=params).json()
        image_response = get_json_response(image_url, params)
        image_url_list = []
        for i in range(5):
            image_path = image_response['backdrops'][i]['file_path']
            image_path = base_image_url + image_path
            image_url_list.append(image_path)
        return image_url_list
    except Exception as e:
        print('Unable to fetch image', e)
    
def more_info(id):
    """ This function gets more data about the movie using the movie id - data like genre, production companies associated with the movie, business
    information like revenue and budget."""
    base_url = f'https://api.themoviedb.org/3/movie/{id}'
    try:
        params = {
           'api_key' : MOVIE_API_KEY 
        }
        #response_data = requests.get(base_url, params=params).json()
        response_data = get_json_response(base_url,params)
        genre_info = response_data['genres']
        genre_list = []
        for genre in genre_info:
            genre_list.append(genre['name'])
        business_data = {
            'budget' : response_data.get('budget'),
            'revenue' : response_data.get('revenue'),
            'status' : response_data.get('status')
        }
        production_companies = response_data['production_companies']
        production_companies_list = []
        for company in production_companies:
            production_companies_list.append(company['name'])            
        return genre_list, business_data, production_companies_list
    except Exception as e:
        print('Unable to fetch genre data', e)
        
        
def get_json_response(url, params):
    """ This function connects to the url with the params given and gets the json response """
    try:
        response = requests.get(url, params=params).json()
        return response
    except Exception as e:
        print('Unable to fetch data', e)
        
    
        
        
    
    
        


