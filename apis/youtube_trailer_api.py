from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_movie_trailer(movie_title):
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
        search_response = youtube.search().list(
            q=movie_title + ' trailer',
            type='video',
            part='id,snippet',
            maxResults=1
        ).execute()
        video_id = search_response['items'][0]['id']['videoId']
        print(f'https://www.youtube.com/watch?v={video_id}')
        print(search_response)
        return {"video_id" : video_id , "title" : movie_title }
        
    except HttpError as e:
        print('An unexpected error occurred: %s' % e)
