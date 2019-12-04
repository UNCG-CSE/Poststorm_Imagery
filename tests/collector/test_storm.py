from unittest import TestCase

from psicollect.collector.storm import Storm
from psicollect.common import s


class TestStorm(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.storm = Storm(s.URL_STORMS + "michael/index.html", "michael", "Hurricane Michael", 2018)

    def test_valid_string(self):
        self.assertIn("Hurricane Michael", str(self.storm))
        self.assertIn("(2018)", str(self.storm))

    def test_generate_archive_list_full(self):
        self.storm.generate_archive_list()
        self.assertGreaterEqual(len(self.storm.archive_list), 10)
        self.assertEqual(str(self.storm.archive_list_last_pattern), '.*')

    def test_generate_archive_list_rgb(self):
        self.storm.generate_archive_list(search_re="RGB")
        self.assertGreaterEqual(len(self.storm.archive_list), 5)
        self.assertEqual(str(self.storm.archive_list_last_pattern), 'RGB')
