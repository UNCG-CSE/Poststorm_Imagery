import os
import unittest
import pytest

from psic.resizer.generate import ResizeImages

SELF_PATH = os.path.dirname(os.path.abspath(__file__))


class TestResizeImages(unittest.TestCase):

    # Allow for capturing console output for comparison using pytest fixtures
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capfd):
        self.capfd = capfd

    def test_resize_all_images_debug(self):

        expected_size: tuple = (1081, 811)

        images = ResizeImages.resize_all_images(path=os.path.join(SELF_PATH, 'input'),
                                                output_path=os.path.join(SELF_PATH, 'output'),
                                                scale=0.15,
                                                save=True,
                                                debug=True)

        for image in images:
            assert image.size == expected_size

        out, err = self.capfd.readouterr()
        print('OUTPUT: ' + out)
        assert 'Searching through' in str(out)
        assert 'input for the pattern' in str(out)
        assert 'Resizing file 1 of 2 (50.00%): C26347592.jpg' in str(out)
        assert 'Resizing file 2 of 2 (100.00%): C26347598.jpg' in str(out)
