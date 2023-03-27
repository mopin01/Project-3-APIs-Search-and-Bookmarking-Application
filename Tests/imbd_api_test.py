import unittest
from unittest import TestCase, mock, patch
import asyncio
import aiohttp
import sys
sys.path.append("../apis")
from imbd_api import get_imbd_data, get_wikipedia_data

class TestIMBD(unittest.TestCase):
    @mock.patch('aiohttp.ClientSession')
    async def test_get_imbd_data(self, mock_session):
        # Set up the mock response for the search_url endpoint
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'results': [
                {'id': 'tt0068646', 'title': 'The Godfather'}
            ]
        }
        mock_session.return_value.get.return_value.__aenter__.return_value = mock_response

        # Call the get_imbd_data function and check if the ID is extracted correctly
        imbd_data = await get_imbd_data('The Godfather')
        self.assertEqual(imbd_data, {'id': 'tt0068646'})

    @mock.patch('aiohttp.ClientSession')
    async def test_get_wikipedia_data(self, mock_session):
        # Set up the mock response for the wikipedia_url endpoint
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'plotShort': {
                'plainText': 'The Godfather is a 1972 American crime film'
            }
        }
        mock_session.return_value.get.return_value.__aenter__.return_value = mock_response

        # Call the get_wikipedia_data function and check if the plot summary is extracted correctly
        wikipedia_data = await get_wikipedia_data('tt0068646')
        self.assertEqual(wikipedia_data, {'plotShort': 'The Godfather is a 1972 American crime film'})


if __name__ == '__main__':
    asyncio.run(unittest.main())

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