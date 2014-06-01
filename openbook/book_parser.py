"""
PARSER
--------------------
Class responsible for parsing the desired site
"""

from bs4 import BeautifulSoup
import requests
from urlparse import urlsplit
import utilities


class BookParser(object):

    def __init__(self, url, css_class, tag_name):
        self.url = url
        self.css_class = utilities.class_or_id(css_class)
        self.tag_name = tag_name
        self.soup = self.get_soup()

    def get_soup(self):
        """
        Retrieve HTML soup from given URL
        """

        r = requests.get(self.url)
        data = r.text
        soup = BeautifulSoup(data)
        return soup

    def get_links(self):
        """
        Get 'table of contents page' and retrieve list of pages to send to Readability.com
        """

        url_list = []
        divs = self.soup.find_all(class_=self.css_class, limit=1)
        for div in divs:
            for link in div.find_all('a'):
                href = str(link.get('href'))

                # ignore empty links, anchors, and mailto:
                if href != '' and href[0] != '#' and 'None' not in href and 'mailto:' not in href:
                    href = self.sanitize_url(link.get('href'))
                    url_list.append(href)

        print 'Found %s links (Selector: %s).' % (len(url_list), self.css_class)

        without_duplicates = utilities.remove_duplicate_urls(url_list)
        print 'Removing duplicates, the list was reduced to %s links.' % len(without_duplicates)
        return without_duplicates

    def sanitize_url(self, current_url):
        """
        Here we have to account for internal links, so if there's no netloc,
        prepend the current (given) URL

        SplitResult(scheme='http', netloc='', path=u'abc.html', query='', fragment=u'')
        """

        # TODO extend this to https and make it more error tolerant
        # absolute urls, starting with / should be handled too

        current_url_parts = urlsplit(current_url)
        if 'http' in current_url:
            sanitized_url = 'http://' + current_url_parts.netloc + current_url_parts.path
        else:
            url_parts = urlsplit(self.url)
            sanitized_url = 'http://' + url_parts.netloc + url_parts.path + current_url_parts.path

        return sanitized_url

    def get_tag_name(self):
        """
        If a name was specified in the command line options, use it as the tag name
        for Readability. Otherwise, default back to the html <title> of the defined page
        """

        if self.tag_name == "":
            return str(self.soup.head.title.contents[0])
        else:
            return self.tag_name


