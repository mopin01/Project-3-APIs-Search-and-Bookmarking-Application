import unittest
from unittest.mock import patch
import sys
sys.path.append('../apis')
from movie_db_api import get_overview, get_json_response, get_image

class TestMovieDbApi(unittest.TestCase):
        
    @patch('requests.get')
    def test_get_overview(self, mock_data):
        mock_title = 'RRR'
        mock_original_title = 'Rise Roar Revolt'
        mock_overview = 'Indian movie'
        mock_release_date = '01/01/2023'
        mock_revenue = 1000000
        example_api_response = {'results': [{"original_title":mock_original_title,"overview":mock_overview,"release_date":mock_release_date,"revenue":mock_revenue,"title":mock_title, "id": 123}]}
        #mock_data.side_effects= [ example_api_response ]
        mock_data.return_value.json.return_value = example_api_response
        overview = get_overview('RRR')
        expected_overview = {
            "original_title":mock_original_title,
            "overview":mock_overview,
            "release_date":mock_release_date,
            "title":mock_title,
            "id": 123
        }
        self.assertEqual(overview, expected_overview)
        
    @patch('requests.get')
    def test_get_image(self, mock_data):
        mock_image_url = 'https://image.tmdb.org/t/p/w500/rzdPqYx7Um4FUZeD8wpXqjAUcEm.jpg'
        mock_image_url_list = [ mock_image_url,'https://image.tmdb.org/t/p/w500/6VmFqApQRyZZzmiGOQq2C92jyvH.jpg',
                                'https://image.tmdb.org/t/p/w500/yDI6D5ZQh67YU4r2ms8qcSbAviZ.jpg',
                                'https://image.tmdb.org/t/p/w500/3WjbxaqYB4vAbdUfdr5vbglD2JZ.jpg',
                                'https://image.tmdb.org/t/p/w500/vIAm7UDNjGztvUYtDuS0in1VAXg.jpg']
        example_api_response = {"backdrops":[{"file_path": '/rzdPqYx7Um4FUZeD8wpXqjAUcEm.jpg'}, 
                                             {"file_path":"/6VmFqApQRyZZzmiGOQq2C92jyvH.jpg"},
                                             {"file_path":"/yDI6D5ZQh67YU4r2ms8qcSbAviZ.jpg"},
                                             {"file_path":"/3WjbxaqYB4vAbdUfdr5vbglD2JZ.jpg"},
                                             {"file_path":"/vIAm7UDNjGztvUYtDuS0in1VAXg.jpg"}]}
        mock_data.return_value.json.return_value = example_api_response
        image_url_list = get_image(597)
        self.assertEqual(mock_image_url_list, image_url_list)

if __name__ == '__main__':
    unittest.main()