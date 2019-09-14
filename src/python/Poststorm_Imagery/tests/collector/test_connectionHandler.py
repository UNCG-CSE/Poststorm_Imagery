from unittest import TestCase

from src.python.Poststorm_Imagery.collector.ConnectionHandler import ConnectionHandler


class TestConnectionHandler(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.c = ConnectionHandler(html_text=open('resources/Storms_List_page.html', 'r').read())

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
        pass
        """
        storms: List[Storm] = c.get_storm_list(OPTIONS.storm)

        for storm in c.storms
        self.assertEqual(, 'unfilled')
        """
