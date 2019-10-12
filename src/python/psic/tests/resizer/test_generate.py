"""
from os import path
from unittest import TestCase

from psic.resizer.generate import resize_image


class TestGenerate(TestCase):
    def test_output(self):
        resize_image(path=path.abspath('./resizer/input'),
                     output_path=path.abspath('./resizer/output'),
                     scale=0.15,
                     debug=True)
        self.assertEqual(True, False)
"""