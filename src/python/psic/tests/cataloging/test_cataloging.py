import os
import shutil
from unittest import TestCase

import pytest

import s
from cataloging.generate import Cataloging

SELF_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SELF_PATH, 'data')
INPUT_PATH = os.path.join(DATA_PATH, 'input')
CATALOG_FILE = os.path.join(INPUT_PATH, Cataloging.CATALOG_FILE)
# EXPECTED_PATH = os.path.join(DATA_PATH, 'expected')
# OUTPUT_PATH = os.path.join(DATA_PATH, 'output')


class TestCataloging(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        if os.path.exists(CATALOG_FILE) and os.path.isfile(CATALOG_FILE):
            os.remove(CATALOG_FILE)

    # Allow for capturing console output for comparison using pytest fixtures
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capfd):
        self.capfd = capfd

    def test_generate_index_from_scope(self):

        Cataloging.generate_index_from_scope(scope_path=INPUT_PATH,
                                             file_extension='jpg',
                                             fields_needed=s.DEFAULT_FIELDS.copy(),
                                             debug=True,
                                             verbosity=3)
        out, err = self.capfd.readouterr()
        print('OUTPUT: ' + str(out).replace('\r', '\\r\n'))
        with self.subTest(msg='Found all 3 files'):
            assert 'C25870213.jpg ... matches pattern!' in str(out)
            assert 'C25870216.jpg ... does not have required .geom file!' in str(out)
            assert 'C25959144.jpg ... matches pattern!' in str(out)

        with self.subTest(msg='Calculated size of files'):
            assert 'Calculating sizes of files ... ' in str(out)

        with self.subTest(msg='Calculated modify times of files'):
            assert 'Calculating modify time of files ... ' in str(out)

        with self.subTest(msg='Saved to disk'):
            assert 'Saved catalog to disk! Basic data is complete! Moving on to .geom specific data ... ' in str(out)

        with self.subTest(msg='All three files processed'):
            assert 'Processing file 1 of 2 (0.00%)' in str(out)
            assert 'Processing file 2 of 2 (50.00%)' in str(out)

        with self.subTest(msg='All default tags were found in a .geom file'):
            assert str(out).count('Found 8 value(s)') == 2

        with self.subTest(msg='DataFrame is of right size'):
            assert '[2 rows x 11 columns]' in str(out)

        with self.subTest(msg='Catalog was saved to disk at the end'):
            assert str(out).count('Saved catalog to disk!') == 2

        # Run it again to check if it detects existing catalog
        Cataloging.generate_index_from_scope(scope_path=INPUT_PATH,
                                             file_extension='jpg',
                                             fields_needed=s.DEFAULT_FIELDS.copy(),
                                             save_interval=1,
                                             debug=True,
                                             verbosity=3)

    # def test__get_best_date(self):
    #     self.fail()
    #
    # def test__timestamp_to_utc(self):
    #     self.fail()
    #
    # def test__force_save_catalog(self):
    #     self.fail()
    #
    # def test__get_geom_fields(self):
    #     self.fail()

    @classmethod
    def tearDownClass(cls) -> None:

        if os.path.exists(CATALOG_FILE) and os.path.isfile(CATALOG_FILE):
            os.remove(CATALOG_FILE)
