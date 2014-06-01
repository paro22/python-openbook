"""
READABILITY CLIENT
--------------------
Class responsible for sending data to readability.com
"""

import readability
from readability import ReaderClient
from settings import \
       CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD
from termcolor import colored


class ReadabilityClient():

    def __init__(self, url_list, tag):
        self.token = self.get_token()
        self.rdb_client = self.create_client()
        self.url_list = url_list
        self.tag = tag

    def get_token(self):
        """
        Returns an array with the user_key [0] and user_secret [1]
        """

        token = readability.xauth(CONSUMER_KEY, CONSUMER_SECRET, USERNAME, PASSWORD)
        return token

    def create_client(self):
        """
        Connect to Readability API
        (http://readability-python-library.readthedocs.org/en/latest/clients.html#readability.ReaderClient)
        """

        rdb_client = ReaderClient(CONSUMER_KEY, CONSUMER_SECRET, self.token[0], self.token[1])
        return rdb_client

    def add_bookmark(self, url):
        """
        Add bookmark with given URL
        """

        add_response = self.rdb_client.add_bookmark(url)

        # debugging only:
        #pprint(add_response)

        return add_response

    def get_status_message(self, response):
        """
        Turns a status code into a colored message (tbd)
        """

        code = response['status']
        # @todo make this print better error messages
        if int(code) not in [202, 409]:
            return colored(code, 'red')
        else:
            return colored(code, 'green')

    def add_tag(self, bookmark_id, tag):
        """
        Add tag to new bookmark:
        """

        self.rdb_client.add_tags_to_bookmark(bookmark_id, tag)

    def send_to_readability(self):
        """
        This function actually puts it together to send data to Readability
        """

        print 'Starting import process...'
        print 'Adding %s pages...' % len(self.url_list)

        for url in self.url_list:
            add_response = self.add_bookmark(url)

            # strip id out of url:
            location = add_response['location']
            bookmark_id = location[location.rfind('/')+1:]

            print '- Adding bookmark for %s. Status: %s' % (url, self.get_status_message(add_response))

            # then add tag:
            self.add_tag(bookmark_id, self.tag)

        print 'Done.'