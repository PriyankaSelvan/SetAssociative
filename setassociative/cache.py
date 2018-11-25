"""
File: cache.py

Author: Priyanka Selvarathinavel

Contains method to instantiate required cache.
"""
import sys
sys.path.append('.')
import setassociative.cache_replacement as cache_replacement
import setassociative.exceptions as exceptions


def create_cache(set_count, set_size, strategy='LRU', callback=None):
    """
    Returns instantiated specialized cache object based on strategy.

    Raises exceptions.IncorrectConfigurationException
    for invalid strategy.

    :param set_count: Number of sets in the cache
    :type set_count: int
    :param set_size: Number of entries in a cache set
    :type set_size: int
    :param strategy: Replacement strategy 'LRU', 'MRU' or 'CUSTOM'
    :type strategy: str
    :param callback: Method that removes an element from a cache set
    :type callback: argument: OrderedDict
    :return: Specialized cache object
    :rtype: subclasses of cacheReplacement.Cache
    """
    if strategy == 'LRU':
        return cache_replacement.LRUcache(set_count, set_size)
    elif strategy == 'MRU':
        return cache_replacement.MRUcache(set_count, set_size)
    elif strategy == 'CUSTOM':
        return cache_replacement.CustomCache(set_count, set_size,
                                             callback)
    else:
        raise exceptions.IncorrectConfigurationException\
            ('Use LRU, MRU or CUSTOM')
