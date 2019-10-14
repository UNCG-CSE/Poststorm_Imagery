import os
import shutil
import unittest

import pytest

from psic.collector.tar_ref import TarRef

SELF_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SELF_PATH, 'data')
INPUT_PATH = os.path.join(DATA_PATH, 'input')
TAR_FILE_PATH = os.path.join(INPUT_PATH, 'test_archive.tar')
EXTRACTED_DIR_PATH = os.path.join(INPUT_PATH, 'test_archive')


class TestTarRef(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.tar = TarRef(tar_url='https://www.google.com/thispathdoesnotexist/test_archive.tar')
        cls.tar2 = TarRef(tar_url='https://www.google.com/thispathdoesnotexist/test_archive.tar', tar_date='20180919')

        if os.path.exists(EXTRACTED_DIR_PATH):
            shutil.rmtree(EXTRACTED_DIR_PATH)

    # Allow for capturing console output for comparison using pytest fixtures
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capfd):
        self.capfd = capfd

    def test_to_string(self):
        assert str(self.tar) == 'test_archive.tar'
        assert str(self.tar2) == '(20180919) test_archive.tar [Unknown]'

    def test_verify_integrity(self):
        assert self.tar.verify_integrity(TAR_FILE_PATH)

    def test_1_extract_archive(self):

        self.tar.extract_archive(TAR_FILE_PATH)

        for file_name in ['C25870213', 'C25870216', 'C25870220']:
            for extension in ['.jpg', '.geom']:
                file_path = os.path.join(EXTRACTED_DIR_PATH, file_name + extension)
                assert os.path.exists(file_path) and os.path.isfile(file_path)

    def test_2_extract_archive_already_exists(self):

        self.tar.extract_archive(TAR_FILE_PATH)

        out, err = self.capfd.readouterr()
        assert str(out).count('Skipping ') == 6

    @classmethod
    def tearDownClass(cls) -> None:

        if os.path.exists(EXTRACTED_DIR_PATH):
            shutil.rmtree(EXTRACTED_DIR_PATH)
