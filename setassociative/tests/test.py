"""
test.py

Priyanka Selvarathinavel

Unit test cases for setassocoative
"""
from unittest import TestCase

'''
import setassociative.cache as cache
import setassociative.exceptions as exceptions
import setassociative.cache_replacement as cache_replacement
'''

import sys
sys.path.append('.')

import setassociative.cache as cache
import setassociative.exceptions as exceptions
import setassociative.cache_replacement as cache_replacement
class TestCache(TestCase):
    """
    All testcases
    """
    def test_configuration(self):
        """
        Testing configuration options
        """
        def dummy(cache_set):
            """
            Dummy function to set callback
            """
            cache_set.popitem()

        with self.assertRaises(exceptions.IncorrectConfigurationException):
            cache.create_cache(2, 3, 'RANDOM')
        self.assertEqual(isinstance(cache.create_cache(2, 3, 'LRU'),
                                    cache_replacement.LRUcache), True)
        self.assertEqual(isinstance(cache.create_cache(2, 3, 'MRU'),
                                    cache_replacement.MRUcache), True)
        self.assertEqual(isinstance(cache.create_cache(2, 3, 'CUSTOM', dummy),
                                    cache_replacement.CustomCache), True)
        self.assertEqual(isinstance(cache.create_cache(2, 3),
                                    cache_replacement.LRUcache), True)

    def test_lru(self):
        """
        Testing LRU cache
        """

        # Create a cache with just one set
        lru_cache = cache.create_cache(1, 3, 'LRU')

        # Add 3 elements
        for i in range(1, 4):
            lru_cache.put(i, i*2)

        # Cache is full now. New entry is added. Key 1 must be replaced

        lru_cache.put(4, 8)

        if_hit, value = lru_cache.get(1)
        self.assertEqual(if_hit, False)

        # Cache hit case
        if_hit, value = lru_cache.get(4)
        self.assertEqual(if_hit, True)
        self.assertEqual(value, 8)

        #adding wrong key type
        with self.assertRaises(exceptions.TypeError):
            lru_cache.put('hello', 4)

        #adding wrong value type
        with self.assertRaises(exceptions.TypeError):
            lru_cache.put(9, 'hello')

        #2 is next to be replaced now. A get on it should replace 3 instead

        if_hit, value = lru_cache.get(2)
        lru_cache.put(5, 10)
        if_hit, value = lru_cache.get(3)
        self.assertEqual(if_hit, False)

        #4 is next to be replaced now. An update on it should replace 2 instead

        lru_cache.put(4, 80)
        lru_cache.put(6, 12)
        if_hit, value = lru_cache.get(2)
        self.assertEqual(if_hit, False)

    def test_mru(self):
        """
        Testing MRU cache
        """

        # Create a cache with just one set
        mru_cache = cache.create_cache(1, 3, 'MRU')

        # Add 3 elements
        for i in range(1, 4):
            mru_cache.put(i, i*2)

        # Cache is full now. New entry is added. Key 3 must be replaced

        mru_cache.put(4, 8)

        if_hit, value = mru_cache.get(3)
        self.assertEqual(if_hit, False)

        # Cache hit case
        if_hit, value = mru_cache.get(4)
        self.assertEqual(if_hit, True)
        self.assertEqual(value, 8)

        #adding wrong key type
        with self.assertRaises(exceptions.TypeError):
            mru_cache.put('hello', 4)

        #adding wrong value type
        with self.assertRaises(exceptions.TypeError):
            mru_cache.put(9, 'hello')

        #4 is next to be replaced now. A get on 1 should replace 1 instead

        if_hit, value = mru_cache.get(1)
        mru_cache.put(5, 10)
        if_hit, value = mru_cache.get(1)
        self.assertEqual(if_hit, False)

        #5 is next to be replaced now. An update on 2 should replace 2 instead

        mru_cache.put(2, 80)
        mru_cache.put(6, 12)
        if_hit, value = mru_cache.get(2)
        self.assertEqual(if_hit, False)

    def test_custom(self):
        """
        Testing custom cache
        """

        def my_callback_incorrect(the_set):
            """
            Supposed to remove an item from the_set but does not
            """
            the_set = the_set

        custom_cache_incorrect = cache.create_cache(1, 3, 'CUSTOM', my_callback_incorrect)

        #incorrect callback does not remove an item. Should raise an exception
        for i in range(3):
            custom_cache_incorrect.put(i, i*4)

        with self.assertRaises(exceptions.ReplacementStrategyException):
            custom_cache_incorrect.put(9, 9)
