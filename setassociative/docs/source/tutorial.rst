**************
Usage Tutorial
**************

LRU Cache
#########

Least recently used items are discarded when a cache set is full.
To instantiate this type of cache, the number of sets and the
number of entries in each set is required.

A usage example is given below

::

    import setassociative.cache

    # Arguments: number of sets, set size, strategy
    lru_cache = setassociative.cache.create_cache(2, 3, 'LRU')

    # Putting value. Needs key, value as arguments
    lru_cache.put(2, 'two')

    # Getting. Requires key. Returns a boolean (True if cache hit)
    # with the value
    # Value is None if cache miss
    hit, val = lru_cache.get(2)
    if hit:
        print('Value:' + str(val))
    else:
        print('Cache miss!')

MRU Cache
#########

Most recently used items are discarded when a cache set is full.
To instantiate this type of cache, the number of sets and the
number of entries in each set is required.

A usage example is given below

::

    import setassociative.cache

    # Arguments: number of sets, set size, strategy
    mru_cache = setassociative.cache.create_cache(2, 3, 'MRU')

    # Putting value. Needs key, value as arguments
    mru_cache.put(2, 'two')

    # Getting. Requires key. Returns a boolean (True if cache hit)
    # with the value
    # Value is None if cache miss
    hit, val = mru_cache.get(2)
    if hit:
        print('Value:' + str(val))
    else:
        print('Cache miss!')

Custom Cache
############

A cache with a custom replacement strategy can be implemented.
To instantiate this type of cache, the number of sets and the
number of entries in each set is required.
Along with this, a callback function has to be passed implementing
the replacement strategy.

Writing custom replacement callback
***********************************

* Write a method that takes just one argument of type collections.OrderedDict
* This will be the cache set from where one entry has to be discarded
* Write method body that discards required item from the OrderedDict
* The OrderedDict is ordered by the order of access (put and get) in the cache set

A usage example is given below

::

    import setassociative.cache

    # Custom callback popping the first item in
    # the collections.OrderedDict
    def my_callback(the_set):
        the_set.popitem(last=False)

    # Arguments: number of sets, set size, strategy, callback
    custom_cache = setassociative.cache.create_cache\
                   (2, 3, 'CUSTOM', my_callback)

    # Putting value. Needs key, value as arguments
    custom_cache.put(2, 'two')

    # Getting. Requires key. Returns a boolean (True if cache hit)
    # with the value
    # Value is None if cache miss
    hit, val = custom_cache.get(2)
    if hit:
        print('Value:' + str(val))
    else:
        print('Cache miss!')