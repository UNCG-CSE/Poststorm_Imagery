import os
from unittest import TestCase

from src.python.Poststorm_Imagery.collector import s
from src.python.Poststorm_Imagery.collector.storm import Storm


class TestStorm(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.storm = Storm(os.path.join(s.URL_STORMS, "michael"), "michael", "Hurricane Michael", 2018)

    def test_valid_string(self):
        self.assertIn("Hurricane Michael", str(self.storm))
        self.assertIn("(2018)", str(self.storm))
