import unittest
from unittest.mock import patch
import sys
sys.path.append("../apis")
from youtube_trailer_api import get_movie_trailer

movie_title = "Inception"
def mock_youtube_search_execute():
    return {
        'items': [
            {
                'id': {'videoId': 'mock_video_id'},
                'snippet': {'title': f'{movie_title} - Mock Trailer',
                    'channelTitle': 'Mock Channel',
                }
            }
        ]
    }

class TestGetMovieTrailer(unittest.TestCase):

    @patch('youtube_trailer_api.build')
    
    def test_get_movie_trailer(self, mock_build):
        mock_build().search().list().execute.side_effect = mock_youtube_search_execute

        movie_title = "Inception"
        result = get_movie_trailer(movie_title)

        # Check if the function returns a dictionary.
        self.assertIsInstance(result, dict)

        # Check if the dictionary has the expected keys.
        self.assertIn("video_id", result)
        self.assertIn("video_title", result)
        self.assertIn("channel_name", result)
        self.assertIn("title", result)

        # Check if the movie_title in the result matches the input movie_title.
        self.assertEqual(result["title"], movie_title)

        # Check if the mocked values are in the result.
        self.assertEqual(result["video_id"], "mock_video_id")
        self.assertEqual(result["video_title"], f'{movie_title} - Mock Trailer')
        self.assertEqual(result["channel_name"], "Mock Channel")

if __name__ == '__main__':
    unittest.main()