from openbook import utilities
import unittest

class TestUtilities(unittest.TestCase):

    def test_remove_duplicate_urls(self):
        list_with_duplicates = ["a", "b", "a", "c", "b", "d", "a", "c", "b"]
        list_without_duplicates = utilities.remove_duplicate_urls(list_with_duplicates)
        self.assertEqual(list_without_duplicates, ["a", "b", "c", "d"])

    def test_class_or_id(self):

        # Class
        selector = ".test_class"
        selector_parsed = utilities.class_or_id(selector)
        self.assertEqual(selector_parsed[0], 'class')
        self.assertEqual(selector_parsed[1], 'test_class')

        # ID:
        selector = "#test_id"
        selector_parsed = utilities.class_or_id(selector)
        self.assertEqual(selector_parsed[0], 'id')
        self.assertEqual(selector_parsed[1], 'test_id')