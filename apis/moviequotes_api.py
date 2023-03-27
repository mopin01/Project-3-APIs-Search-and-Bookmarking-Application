# import necessary libraries
import requests
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# get API key from environment variable
X_RapidAPI_Key = os.getenv('X-RapidAPI-Key')
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
        # extract the quote, author and category from the response
        data = response.json()[0]
        # return a dictionary with the quote, author and category
        movie_quote = {
            'quote': data['quote'],
            'author': data['author'],
            'category': data['category']
        }
        return movie_quote
    except Exception as e:
        print('Unable to fetch quote', e)

# main block of code that runs if the script is executed directly
if __name__ == '__main__':
    # print a message indicating that a quote is being fetched
    print('Fetching quote...')
    # call the get_quote function to get a random movie quote
    movie_quote = get_quote()
    # print the quote
    print(movie_quote['quote'] + ' - ' + movie_quote['author'] )