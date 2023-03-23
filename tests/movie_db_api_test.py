import unittest
from unittest.mock import patch
import sys
sys.path.append('../apis')
#/Users/minleg/Desktop/Spring2023/SoftwareDevelopmentCapstone/Project/Project3/Project-3-APIs-Search-and-Bookmarking-Application/apis
from movie_db_api import get_overview, get_json_response

class TestMovieDbApi(unittest.TestCase):
        
    @patch('requests.get')
    def test_get_overview(self, mock_data):
        mock_title = 'RRR'
        mock_original_title = 'Rise Roar Revolt'
        mock_overview = 'Indian movie'
        mock_release_date = '01/01/2023'
        mock_revenue = 1000000
        example_api_response = {'results': [{"original_title":mock_original_title,"overview":mock_overview,"release_date":mock_release_date,"revenue":mock_revenue,"title":mock_title}]}
        #mock_data.side_effects= [ example_api_response ]
        mock_data.return_value.json.return_value = example_api_response
        overview = get_overview('RRR')
        self.assertEqual(overview['title'], 'RRR')
        
    @patch('requests.get')
    def test_more_info(self, mock_data):
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()