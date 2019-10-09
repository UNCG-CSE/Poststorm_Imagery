import argparse
import os
import pickle
from typing import Union, Set

from Poststorm_Imagery.assigner.image_assigner import ImageAssigner
from src.python.Poststorm_Imagery import s

ASSIGNER_FILE_NAME: str = 'assigner_cache.bin'

DATA_PATH: Union[bytes, str] = os.path.abspath(s.DATA_PATH)
TAR_CACHE_PATH: Union[bytes, str] = os.path.join(DATA_PATH, s.TAR_CACHE)

SMALL_PATH: Union[bytes, str] = os.path.abspath(s.SMALL_PATH)
SMALL_TAR_CACHE_PATH: Union[bytes, str] = os.path.join(SMALL_PATH, s.TAR_CACHE)

################################################
# Define command-line parameters and arguments #
################################################

parser = argparse.ArgumentParser(prog='assign')

parser.add_argument('--path', '-p', default=TAR_CACHE_PATH,
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parser.add_argument('--small_path', '-s', default=SMALL_TAR_CACHE_PATH,
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parser.add_argument('--debug', '-d', action='store_true',
                    help='If included, the program will print info throughout the process (Default: %(default)s).')

parser.add_argument('--verbosity', '-v', type=int, default=1,
                    help='Changes the log / debug message verbosity. Not all functions may be affected by this '
                         'value! Possible values are ... '
                         '0 = only errors, '
                         '1 = low, '
                         '2 = medium, '
                         '3 = high '
                         '(Default: %(default)s).')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = parser.parse_args()

assigner_cache = os.path.join(OPTIONS.path, ASSIGNER_FILE_NAME)

assigner: ImageAssigner

if os.path.exists(assigner_cache):
    with open(assigner_cache, 'rb') as f:
        assigner = pickle.load(f)
        if OPTIONS.debug:
            print('Using existing assigner object at ' + OPTIONS.path + ' ... ')
else:
    if OPTIONS.debug:
        print('Creating new assigner object at ' + OPTIONS.path + ' ... ')
    assigner = ImageAssigner(scope_path=OPTIONS.path,
                             small_path=OPTIONS.small_path)

pickle.dump(assigner, open(assigner_cache, 'wb'), pickle.HIGHEST_PROTOCOL)
