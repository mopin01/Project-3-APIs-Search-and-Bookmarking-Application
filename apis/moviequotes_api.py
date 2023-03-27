import requests
import os
from dotenv import load_dotenv
import asyncio

# load environment variables from .env file
load_dotenv()

# get API key from environment variable
X_RapidAPI_Key = os.getenv('X-RapidAPI-Key')
if not X_RapidAPI_Key:
    raise ValueError('X_RapidAPI_Key not found in environment variables')

search_url = 'https://andruxnet-random-famous-quotes.p.rapidapi.com/?count=1&cat=movies'

# function to get a random famous movie quote
async def get_quote():
    try:
        # set the headers with API key and content type
        headers = {
            'X-RapidAPI-Key': X_RapidAPI_Key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # send a post request to the API endpoint to get a random movie quote
        response = await asyncio.to_thread(requests.post, search_url, headers=headers)
        response.raise_for_status() # check if there's any error in the response
        # extract the quote, author and category from the response
        data = response.json()[0]
        # extract the quote, author and category from the response
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


async def main():
    # print a message indicating that a quote is being fetched
    print('Fetching quote...')
        # call the get_quote function to get a random movie quote
    movie_quote = await get_quote()
    # print the quote
    print(movie_quote['quote'] + ' - ' + movie_quote['author'])

if __name__ == '__main__':
    asyncio.run(main())