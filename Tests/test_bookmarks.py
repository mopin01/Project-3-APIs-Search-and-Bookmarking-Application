import unittest
from databases.bookmarks import Bookmarks
import sqlite3

class TestBookmarks(unittest.TestCase):

    def setUp(self):
        self.bookmarks = Bookmarks(db_name='test_bookmarks.db')
        self.bookmarks.create_table({'title': 'test_movie', 'year': '2022', 'random_data': 'random_data'})


    def tearDown(self):
        self.bookmarks.delete_table()


    def test_add_movie(self):
        data = {'title': 'new_movie', 'year': '2023', 'random_data': 'random_data'}
        self.bookmarks.add_movie(data)
        self.assertTrue(self.bookmarks.movie_exists('new_movie'))
    

    def test_add_duplicate_movie(self):
        data = {'title': 'test_movie', 'year': '2022', 'random_data': 'random_data'}
        self.bookmarks.add_movie(data)
        titles = self.bookmarks.get_all_titles()
        self.assertEqual(titles.count('test_movie'), 1)
    

    def test_add_movie_with_int_data_type(self):
        data = {'title': 'new_movie', 'year': 2022, 'random_data': 'random_data'}
        self.bookmarks.add_movie(data)
        movie = self.bookmarks.get_movie_by_title('new_movie')
        self.assertEqual(movie['year'], 2022)
    

    def test_add_movie_with_boolean_data_type(self):
        data = {'title': 'new_movie', 'year': '2022', 'random_data': True}
        self.bookmarks.add_movie(data)
        movie = self.bookmarks.get_movie_by_title('new_movie')
        self.assertEqual(movie['random_data'], True)
    

    def test_add_movie_with_missing_fields(self):
        data = {'title': 'new_movie', 'year': '2023'}
        self.bookmarks.add_movie(data)
        movie = self.bookmarks.get_movie_by_title('new_movie')
        self.assertEqual(movie['random_data'], None)
    

    def test_add_invalid_movie(self):
        data = {'gdssgds': 'fasdfasdfsa'}
        with self.assertRaises(sqlite3.Error):
            self.bookmarks.add_movie(data)
    

    def test_delete_movie(self):
        self.bookmarks.delete_movie('test_movie')
        self.assertFalse(self.bookmarks.movie_exists('test_movie'))
    

    def test_delete_non_existent_movie(self):
        with self.assertRaises(ValueError):
            self.bookmarks.delete_movie('not movie')


    def test_get_all_titles(self):
        titles = self.bookmarks.get_all_titles()
        self.assertIn('test_movie', titles)
    

    def test_get_all_titles_with_no_movies(self):
        self.bookmarks.delete_movie('test_movie')
        self.assertEqual(self.bookmarks.get_all_titles(), [])


    def test_get_movie_by_title(self):
        data = self.bookmarks.get_movie_by_title('test_movie')
        self.assertEqual(data['title'], 'test_movie')
        self.assertEqual(data['year'], '2022')
    

    def test_get_non_existent_title(self):
        with self.assertRaises(ValueError):
            self.bookmarks.get_movie_by_title('not movie')


if __name__ == '__main__':
    unittest.main()
