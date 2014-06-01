from openbook import book_parser
import unittest


class TestBookParser(unittest.TestCase):

    def setUp(self):
        self.book_parser = book_parser.BookParser('http://openbook.galileocomputing.de/java7/', '.main', 'Test')

    def test_get_tag_name(self):
        tag_name = self.book_parser.get_tag_name()
        self.assertEqual(tag_name, 'Test')

    def test_sanitize_url(self):

        # test with http in front
        current_url = 'http://openbook.galileocomputing.de/java7/1507_01_001.html#dodtp72eab4f3-0cfe-4098-8ac4-6af7e550501f'
        sanitized_url = self.book_parser.sanitize_url(current_url)
        self.assertEqual(sanitized_url, 'http://openbook.galileocomputing.de/java7/1507_01_001.html')

        # test without http
        current_url2 = '1507_01_001.html#dodtp72eab4f3-0cfe-4098-8ac4-6af7e550501f'
        sanitized_url2 = self.book_parser.sanitize_url(current_url2)
        self.assertEqual(sanitized_url2, 'http://openbook.galileocomputing.de/java7/1507_01_001.html')