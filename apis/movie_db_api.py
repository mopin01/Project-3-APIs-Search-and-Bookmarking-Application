import requests
import os
from dotenv import load_dotenv

load_dotenv()

search_url = 'https://api.themoviedb.org/3/search/movie'
base_image_url = 'https://image.tmdb.org/t/p/w500'
MOVIE_API_KEY = os.getenv('MOVIE_API_KEY')
if not apiKey:
    raise ValueError('MOVIE_API_KEY not found in environment variables')

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
        image_response = get_json_response(image_url, params)
        image_url_list = get_image_response(image_response)
        return image_url_list
    except Exception as e:
        print('Unable to fetch image', e)

def get_image_response(image_response,number_of_image=5):
    """ This function returns a list of image related to the  movie , you can get n number of images by changing number_of_image,
    default is set at 5 images. It checks if the number of image returned from the list is more than five, if it is, it returns only five images
    and if it is less than five, it returns whatever images there is."""
    image_url_list = []
    image_response_list = image_response['backdrops']
    try:
        if len(image_response_list) >= number_of_image: # if response has more than five images, get only five image paths
            for img in range(number_of_image):
                image_path = image_response_list[img]['file_path']
                image_path = base_image_url + image_path
                image_url_list.append(image_path)
            return image_url_list
        elif len(image_response_list) > 0 and len(image_response_list) < 5:
            for img in range(len(image_response_list)): # otherwise get the paths of images available
                image_path = image_response_list[img]['file_path']
                image_path = base_image_url + image_path
                image_url_list.append(image_path)
            return image_url_list
        else: # if no images avaiable at all
            return None
                
    except Exception as e:
        print('Unable to get images', e)
    
    
def more_info(id):
    """ This function gets more data about the movie using the movie id - data like genre, production companies associated with the movie, business
    information like revenue and budget."""
    base_url = f'https://api.themoviedb.org/3/movie/{id}'
    try:
        params = {
           'api_key' : MOVIE_API_KEY 
        }
        response_data = get_json_response(base_url,params)
        genre_list = get_genre_list(response_data)
        business_data = get_business_data(response_data)
        production_companies_list = get_production_companies(response_data)          
        return genre_list, business_data, production_companies_list
    except Exception as e:
        print('Unable to fetch genre data', e)

def get_genre_list(response_data):
    """ This function gets the genre information of the movie """
    try:
        genre_info = response_data['genres']
        genre_list = []
        for genre in genre_info:
            genre_list.append(genre['name'])
        return genre_list
    except Exception as e:
        print('Unable to get genre information', e)
    
def get_business_data(response_data):
    """ This function gets the business data related to the movie, like budget and revenue """
    try:
        business_data = {
            'budget' : response_data.get('budget'),
            'revenue' : response_data.get('revenue'),
            'status' : response_data.get('status')
        }
        return business_data
    except Exception as e:
        print('Unable to get business data', e)
        
def get_production_companies(response_data):
    """ Gets the list of production companies associated with the movie """
    try:
        production_companies = response_data['production_companies']
        production_companies_list = []
        for company in production_companies:
            production_companies_list.append(company['name'])
        return production_companies_list
    except Exception as e:
        print('Unable to get production companies associated with the movie', e)
        
        
def get_json_response(url, params):
    """ This function connects to the url with the params given and gets the json response """
    try:
        response = requests.get(url, params=params).json()
        # response.raise_for_status()
        return response
    except Exception as e:
        print('Unable to fetch data', e)

        
    
        
        
    
    
        


