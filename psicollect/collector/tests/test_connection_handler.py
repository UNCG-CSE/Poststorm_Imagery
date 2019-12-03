import os
from typing import List
from unittest import TestCase

from psicollect.collector.connection_handler import ConnectionHandler
from psicollect.collector.storm import Storm

SELF_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SELF_PATH, 'data')
INPUT_PATH = os.path.join(DATA_PATH, 'input')
TEST_FILE_PATH = os.path.join(INPUT_PATH, 'Storms_List_Page.html')


class TestConnectionHandler(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print(SELF_PATH)
        f = open(TEST_FILE_PATH, 'r')
        cls.c = ConnectionHandler(html_text=f.read())
        f.close()

    def test_generate_storm_list_all(self):

        # Parse all 34 storms
        self.assertEqual(len(self.c.generate_storm_list()), 34)

    def test_generate_storm_list_search_year(self):

        # Parse all 2008 storms (2)
        self.assertEqual(len(self.c.generate_storm_list(search_re='2008')), 2)

    def test_generate_storm_list_search_name_term(self):

        # Parse all hurricanes (25)
        self.assertEqual(len(self.c.generate_storm_list(search_re='hurricane')), 25)

    def test_generate_storm_list_search_none(self):

        # Test when there are no matches
        self.assertEqual(len(self.c.generate_storm_list(search_re='no storms will match this')), 0)

    def test_get_storm_list(self):

        # Ensure it actually gets the storm list
        self.assertEqual(self.c.generate_storm_list(), self.c.get_storm_list())

        # Ensure that changing the pattern reloads the cache
        storms_all: List[Storm] = self.c.get_storm_list()
        storms_2019: List[Storm] = self.c.get_storm_list(search_re='2019')
        self.assertNotEqual(storms_all, storms_2019)
