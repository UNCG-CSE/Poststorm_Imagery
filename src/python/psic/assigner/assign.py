#!/usr/bin/env python3

import argparse
from os import path
from typing import Union

import jsonpickle

from psic import s
from psic.assigner.image_assigner import ImageAssigner, CatalogNotFoundException
from psic.assigner.json_response import JSONResponse

ASSIGNER_FILE_NAME: str = 'assigner_state.json'

DATA_PATH: Union[bytes, str] = path.abspath(s.DATA_PATH)
TAR_CACHE_PATH: Union[bytes, str] = path.join(DATA_PATH, s.TAR_CACHE)

SMALL_PATH: Union[bytes, str] = path.abspath(s.SMALL_PATH)
SMALL_TAR_CACHE_PATH: Union[bytes, str] = path.join(SMALL_PATH, s.TAR_CACHE)

################################################
# Define command-line parameters and arguments #
################################################

# Define a set of arguments that should always be included in all commands and sub-commands of the assign.py command
parent = argparse.ArgumentParser(add_help=False)

parent.add_argument('--path', '-p', default=TAR_CACHE_PATH, dest='path',
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parent.add_argument('--small_path', '-s', default=SMALL_TAR_CACHE_PATH, dest='small_path',
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parent.add_argument('--response', '-r', choices=['json'], default='json', dest='format',
                    help='The format of the response to return results as (Default: %(default)s).')

parent.add_argument('--debug', '-d', action='store_true', default=s.DEFAULT_DEBUG, dest='debug',
                    help='If included, the program will print info throughout the process (Default: %(default)s).')

parent.add_argument('--verbosity', '-v', type=int, default=s.DEFAULT_VERBOSITY, dest='verbosity',
                    help='Changes the log / debug message verbosity. Not all functions may be affected by this '
                         'value! Possible values are ... '
                         '0 = only errors, '
                         '1 = low, '
                         '2 = medium, '
                         '3 = high '
                         '(Default: %(default)s).')

# Define the user parameter for specific functions that use it (i.e. tag's sub-commands and current
user = argparse.ArgumentParser(add_help=False)

user.add_argument('--user', '-u', type=str, dest='user', required=True,
                  help='The user that the command will be run in the context of.')

# Define the root command
p = argparse.ArgumentParser(prog='assign', parents=[parent])
p_subparsers = p.add_subparsers(title='operations', dest='command')


# Define the command to get the current image for a specific user (-u <user>)
p_current = p_subparsers.add_parser(name='current', parents=[parent, user],
                                    help='The current image return help')


# Define the command to modify tags of the user's (-u <user>) current image in the context of that user
p_tag = p_subparsers.add_parser(name='tag', parents=[parent],
                                help='The tagging sub-command help')
p_tag_subparsers = p_tag.add_subparsers(title='tagging operations', dest='tag_operation')


# Define the sub-command for adding tags to an image
p_tag_add = p_tag_subparsers.add_parser(name='add', parents=[parent, user],)

p_tag_add.add_argument('--tag', '-t', type=str, dest='tag', required=True,
                       help='The tag to add to the user\'s current image.')

p_tag_add.add_argument('--content', '-c', dest='content', required=True,
                       help='The content of the tag to add to the user\'s current image.')


# Define the sub-command for removing tags from an image
p_tag_remove = p_tag_subparsers.add_parser(name='remove', parents=[parent, user])

p_tag_remove.add_argument('--tag', '-t', type=str, dest='tag', required=True,
                          help='The tag to add to the user\'s current image.')


# Define the sub-command for skipping an image and moving onto the next image
p_tag_next = p_tag_subparsers.add_parser(name='next', parents=[parent, user])


# Define the sub-command for skipping an image and moving onto the next image
p_tag_skip = p_tag_subparsers.add_parser(name='skip', parents=[parent, user])

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = p.parse_args()

if OPTIONS.debug:
    print(OPTIONS)

assigner: ImageAssigner
flag_pickle_changed: bool = False

assigner_cache = path.join(OPTIONS.path, ASSIGNER_FILE_NAME)

try:

    if path.exists(assigner_cache) is False:
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
        assigner = jsonpickle.decode(f.read())
        if OPTIONS.debug:
            print('Using assigner object at ' + OPTIONS.path + ' ... ')

        # Modifying the tags of a user's current image
        if OPTIONS.command == 'tag':
            if OPTIONS.tag_operation == 'add':
                assigner.get_current_image(user_id=OPTIONS.user)\
                    .add_tag(user_id=OPTIONS.user, tag=OPTIONS.tag, content=OPTIONS.content)
                flag_pickle_changed = True
                print(JSONResponse(status=0, content=assigner.get_current_image(user_id=OPTIONS.user,
                                                                                expanded=True)).json())
            elif OPTIONS.tag_operation == 'remove':
                assigner.get_current_image(user_id=OPTIONS.user)\
                    .remove_tag(user_id=OPTIONS.user, tag=OPTIONS.tag)
                flag_pickle_changed = True
                print(JSONResponse(status=0, content=assigner.get_current_image(user_id=OPTIONS.user,
                                                                                expanded=True)).json())
            elif OPTIONS.tag_operation == 'next':
                print(JSONResponse(status=0, content=assigner.get_next_image(user_id=OPTIONS.user,
                                                                             expanded=True)).json())
                flag_pickle_changed = True
            elif OPTIONS.tag_operation == 'skip':
                print(JSONResponse(status=0, content=assigner.get_next_image(user_id=OPTIONS.user,
                                                                             skip=True,
                                                                             expanded=True)).json())
                flag_pickle_changed = True
            else:
                print(JSONResponse(status=1, error_message='This tagging operation is not implemented yet!').json())

        # Get the user's current image
        elif OPTIONS.command == 'current':
            print(JSONResponse(status=0, content=assigner.get_current_image(user_id=OPTIONS.user,
                                                                            expanded=True)).json())

except CatalogNotFoundException as e:
    print(JSONResponse(status=1, error_message=str(e) + ' Try double-checking the path passed!').json())
except Exception as e:
    print(JSONResponse(status=1, error_message=str(e)).json())

try:
    if flag_pickle_changed:
        cache_data = jsonpickle.encode(assigner.save())
        with open(assigner_cache, 'w') as f:
            f.write(cache_data)
except Exception as e:
    print(JSONResponse(status=1, error_message=str(e)).json())
