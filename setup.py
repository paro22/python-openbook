try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Proof of concept for a online book parser that sends articles to Readability.com',
    'author': 'Paul Rohrbeck',
    'url': 'https://github.com/paro22/python-openbook',
    'download_url': '',
    'author_email': 'paul@paul-rohrbeck.de',
    'version': '0.1',
    'install_requires': ['nose', 'beautifulsoup4', 'readability-api'],
    'packages': ['openbook'],
    'scripts': [],
    'name': 'Readability Book Parser'
}

setup(**config)
