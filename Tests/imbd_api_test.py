import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'apis')))
from imbd_api import get_imbd_data, get_wikipedia_data

class TestAPIRequests(unittest.TestCase):

    @patch('imbd_api.requests.get')
    def test_get_imbd_data(self, mock_get):
        # Mock the response from the API
        mock_data = {
            'results': [
                {'id': 'tt0068646', 'title': 'The Godfather', 'description': '...'},
                {'id': 'tt0071562', 'title': 'The Godfather: Part II', 'description': '...'}
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        
        # Call the function to test
        result = get_imbd_data('The Godfather')
        
        # Assert that the expected result was returned
        self.assertEqual(result, {'id': 'tt0068646'})

    @patch('imbd_api.requests.get')
    def test_get_wikipedia_data(self, mock_get):
        # Mock the response from the API
        mock_data = {
            'id': 'tt0068646',
            'title': 'The Godfather',
            'plotShort': {
                'plainText': 'The aging patriarch of an organized crime dynasty...'
            }
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        
        # Call the function to test
        result = get_wikipedia_data('tt0068646')
        
        # Assert that the expected result was returned
        self.assertEqual(result, {"plotShort": "The aging patriarch of an organized crime dynasty..."})

if __name__ == '__main__':
    unittest.main()
