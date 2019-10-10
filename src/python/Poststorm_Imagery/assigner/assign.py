import argparse
import os
import jsonpickle
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

p = argparse.ArgumentParser(prog='assign')

p.add_argument('--path', '-p', default=TAR_CACHE_PATH,
               help='The path on your system to set the scope of file search to (Default: %(default)s).')

p.add_argument('--small_path', '-s', default=SMALL_TAR_CACHE_PATH,
               help='The path on your system to set the scope of file search to (Default: %(default)s).')

p.add_argument('--debug', '-d', action='store_true', default=s.DEFAULT_DEBUG,
               help='If included, the program will print info throughout the process (Default: %(default)s).')

p.add_argument('--verbosity', '-v', type=int, default=s.DEFAULT_VERBOSITY,
               help='Changes the log / debug message verbosity. Not all functions may be affected by this '
                         'value! Possible values are ... '
                         '0 = only errors, '
                         '1 = low, '
                         '2 = medium, '
                         '3 = high '
                         '(Default: %(default)s).')

subparsers = p.add_subparsers()

pt = subparsers.add_parser(name='tag', help='tagging help')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = p.parse_args()

assigner_cache = os.path.join(OPTIONS.path, ASSIGNER_FILE_NAME)

assigner: ImageAssigner

if os.path.exists(assigner_cache) is False:
    if OPTIONS.debug:
        print('Creating new assigner object at ' + OPTIONS.path + ' ... ')
    assigner = ImageAssigner(scope_path=OPTIONS.path,
                             small_path=OPTIONS.small_path,
                             debug=OPTIONS.debug,
                             verbosity=OPTIONS.verbosity)

    cache_data = jsonpickle.encode(assigner)
    with open(assigner_cache, 'w') as f:
        f.write(cache_data)

with open(assigner_cache, 'r') as f:
    assigner = jsonpickle.decode(f.read())
    if OPTIONS.debug:
        print('Using assigner object at ' + OPTIONS.path + ' ... ')

# Modification of object here

cache_data = jsonpickle.encode(assigner)
with open(assigner_cache, 'w') as f:
    f.write(cache_data)
