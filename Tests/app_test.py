import unittest
from unittest import TestCase  
from unittest.mock import patch
import sys
sys.path.append('../')
from app import app
from flask import request

class TestApp(TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('requests.get')
    def test_homepage(self, mock_data):
        response = self.client.get('/')
        content = response.get_data(as_text=True)
        self.assertEqual(200, response.status_code)
        
if __name__ == '__main__':
    unittest.main()