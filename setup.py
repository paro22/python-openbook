try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '',
    'author': 'Paul Rohrbeck',
    'url': '',
    'download_url': '',
    'author_email': 'paul@paul-rohrbeck.de',
    'version': '0.1',
    'install_requires': ['nose', 'beautifulsoup4', 'readability-api'],
    'packages': ['openbook'],
    'scripts': [],
    'name': 'Readability Book Reader POC'
}

setup(**config)
