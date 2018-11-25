import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()

setuptools.setup(name='setassociative',
      version='0.1',
      description='n-way set associative cache',
      long_description=readme(),
      test_suite='nose.collector',
      tests_require=['nose'],
      #url='http://github.com/storborg/funniest',
      author='Priyanka Selvarathinavel',
      author_email='priyanka.nessie@gmail.com',
      #license='MIT',
      #packages=['setassociative'],
      packages=setuptools.find_packages(),
      zip_safe=True)
