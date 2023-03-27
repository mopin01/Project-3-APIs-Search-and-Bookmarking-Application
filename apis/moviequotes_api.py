# import necessary libraries
import requests
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# get API key from environment variable
X_RapidAPI_Key = os.getenv('X-RapidAPI-Key')
if not X_RapidAPI_Key:
    raise ValueError('X_RapidAPI_Key not found in environment variables')

search_url = 'https://andruxnet-random-famous-quotes.p.rapidapi.com/?count=1&cat=movies'

# function to get a random famous movie quote
def get_quote():
    try:
        # set the headers with API key and content type
        headers = {
            'X-RapidAPI-Key': X_RapidAPI_Key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # send a post request to the API endpoint to get a random movie quote
        response = requests.post(search_url, headers=headers)
        response.raise_for_status() # check if there's any error in the response

        # extract the quote, author and category from the response
        data = response.json()[0]
        # return a dictionary with the quote, author and category
        movie_quote = {
            'quote': data['quote'],
            'author': data['author'],
            'category': data['category']
        }
        return movie_quote
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error occurred: {e}')
    except requests.exceptions.Timeout as e:
        print(f'Request timed out: {e}')
    except requests.exceptions.RequestException as e:
        print(f'An error occurred while processing the request: {e}')


# main block of code that runs if the script is executed directly
if __name__ == '__main__':
    # print a message indicating that a quote is being fetched
    print('Fetching quote...')
    # call the get_quote function to get a random movie quote
    movie_quote = get_quote()
    # print the quote
    print(movie_quote['quote'] + ' - ' + movie_quote['author'] )