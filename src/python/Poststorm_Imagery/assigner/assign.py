import argparse
import os
import jsonpickle
from typing import Union, Set

from Poststorm_Imagery.assigner.image_assigner import ImageAssigner
from src.python.Poststorm_Imagery import s

ASSIGNER_FILE_NAME: str = 'assigner_state.json'

DATA_PATH: Union[bytes, str] = os.path.abspath(s.DATA_PATH)
TAR_CACHE_PATH: Union[bytes, str] = os.path.join(DATA_PATH, s.TAR_CACHE)

SMALL_PATH: Union[bytes, str] = os.path.abspath(s.SMALL_PATH)
SMALL_TAR_CACHE_PATH: Union[bytes, str] = os.path.join(SMALL_PATH, s.TAR_CACHE)

################################################
# Define command-line parameters and arguments #
################################################

# Define a set of arguments that should always be included in all commands and sub-commands of the assign.py command
parent = argparse.ArgumentParser(description='The default arguments for all commands and sub-commands')

parent.add_argument('--path', '-p', default=TAR_CACHE_PATH,
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parent.add_argument('--small_path', '-s', default=SMALL_TAR_CACHE_PATH,
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parent.add_argument('--debug', '-d', action='store_true', default=s.DEFAULT_DEBUG,
                    help='If included, the program will print info throughout the process (Default: %(default)s).')

parent.add_argument('--verbosity', '-v', type=int, default=s.DEFAULT_VERBOSITY,
                    help='Changes the log / debug message verbosity. Not all functions may be affected by this '
                         'value! Possible values are ... '
                         '0 = only errors, '
                         '1 = low, '
                         '2 = medium, '
                         '3 = high '
                         '(Default: %(default)s).')

# Define the root command
p = argparse.ArgumentParser(prog='assign', parents=[parent], add_help=False)
p_subparsers = p.add_subparsers(title='operations')


# Define the command to get the current image for a specific user (-u <user>)
p_current = p_subparsers.add_parser(name='current', help='The current image return help', parents=[parent], add_help=False)

p_current.add_argument('--user', '-u', type=str,
                       help='The user to get the current image of.')


# Define the command to modify tags of the user's (-u <user>) current image in the context of that user
p_tag = p_subparsers.add_parser(name='tag', help='The tagging sub-command help', parents=[parent], add_help=False)
p_tag_subparsers = p_tag.add_subparsers()


# Define the sub-command for adding tags to an image
p_tag_add = p_tag_subparsers.add_parser(name='add', parents=[parent], add_help=False)

p_tag_add.add_argument('--user', '-u', type=str,
                       help='The user that the command will be run in the context of.')

p_tag_add.add_argument('--tag', '-t', type=str,
                       help='The tag to add to the user\'s current image.')

p_tag_add.add_argument('--content', '-c', type=str,
                       help='The content of the tag to add to the user\'s current image.')


# Define the sub-command for removing tags from an image
p_tag_remove = p_tag_subparsers.add_parser(name='remove', parents=[parent], add_help=False)

p_tag_remove.add_argument('--user', '-u', type=str,
                          help='The user that the command will be run in the context of.')

p_tag_remove.add_argument('--tag', '-t', type=str,
                          help='The tag to add to the user\'s current image.')


# Define the sub-command for skipping an image and moving onto the next image
p_tag_skip = p_tag_subparsers.add_parser(name='skip', parents=[parent], add_help=False)

p_tag_skip.add_argument('--user', '-u', type=str,
                        help='The user that the command will be run in the context of.')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = p.parse_args()

if OPTIONS.debug:
    print(OPTIONS)

assigner_cache = os.path.join(OPTIONS.path, ASSIGNER_FILE_NAME)

assigner: ImageAssigner

if os.path.exists(assigner_cache) is False:
    if OPTIONS.debug:
        print('Creating new assigner object at ' + OPTIONS.path + ' ... ')
    assigner = ImageAssigner(scope_path=OPTIONS.path,
                             small_path=OPTIONS.small_path,
                             debug=OPTIONS.debug,
                             verbosity=OPTIONS.verbosity)

    cache_data = jsonpickle.encode(assigner.save())
    with open(assigner_cache, 'w') as f:
        f.write(cache_data)

with open(assigner_cache, 'r') as f:
    assigner = jsonpickle.decode(f.read()).load()
    if OPTIONS.debug:
        print('Using assigner object at ' + OPTIONS.path + ' ... ')

    # Modification of object here

cache_data = jsonpickle.encode(assigner.save())
with open(assigner_cache, 'w') as f:
    f.write(cache_data)
