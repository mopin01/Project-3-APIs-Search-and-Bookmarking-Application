import requests
import os

search_url = 'https://api.themoviedb.org/3/search/movie'
MOVIE_API_KEY = os.getenv('MOVIE_API_KEY')


def get_overview(name):
    # search_url = f'https://api.themoviedb.org/3/search/movie'
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
        return overview, release_date,id,original_title
    except Exception as e:
        print('Unable to fetch data', e)
        


