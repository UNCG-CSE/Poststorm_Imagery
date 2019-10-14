import os
import unittest
import pytest

from psic.resizer.generate import ResizeImages

SELF_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SELF_PATH, 'data')
INPUT_PATH = os.path.join(DATA_PATH, 'input')
EXPECTED_PATH = os.path.join(DATA_PATH, 'expected')
OUTPUT_PATH = os.path.join(DATA_PATH, 'output')


class TestResizeImages(unittest.TestCase):

    # Allow for capturing console output for comparison using pytest fixtures
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capfd):
        self.capfd = capfd

    def test_resize_all_images_debug(self):

        expected_size: tuple = (1081, 811)
        images = ResizeImages.resize_all_images(path=INPUT_PATH,
                                                output_path=OUTPUT_PATH,
                                                scale=0.15,
                                                save=True,
                                                debug=True)

        for image in images:
            assert image.size == expected_size

        out, err = self.capfd.readouterr()
        print('OUTPUT: ' + str(out).replace('\r', '\\r\n'))
        assert 'Searching through' in str(out)
        assert 'input for the pattern' in str(out)
        assert 'Resizing file 1 of 2 (50.00%): ' in str(out)
        assert 'Resizing file 2 of 2 (100.00%): ' in str(out)
