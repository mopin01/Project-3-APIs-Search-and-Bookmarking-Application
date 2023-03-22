import unittest
from unittest.mock import patch
import sys
sys.path.append("../apis")
from imbd_api import get_imbd_data, get_wikipedia_data

class TestIMBD(unittest.TestCase):

    @patch('requests.get')
    def test_get_imbd_data(self, mock_get):
        # Mock the API response
        mock_get.return_value.json.return_value = {
            'results': [{
                'id': 'tt1234567',
                'title': 'Test Movie'
            }]
        }

        # Call the function with a search query
        imbd_data = get_imbd_data('Test Movie')

        # Check that the function returns the correct movie ID
        self.assertEqual(imbd_data['id'], 'tt1234567')

    @patch('requests.get')
    def test_get_wikipedia_data(self, mock_get):
        # Mock the API response
        mock_get.return_value.json.return_value = {
            'plotShort': {
                'plainText': 'Test plot summary'
            }
        }

        # Call the function with a movie ID
        wikipedia_summary = get_wikipedia_data('tt1234567')

        # Check that the function returns the correct plot summary
        self.assertEqual(wikipedia_summary['plotShort'], 'Test plot summary')

if __name__ == '__main__':
    unittest.main()