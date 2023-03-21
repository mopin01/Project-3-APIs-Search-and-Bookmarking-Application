import unittest
from unittest.mock import patch
import sys
sys.path.append("../apis")
from imbd_api import get_imbd_data, get_wikipedia_data

class TestIMBD(unittest.TestCase):

    @patch('get_imbd_data.requests.get')
    def test_get_imbd_data(self, mock_get):
        # Mock response from the IMBD API
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            'results': [
                {
                    'id': 'tt0111161',
                    'title': 'The Shawshank Redemption',
                }
            ]
        }

if __name__ == '__main__':
    unittest.main()