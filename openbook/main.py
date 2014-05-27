
"""

"""

from bs4 import BeautifulSoup
import requests
import readability
from readability import ReaderClient
from pprint import pprint
from settings import \
       CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD


def get_token():
	"""Returns an array with the user_key [0] and user_secret [1]"""

	token = readability.xauth(CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD)
	return token


def get_toc(url):
	"""Get 'table of contents page' and retrieve list of pages to send to Readability"""

	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	#find all links:
	for link in soup.find_all('a'):
		print(link.get('href'))



def create_client(token):
	"""Connect to Readability API
	(http://readability-python-library.readthedocs.org/en/latest/clients.html#readability.ReaderClient)"""

	rdb_client = ReaderClient(CONSUMER_KEY, CONSUMER_SECRET, token[0], token[1])
	return rdb_client


def add_bookmark(rdb_client, url):
	"""Add bookmark with given URL"""

	add_response = rdb_client.add_bookmark(url)
	pprint(add_response)

	# strip id out of url:
	location = add_response['location']
	bookmark_id = location[location.rfind('/')+1:]

	return bookmark_id


def add_tag(rdb_client, bookmark_id, tag):
	"""Add tag to new bookmark:"""

	add_tags = rdb_client.add_tags_to_bookmark(bookmark_id, tag)

	

token = get_token()
rdb_client = create_client(token)
list = ['https://nose.readthedocs.org/en/latest/writing_tests.html#test-functions', 'http://learnpythonthehardway.org/book/ex40.html']

for url in list:
	print 'adding bookmark for', url
	bookmark_id = add_bookmark(rdb_client, url)
	add_tag(rdb_client, bookmark_id, 'Book')

