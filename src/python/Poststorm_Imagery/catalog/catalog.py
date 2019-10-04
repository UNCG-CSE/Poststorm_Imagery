import argparse
import os
from typing import Union

from src.python.Poststorm_Imagery.collector import s
from src.python.Poststorm_Imagery.catalog import generate

DATA_PATH: Union[bytes, str] = os.path.abspath(s.DATA_PATH)
TAR_CACHE_PATH: Union[bytes, str] = os.path.join(DATA_PATH, s.TAR_CACHE)

################################################
# Define command-line parameters and arguments #
################################################

parser = argparse.ArgumentParser(prog='catalog')

parser.add_argument('--path', '-p', default=TAR_CACHE_PATH,
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parser.add_argument('--extension', '-e', default=None,
                    help='The file extension to restrict the search to.')

parser.add_argument('--debug', '-d', action='store_true',
                    help='If included, the program will print info throughout the process (Default: %(default)s).')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = parser.parse_args()

generate.generate_index_from_scope(debug=OPTIONS.debug, scope_path=OPTIONS.path, file_extension=OPTIONS.extension)
