#!/usr/bin/python

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
import optparse
from termcolor import colored


def get_token():
    """
    Returns an array with the user_key [0] and user_secret [1]
    """

    token = readability.xauth(CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD)
    return token


def get_soup(url):
    """
    Retrieve HTML soup from given URL
    """

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    return soup


def get_links(soup, url, cssClass):
    """
    Get 'table of contents page' and retrieve list of pages to send to Readability
    """

    url_list = []
    divs = soup.find_all(class_=cssClass, limit=1)
    for div in divs:
        for link in div.find_all('a'):
            href = str(link.get('href'))

            if href != '' and href[0] != '#' and 'None' not in href and 'mailto:' not in href:
                href = sanitize_url(link.get('href'), url)
                url_list.append(href)

    print 'Found', len(url_list), 'links in container', cssClass
    return remove_duplicate_urls(url_list)


def get_tag_name(soup, name):
    """
    If a name was specified in the command line options, use it as the tag name
    for Readability. Otherwise, default back to the html <title> of the defined page
    """

    if name == "":
        return str(soup.head.title.contents[0])
    else:
        return name


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

    print 'Removing duplicates, the list was reduced to', len(result), 'links.'
    return result


def sanitize_url(url, givenUrl):
    """
    Here we have to account for internal links, so if there's no netloc,
    prepend the current (given) URL

    SplitResult(scheme='http', netloc='', path=u'abc.html', query='', fragment=u'')
    """

    # @todo extend this to https and make it more error tolerant
    # absolute urls, starting with / should be handled too

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
    get_status_message(add_response['status'])

    return bookmark_id


def get_status_message(code):
    """
    Turns a status code into a colored message (tbd)
    """

    # @todo make this print better error messages
    if int(code) not in [202, 409]:
        print colored(code, 'red')
    else:
        print colored(code, 'green')


def add_tag(rdb_client, bookmark_id, tag):
    """
    Add tag to new bookmark:
    """

    add_tags = rdb_client.add_tags_to_bookmark(bookmark_id, tag)


def class_or_id(param):
    """
    Ideally this will differentiate between classes and ids,
    maybe in the way jQuery does (#id, .class)
    """

    # @todo differentiate between IDs and classes
    if param[0] == ".":
        return param[1:]


def send_to_readability(url_list, tag):
    """
    This function actually puts it together to send data to Readability
    """

    token = get_token()
    rdb_client = create_client(token)

    print 'Starting import process...'
    print 'Adding', len(url_list), 'pages...'

    for url in url_list:
        print '- Adding bookmark for:', url
        bookmark_id = add_bookmark(rdb_client, url)
        add_tag(rdb_client, bookmark_id, tag)

    print 'Done.'


def get_options():
    """
    Define and retrieve options from the command line
    """

    parser = optparse.OptionParser()
    parser.add_option('-u', help='URL with table of contents to parse (required)', dest='url', action='store_true')
    parser.add_option('-c', help='CSS Class or ID to parse, eg. main-content (required)', dest='css_class', action='store_true')
    parser.add_option('-t', help='Tag name in Readability. Defaults to <title> of site given in option -u if empty.', dest='tag', action='store_true')
    (opts, args) = parser.parse_args()

    # Making sure all mandatory options are set:
    mandatories = ['url', 'css_class']
    for m in mandatories:
        if not opts.__dict__[m]:
            print "Mandatory options is missing!\n"
            parser.print_help()
            exit(-1)

    return (opts, args)


def main():
    """
    main function that starts everything else
    """

    # get options:
    (opts, args) = get_options()
    url = str(args[0]) if opts.url else ""
    css_class = str(args[1]) if opts.css_class else ""
    tag = str(args[2]) if opts.tag else ""

    # then start doing stuff:
    soup = get_soup(url)
    url_list = get_links(soup, url, class_or_id(css_class))
    tag_name = get_tag_name(soup, tag)

    # debug:
    #url_list = url_list[:10]

    send_to_readability(url_list, tag_name)


if __name__ == "__main__":
    main()