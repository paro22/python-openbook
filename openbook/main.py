
"""
MAIN
"""

from bs4 import BeautifulSoup
import requests
import readability
from readability import ReaderClient
from pprint import pprint
from settings import \
       CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD
from urlparse import urlsplit


def get_token():
    """
    Returns an array with the user_key [0] and user_secret [1]
    """

    token = readability.xauth(CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD)
    return token


def get_toc(url):
    """
    Get 'table of contents page' and retrieve list of pages to send to Readability
    """

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    url_list = []

    # find all links:
    for link in soup.find_all('a'):
        href = str(link.get('href'))

        if href != '' and href[0] != '#' and 'None' not in href and 'mailto:' not in href:
            href = sanitize_url(link.get('href'), url)
            url_list.append(href)

    return remove_duplicate_urls(url_list)


def remove_duplicate_urls(seq, idfun=None): 
    """
    Remove unnessary duplicates from the list of URLs

    The function is borrowed from the nice gentlemen at http://www.peterbe.com/plog/uniqifiers-benchmark
    """

    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result


def sanitize_url(url, givenUrl):
    """
    Here we have to account for internal links, so if there's no netloc,
    prepend the current (given) URL

    SplitResult(scheme='http', netloc='', path=u'abc.html', query='', fragment=u'')
    """

    # @todo extend this to https and make it more error tolerant
    urlParts = urlsplit(url)
    if 'http' in url:
        sanitizedUrl = 'http://' + urlParts.netloc + urlParts.path
    else:
        givenUrlParts = urlsplit(givenUrl)
        sanitizedUrl = 'http://' + givenUrlParts.netloc + givenUrlParts.path + urlParts.path

    return sanitizedUrl


def create_client(token):
    """
    Connect to Readability API
    (http://readability-python-library.readthedocs.org/en/latest/clients.html#readability.ReaderClient)
    """

    rdb_client = ReaderClient(CONSUMER_KEY, CONSUMER_SECRET, token[0], token[1])
    return rdb_client


def add_bookmark(rdb_client, url):
    """
    Add bookmark with given URL
    """

    add_response = rdb_client.add_bookmark(url)

    # debugging only:
    #pprint(add_response)

    # strip id out of url:
    location = add_response['location']
    bookmark_id = location[location.rfind('/')+1:]

    # print status
    # @todo make this print in color codes ? and a better error message
    print '--------->', add_response['status']

    return bookmark_id


def add_tag(rdb_client, bookmark_id, tag):
    """
    Add tag to new bookmark:
    """

    add_tags = rdb_client.add_tags_to_bookmark(bookmark_id, tag)


def send_to_readability(list, tag):
    """
    This function actually puts it together to send data to Readability
    """

    token = get_token()
    rdb_client = create_client(token)

    print 'Starting import process...'
    print 'Adding', len(list), 'pages...'

    for url in list:
        print '- Adding bookmark for:', url
        bookmark_id = add_bookmark(rdb_client, url)
        add_tag(rdb_client, bookmark_id, tag)

    print 'Done.'



#list = ['https://nose.readthedocs.org/en/latest/writing_tests.html#test-functions', 'http://learnpythonthehardway.org/book/ex40.html']

new_list = get_toc('http://openbook.galileocomputing.de/java7/')

# debug:
list = new_list[11:13]

send_to_readability(list, 'Book')


