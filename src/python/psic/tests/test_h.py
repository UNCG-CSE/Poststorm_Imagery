import os
from unittest import TestCase

from psic import h, s

SELF_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SELF_PATH, 'data')
INPUT_PATH = os.path.join(DATA_PATH, 'input')
TEST_FILE_PATH = os.path.join(INPUT_PATH, 'test_lock_me.txt')
NO_USER_FILE_PATH = os.path.join(INPUT_PATH, 'no_user_lock_file.txt')
TEST_LOCK_PATH = TEST_FILE_PATH + s.LOCK_SUFFIX


class TestHelper(TestCase):

    def test_to_readable_bytes(self):
        self.assertIn('???', h.to_readable_bytes('taco'))
        self.assertIn('???', h.to_readable_bytes(None))
        self.assertIn('KiB', h.to_readable_bytes(1))
        self.assertIn('KiB', h.to_readable_bytes(1024 ** 1 + 1))
        self.assertIn('MiB', h.to_readable_bytes(1024 ** 2 + 1))
        self.assertIn('GiB', h.to_readable_bytes(1024 ** 3 + 1))

    def test_1_get_lock_info_none(self):

        info: dict = h.get_lock_info(TEST_FILE_PATH)

        assert info['user'] is None
        assert info[s.LOCK_PART_SIZE_BYTES_FIELD] is None
        assert info[s.LOCK_TOTAL_SIZE_BYTES_FIELD] is None

    def test_2_update_file_lock_new_lock(self):

        test_file_path = os.path.join(INPUT_PATH, 'test_lock_me.txt')
        test_lock_path = test_file_path + s.LOCK_SUFFIX

        if os.path.exists(test_lock_path) and os.path.isfile(test_lock_path):
            os.remove(test_lock_path)

        lock = h.update_file_lock(base_file=test_file_path, user='test_dummy',
                                  total_size_byte=100, part_size_byte=50)

        assert lock  # Make sure it exists

        with open(test_lock_path, 'r') as f:
            lines = f.readlines()

        # Remove special characters like new-line chars
        line = [line.strip() for line in lines]

        for x in {'user = test_dummy', 'size_bytes = 50', 'total_size_bytes = 100'}:
            assert x in line

    def test_3_update_and_get_lock_info_existing(self):

        h.update_file_lock(base_file=TEST_FILE_PATH, user='test_dummy',
                           total_size_byte=100, part_size_byte=50)

        info: dict = h.get_lock_info(TEST_FILE_PATH)

        assert info['user'] == 'test_dummy'
        assert info[s.LOCK_PART_SIZE_BYTES_FIELD] == 50
        assert info[s.LOCK_TOTAL_SIZE_BYTES_FIELD] == 100

    def test_4_is_locked_by_another_user(self):
        assert h.is_locked_by_another_user('a_non_existent_file', this_user='not_test_dummy') is False
        assert h.is_locked_by_another_user(TEST_FILE_PATH, this_user='not_test_dummy')
        assert h.is_locked_by_another_user(TEST_FILE_PATH, this_user='test_dummy') is False

    def test_is_locked_by_another_user_no_user_found(self):
        assert h.is_locked_by_another_user(NO_USER_FILE_PATH, this_user='test_dummy') is False

    @classmethod
    def tearDownClass(cls) -> None:

        if os.path.exists(TEST_LOCK_PATH) and os.path.isfile(TEST_LOCK_PATH):
            os.remove(TEST_LOCK_PATH)
