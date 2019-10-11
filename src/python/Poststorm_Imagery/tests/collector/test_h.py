from unittest import TestCase

from src.python.Poststorm_Imagery import h


class TestHelper(TestCase):

    def test_to_readable_bytes(self):
        self.assertIn('KiB', h.to_readable_bytes(1))
        self.assertIn('KiB', h.to_readable_bytes(1024 ** 1 + 1))
        self.assertIn('MiB', h.to_readable_bytes(1024 ** 2 + 1))
        self.assertIn('GiB', h.to_readable_bytes(1024 ** 3 + 1))
