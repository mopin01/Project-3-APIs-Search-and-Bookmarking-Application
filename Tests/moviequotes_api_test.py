import unittest
from unittest.mock import patch
import sys
sys.path.append("../apis")
from moviequotes_api import get_quote

class TestIMBD(unittest.TestCase):

    @patch('requests.post')
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
        movie_quote = get_quote()

        # Check that the function returns the correct quote, author and category
        self.assertEqual(movie_quote['quote'], 'Test quote')
        self.assertEqual(movie_quote['author'], 'Test author')
        self.assertEqual(movie_quote['category'], 'Test category')

if __name__ == '__main__':
    unittest.main()