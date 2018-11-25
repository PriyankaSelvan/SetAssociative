"""
File: cache_replacement.py

Author: Priyanka Selvarathinavel

Contains abstract Cache class followed by specialized cache classes
based on replacement strategies.

"""

import sys
sys.path.append('.')

from abc import ABC, abstractmethod
import random
import collections
import setassociative.exceptions as exceptions


class Cache(ABC):
    """
    Abstract class for caches of different replacement strategies
    """

    def __init__(self, set_count, set_size):
        """
        :param set_count: Number of sets
        :type set_count: int
        :param set_size: Number of cache entries in a set
        :type set_size: int
        """
        self.contents = [collections.OrderedDict()
                         for _ in range(set_count)]
        self.set_count = set_count
        self.set_size = set_size
        self.key_type = None
        self.value_type = None
    '''

    def print_contents(self):
        """
        Displays contents of the cache. Debugging purposes.
        """
        i = 0
        print('=======')
        for set_ in self.contents:
            print('---Set:' + str(i) + '---')
            for key in set_:
                print(str(key) + '->' + str(set_[key]))
            i = i + 1
        print('=======')
    '''

    def get_set(self, key):
        """
        Calculates set value for a new key.

        :param key: Key to be inserted
        :type key: any
        :return: tag value, set value
        :rtype: int, int
        """
        tag = hash(key)
        random.seed(tag)
        set_ = random.randint(0, self.set_count - 1)
        return set_

    @abstractmethod
    def strategy_to_replace(self, set_):
        """
        Abstract method. Must be implemented by subclasses.
        """
        pass


    def put(self, key, value):
        """
        Inserts a new key into the cache

        :param key: Key to be inserted
        :type key: any
        :param value: Value for the key to be inserted
        :type value: any
        """
        if not self.key_type:
            self.key_type = type(key)
            self.value_type = type(value)

        if not (isinstance(key, self.key_type) and
                    isinstance(value, self.value_type)):
            raise exceptions.TypeError('Either key or value '
                                       'does not match the '
                                       'existing key value types')

        set_ = self.get_set(key)
        if key in self.contents[set_]:
            self.contents[set_].pop(key)

        elif len(self.contents[set_]) >= self.set_size:
            self.strategy_to_replace(set_)

        if len(self.contents[set_]) >= self.set_size:
            raise exceptions.ReplacementStrategyException\
                ('Replacement strategy has not removed an element')


        self.contents[set_][key] = value
        # self.print_contents()
        print('Successfully inserted data')

    def get(self, key):
        """
        Returns value in cache for a given key.

        :param key: Key we need value for
        :type key: any
        :return: (True, value of key)  or (False ,None)
        :rtype: bool, any
        """
        set_ = self.get_set(key)
        if key in self.contents[set_]:
            value = self.contents[set_].pop(key)
            self.contents[set_][key] = value
            # self.print_contents()
            return True, value

        # self.print_contents()
        return False, None


class LRUcache(Cache):
    """
    Specialized class for LRU replacement strategy cache.
    """
    def strategy_to_replace(self, set_):
        """
        Deletes item in cache set according to LRU strategy

        :param set_: cache set to delete from
        :type set_: int
        """
        self.contents[set_].popitem(last=False)


class MRUcache(Cache):
    """
    Specialized class for MRU replacement strategy cache.
    """

    def strategy_to_replace(self, set_):
        """
        Deletes item in cache set according to MRU strategy

        :param set_: cache set to delete from
        :type set_: int
        """
        self.contents[set_].popitem(last=True)


class CustomCache(Cache):
    """
       Specialized class for CUSTOM replacement strategy cache.
    """
    def __init__(self, set_count, set_size, callback):
        """
        Specialized class to accommodate custom cache
        replacement strategy

        :param set_count: Number of sets in the cache
        :type set_count: int
        :param set_size: Number of cache entries in a set
        :type set_size: int
        :param callback: User defined method that removes
        an element from a cache set
        :type callback: argument: OrderedDict
        """
        super().__init__(set_count, set_size)
        self.callback = callback

    def strategy_to_replace(self, set_):
        """
        Calls provided callback function that Removes an element
        from the cache set

        :param set_: cache set to delete from
        :type set_: int
        """
        self.callback(self.contents[set_])
