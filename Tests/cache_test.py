import unittest
from databases.cache import Cache
import sqlite3

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
    

    def test_add_duplicate_movie(self):
        data = {'title': 'test_movie', 'year': '2022', 'random_data': 'random_data'}
        self.cache.add_movie(data)
        titles = self.cache.get_all_titles()
        self.assertEqual(titles.count('test_movie'), 1)
    

    def test_add_movie_with_int_data_type(self):
        data = {'title': 'new_movie', 'year': 2022, 'random_data': 'random_data'}
        self.cache.add_movie(data)
        movie = self.cache.get_movie_by_title('new_movie')
        self.assertEqual(movie['year'], 2022)
    

    def test_add_movie_with_boolean_data_type(self):
        data = {'title': 'new_movie', 'year': '2022', 'random_data': True}
        self.cache.add_movie(data)
        movie = self.cache.get_movie_by_title('new_movie')
        self.assertEqual(movie['random_data'], True)
    

    def test_add_movie_with_missing_fields(self):
        data = {'title': 'new_movie', 'year': '2023'}
        self.cache.add_movie(data)
        movie = self.cache.get_movie_by_title('new_movie')
        self.assertEqual(movie['random_data'], None)
    

    def test_add_invalid_movie(self):
        data = {'gdssgds': 'fasdfasdfsa'}
        with self.assertRaises(sqlite3.Error):
            self.cache.add_movie(data)
    

    def test_clear_cache(self):
        self.cache.clear_cache()
        self.assertEqual(self.cache.get_all_titles(), [])


    def test_get_all_titles(self):
        titles = self.cache.get_all_titles()
        self.assertIn('test_movie', titles)


    def test_get_movie_by_title(self):
        data = self.cache.get_movie_by_title('test_movie')
        self.assertEqual(data['title'], 'test_movie')
        self.assertEqual(data['year'], '2022')
    

    def test_get_non_existent_title(self):
        with self.assertRaises(ValueError):
            self.cache.get_movie_by_title('not movie')


if __name__ == '__main__':
    unittest.main()
