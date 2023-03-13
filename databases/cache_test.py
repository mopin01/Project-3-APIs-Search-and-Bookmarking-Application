from cache import Cache
import pytest
import unittest
from unittest import TestCase

cache = Cache()

class TestCache(TestCase):

    def test_add_movie(self):
        cache.clear_cache()
        data = {'title': 'The Matrix', 'overview': 'overview', 'release_date': '1999-03-30', 'id': '603', 'original_title': 'The Matrix'}
        cache.add_movie(data)
        assert cache.get_movie('The Matrix') == data

    def test_add_movie_duplicate(self):
        cache.clear_cache()
        data = {'title': 'The Matrix', 'overview': 'overview', 'release_date': '1999-03-30', 'id': '603', 'original_title': 'The Matrix'}
        cache.add_movie(data)
        with pytest.raises(ValueError):
            cache.add_movie(data)

    def test_get_movie_not_found(self):
        cache.clear_cache()
        assert cache.get_movie('Inception') is None

    def test_search_movies_empty(self):
        cache.clear_cache()
        assert cache.get_movie('matrix') is None

if __name__ == '__main__':
    unittest.main()