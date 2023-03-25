import unittest
from databases.bookmarks import Bookmarks

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


    def test_get_all_titles(self):
        titles = self.bookmarks.get_all_titles()
        self.assertIn('test_movie', titles)


    def test_get_movie_by_title(self):
        data = self.bookmarks.get_movie_by_title('test_movie')
        self.assertEqual(data['title'], 'test_movie')
        self.assertEqual(data['year'], '2022')


    def test_delete_movie(self):
        self.bookmarks.delete_movie('test_movie')
        self.assertFalse(self.bookmarks.movie_exists('test_movie'))


if __name__ == '__main__':
    unittest.main()
