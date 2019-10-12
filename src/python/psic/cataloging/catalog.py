import argparse
import os
from typing import Union, Set

from psic import s
from psic.cataloging import generate

DATA_PATH: Union[bytes, str] = os.path.abspath(s.DATA_PATH)
TAR_CACHE_PATH: Union[bytes, str] = os.path.join(DATA_PATH, s.TAR_CACHE)

################################################
# Define command-line parameters and arguments #
################################################

parser = argparse.ArgumentParser(prog='catalog')

parser.add_argument('--path', '-p', default=TAR_CACHE_PATH,
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parser.add_argument('--extension', '-e', default='jpg',
                    help='The file extension to restrict the search to (Default: %(default)s).')

parser.add_argument('--fields', '-f', type=Set, default=s.DEFAULT_FIELDS.copy(),
                    help='The various fields listed within a python set to grab from the .geom file as well as '
                         'optional fields "size" and "date" for the size of the image and the date taken respectively '
                         '(Default: %(default)s).')

parser.add_argument('--debug', '-d', action='store_true', default=s.DEFAULT_DEBUG,
                    help='If included, the program will print info throughout the process (Default: %(default)s).')

parser.add_argument('--verbosity', '-v', type=int, default=s.DEFAULT_VERBOSITY,
                    help='Changes the log / debug message verbosity. Not all functions may be affected by this '
                         'value! Possible values are ... '
                         '0 = only errors, '
                         '1 = low, '
                         '2 = medium, '
                         '3 = high '
                         '(Default: %(default)s).')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = parser.parse_args()

generate.generate_index_from_scope(scope_path=OPTIONS.path,
                                   file_extension=OPTIONS.extension,
                                   fields_needed=OPTIONS.fields,
                                   debug=OPTIONS.debug,
                                   verbosity=OPTIONS.verbosity)
