from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
if not API_KEY:
    raise ValueError('API key not found. Please set YOUTUBE_API_KEY environment variable.')

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def get_movie_trailer(movie_title):
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
        search_result = youtube.search().list(
            q=movie_title + ' trailer',
            type='video',
            part='id,snippet',
            maxResults=1
            
        ).execute()

        video_id = search_result['items'][0]['id']['videoId']
        video_title = search_result['items'][0]['snippet']['title']
        channel_name = search_result['items'][0]['snippet']['channelTitle']

        return {
            "video_id": video_id,
            "video_title": video_title,
            "channel_name": channel_name,
            "movie_title": movie_title
        }

    except HttpError as e:
        print(f'An error occurred while searching for {movie_title} trailer: {e}')
        return None
