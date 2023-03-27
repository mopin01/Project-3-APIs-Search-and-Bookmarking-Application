import unittest
from unittest.mock import AsyncMock, patch
import asyncio
import sys
sys.path.append("../apis")
from moviequotes_api import get_quote

class TestMovieQuotes(unittest.TestCase):

    @patch('moviequotes_api.requests.post')
    def test_get_quote(self, mock_post):
        # Mock the API response
        mock_post.return_value.json.return_value = [
            {
                'quote': 'Test quote',
                'author': 'Test author',
                'category': 'Test category'
            }
        ]

        # Call the function to get a random movie quote
        loop = asyncio.get_event_loop()
        movie_quote = loop.run_until_complete(get_quote())

        # Check that the function returns the correct quote, author and category
        self.assertEqual(movie_quote['quote'], 'Test quote')
        self.assertEqual(movie_quote['author'], 'Test author')
        self.assertEqual(movie_quote['category'], 'Test category')

if __name__ == '__main__':
    unittest.main()