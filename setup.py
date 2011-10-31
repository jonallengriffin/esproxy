import os
from setuptools import setup, find_packages

version = '0.1'

# get documentation from the README
try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

# dependencies
deps = []

setup(name='esproxy',
      version=version,
      description="ElasticSearch proxy",
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='elasticsearch',
      author='Jonathan Griffin',
      author_email='jonallengriffin@gmail.com',
      url='https://github.com/jonallengriffin/esproxy',
      license='MPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      )
