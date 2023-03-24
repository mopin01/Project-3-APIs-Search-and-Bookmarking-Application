import unittest
from databases.cache import Cache

class TestBookmarks(unittest.TestCase):

    def setUp(self):
        self.cache = Cache(db_name='test_cache.db')
        self.cache.create_table({'title': 'test_movie', 'year': '2022', 'random_data': 'random_data'})


    def tearDown(self):
        self.cache.delete_table()


    def test_add_movie(self):
        data = {'title': 'new_movie', 'year': '2023', 'random_data': 'random_data'}
        self.cache.add_movie(data)
        self.assertTrue(self.cache.movie_exists('new_movie'))


    def test_get_movie(self):
        data = self.cache.get_movie('test_movie')
        self.assertEqual(data['title'], 'test_movie')
        self.assertEqual(data['year'], '2022')


    def test_clear_cache(self):
        self.cache.clear_cache()
        self.assertFalse(self.cache.movie_exists('test_movie'))


if __name__ == '__main__':
    unittest.main()
