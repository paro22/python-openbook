from openbook import readability_client
import unittest


class TestReadabilityClient(unittest.TestCase):

    def setUp(self):
        url_list = ['http://openbook.galileocomputing.de/java7/1507_01_001.html#dodtp72eab4f3-0cfe-4098-8ac4-6af7e550501f',
                    'http://openbook.galileocomputing.de/java7/1507_03_009.html#dodtpbd929b12-ddef-4cab-b2b6-e3a94fdf4247']
        tag_name = 'Test'
        self.client = readability_client.ReadabilityClient(url_list, tag_name)

    def test_get_token(self):
        # TODO better way to test this?
        self.assertTrue(len(self.client.token) == 2)

    def test_create_client(self):
        # TODO improve this
        self.assertTrue(self.client.rdb_client)