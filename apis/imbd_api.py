import asyncio
import os
from dotenv import load_dotenv
import aiohttp

# Load the environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
apiKey = os.getenv('IMBD_API_KEY')
if not apiKey:
    raise ValueError('IMBD_API_KEY not found in environment variables')

# Define the API endpoints
search_url = "https://imdb-api.com/en/API/SearchMovie"
wikipedia_url = 'https://imdb-api.com/en/API/Wikipedia/'

async def get_imbd_data(name):
    try:
        # Set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'expression': name
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, params=params) as response:
                data = await response.json()

        # Extract the ID of the first movie that matches the search
        imbd_data = {
            'id': data.get('results')[0].get('id')
        }
        return imbd_data

    except (IndexError, KeyError) as e:
        print('Error getting IMBD data: ', e)
        raise ValueError('Could not find IMBD data for given movie title.')
            
    except aiohttp.ClientError as e:
        print('Error connecting to IMBD API: ', e)
        raise ValueError('Unable to connect to IMBD API.') 
            
    except Exception as e:
        print('Unknown error occurred while getting IMBD data: ', e)
        raise ValueError('An unknown error occurred while getting IMBD data.')


async def get_wikipedia_data(id):
    try:
        # Set the headers with API key and content type
        params = {
            'apiKey': apiKey,
            'id': id
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(wikipedia_url, params=params) as response:
                data = await response.json()

        # Extract the plot summary of the movie
        wikiedia_summary = {
            "plotShort": data.get('plotShort').get('plainText')
        }
        return wikiedia_summary

    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f'Error occurred while fetching Wikipedia data: {str(e)}')
        raise Exception('Error occurred while fetching Wikipedia data.')
    except KeyError as e:
        print(f'Error occurred while parsing Wikipedia response: {str(e)}')
        raise Exception('Error occurred while parsing Wikipedia response.')
    except Exception as e:
        print(f'Unknown error occurred while fetching Wikipedia data: {str(e)}')
        raise Exception('Unknown error occurred while fetching Wikipedia data.')


async def main():
    name = "The Godfather"
    imdb_data = await get_imbd_data(name)
    wikipedia_data = await get_wikipedia_data(imdb_data['id'])
    print(wikipedia_data)

if __name__ == '__main__':
    asyncio.run(main())
