from bookmarks import Bookmarks
import pytest
import unittest
from unittest import TestCase

bookmarks = Bookmarks()

class TestBookmarks(TestCase):

    def test_add_movie(self):
        bookmarks.clear_database()
        data = {'title': 'The Matrix', 'overview': 'overview', 'release_date': '1999-03-30', 'id': '603', 'original_title': 'The Matrix'}
        bookmarks.add_movie(data)
        assert bookmarks.get_movie('The Matrix') == data

    def test_add_duplicate_movie(self):
        bookmarks.clear_database()
        data1 = {'title': 'The Matrix', 'overview': 'test1', 'release_date': '1999-03-30', 'id': '603', 'original_title': 'The Matrix'}
        data2 = {'title': 'The Matrix', 'overview': 'test2', 'release_date': '1999-03-30', 'id': '603', 'original_title': 'The Matrix'}
        bookmarks.add_movie(data1)
        bookmarks.add_movie(data2)
        assert bookmarks.get_movie('The Matrix') == data2

    def test_delete_movie(self):
        bookmarks.clear_database()
        data = {'title': 'The Matrix', 'overview': 'overview', 'release_date': '1999-03-30', 'id': '603', 'original_title': 'The Matrix'}
        bookmarks.add_movie(data)
        bookmarks.delete_movie('The Matrix')
        assert bookmarks.get_movie('The Matrix') is None

    def test_delete_movie_not_found(self):
        bookmarks.clear_database()
        with pytest.raises(ValueError):
            bookmarks.delete_movie('The Matrix')

    def test_get_movie_not_found(self):
        bookmarks.clear_database()
        assert bookmarks.get_movie('Inception') is None

    def test_search_movies_empty(self):
        bookmarks.clear_database()
        assert bookmarks.get_movie('matrix') is None
    
    def test_get_all_movies(self):
        bookmarks.clear_database()
        data1 = {'title': 'The Matrix', 'overview': 'overview', 'release_date': '1999-03-30', 'id': '603', 'original_title': 'The Matrix'}
        data2 = {'title': 'The Shawshank Redemption', 'overview': 'overview', 'release_date': '1994-09-23', 'id': '278', 'original_title': 'The Shawshank Redemption'}
        bookmarks.add_movie(data1)
        bookmarks.add_movie(data2)
        assert bookmarks.get_all_movies() == [data1, data2]

if __name__ == '__main__':
    unittest.main()