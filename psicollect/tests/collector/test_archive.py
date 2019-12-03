import os
import shutil
import unittest

import pytest

from psicollect.collector.archive import Archive

SELF_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SELF_PATH, 'data')
INPUT_PATH = os.path.join(DATA_PATH, 'input')
ARCHIVE_FILE_PATHS = [os.path.join(INPUT_PATH, 'test_archive.tar'), os.path.join(INPUT_PATH, 'test_archive.zip')]
EXTRACTED_DIR_PATH = os.path.join(INPUT_PATH, 'test_archive')


class TestArchive(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.archive = Archive(archive_url='https://www.google.com/thispathdoesnotexist/test_archive.tar')
        cls.archive2 = Archive(archive_url='https://www.google.com/thispathdoesnotexist/test_archive.tar',
                               archive_date='20180919')

        if os.path.exists(EXTRACTED_DIR_PATH):
            shutil.rmtree(EXTRACTED_DIR_PATH)

    # Allow for capturing console output for comparison using pytest fixtures
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capfd):
        self.capfd = capfd

    def test_to_string(self):
        assert str(self.archive) == 'test_archive.tar'
        assert str(self.archive2) == '(20180919) test_archive.tar [Unknown]'

    def test_is_zip(self):
        assert not self.archive.is_zip()

    def test_is_tar(self):
        assert self.archive.is_tar()

    def test_verify_integrity(self):
        for archive_file_path in ARCHIVE_FILE_PATHS:
            assert self.archive.verify_integrity(archive_file_path)

    def test_extract_archive(self):

        for archive_file_path in ARCHIVE_FILE_PATHS:

            # Delete the previous archive's extracted contents to try the function again with a new archive
            if os.path.exists(EXTRACTED_DIR_PATH):
                shutil.rmtree(EXTRACTED_DIR_PATH)

            self.archive.extract_archive(archive_file_path)

            for file_name in ['C25870213', 'C25870216', 'C25870220']:
                for extension in ['.jpg', '.geom']:
                    file_path = os.path.join(EXTRACTED_DIR_PATH, file_name + extension)
                    assert os.path.exists(file_path) and os.path.isfile(file_path)

        self.archive.extract_archive(ARCHIVE_FILE_PATHS[0])

        out, err = self.capfd.readouterr()
        assert str(out).count('Skipping ') == 6

    @classmethod
    def tearDownClass(cls) -> None:

        if os.path.exists(EXTRACTED_DIR_PATH):
            shutil.rmtree(EXTRACTED_DIR_PATH)
