import os
import shutil
import unittest

import pytest

from psic.collector.archive import Archive

SELF_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SELF_PATH, 'data')
INPUT_PATH = os.path.join(DATA_PATH, 'input')
ARCHIVE_FILE_PATH = os.path.join(INPUT_PATH, 'test_archive.tar')
EXTRACTED_DIR_PATH = os.path.join(INPUT_PATH, 'test_archive')


class TestTarRef(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.archive = Archive(archive_url='https://www.google.com/thispathdoesnotexist/test_archive.tar')
        cls.tar2 = Archive(archive_url='https://www.google.com/thispathdoesnotexist/test_archive.tar', archive_date='20180919')

        if os.path.exists(EXTRACTED_DIR_PATH):
            shutil.rmtree(EXTRACTED_DIR_PATH)

    # Allow for capturing console output for comparison using pytest fixtures
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capfd):
        self.capfd = capfd

    def test_to_string(self):
        assert str(self.archive) == 'test_archive.tar'
        assert str(self.archive2) == '(20180919) test_archive.tar [Unknown]'

    def test_verify_integrity(self):
        assert self.archive.verify_integrity(ARCHIVE_FILE_PATH)

    def test_1_extract_archive(self):

        self.archive.extract_archive(ARCHIVE_FILE_PATH)

        for file_name in ['C25870213', 'C25870216', 'C25870220']:
            for extension in ['.jpg', '.geom']:
                file_path = os.path.join(EXTRACTED_DIR_PATH, file_name + extension)
                assert os.path.exists(file_path) and os.path.isfile(file_path)

    def test_2_extract_archive_already_exists(self):

        self.archive.extract_archive(ARCHIVE_FILE_PATH)

        out, err = self.capfd.readouterr()
        assert str(out).count('Skipping ') == 6

    @classmethod
    def tearDownClass(cls) -> None:

        if os.path.exists(EXTRACTED_DIR_PATH):
            shutil.rmtree(EXTRACTED_DIR_PATH)
