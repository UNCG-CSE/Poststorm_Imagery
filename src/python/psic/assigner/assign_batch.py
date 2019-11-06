#!/usr/bin/env python3

import getpass
import sys
from os import path

import jsonpickle

from psic.assigner.batch import Batch
from psic.assigner.image_assigner import ImageAssigner, CatalogNotFoundException
from psic.assigner.image_ref import Image
from psic.assigner.json_response import JSONResponse

# Get the username of the current user to prevent conflicts of multiple users testing same filesystem
curr_user = getpass.getuser()
ASSIGNER_FILE_NAME: str = 'assigner_state-' + curr_user + '.json'

assigner: ImageAssigner
flag_pickle_changed: bool = False

# Get everything after the command path as a pickle-able JSON object
json_obj: Batch = jsonpickle.decode(' '.join(sys.argv[1:]))

assigner_cache = ASSIGNER_FILE_NAME

# Create a new assigner state if one doesn't exist
if path.exists(assigner_cache) is False:
    if json_obj.debug:
        print('Creating new assigner object at ' + json_obj.path + ' ... ')
    assigner = ImageAssigner(scope_path=json_obj.path,
                             small_path=json_obj.small_path,
                             debug=json_obj.debug)

    cache_data = jsonpickle.encode(assigner.save())
    with open(assigner_cache, 'w') as f:
        f.write(cache_data)

if json_obj.debug:
    print('Using assigner object at ' + json_obj.path + ' ... ')

with open(assigner_cache, 'r') as f:
    assigner = jsonpickle.decode(f.read())

    last_tagged_image: Image = assigner.get_current_image(user_id=json_obj.user_id, expanded=True)

    for op in json_obj.operations:

        try:

            # Modifying the tags of a user's current image
            if op['command'] == 'tag':
                if op['tag_operation'] == 'add':
                    assigner.get_current_image(user_id=json_obj.user_id) \
                        .add_tag(user_id=json_obj.user_id, tag=op['tag'], content=op['content'])
                    flag_pickle_changed = True
                    last_tagged_image = assigner.get_current_image(user_id=json_obj.user_id, expanded=True)
                elif op['tag_operation'] == 'add_notes':
                    assigner.get_current_image(user_id=json_obj.user_id) \
                        .add_tag(user_id=json_obj.user_id, tag='notes', content=op['content'])
                    flag_pickle_changed = True
                    last_tagged_image = assigner.get_current_image(user_id=json_obj.user_id, expanded=True)
                elif op['tag_operation'] == 'remove':
                    assigner.get_current_image(user_id=json_obj.user_id) \
                        .remove_tag(user_id=json_obj.user_id, tag=op['tag'])
                    flag_pickle_changed = True
                    last_tagged_image = assigner.get_current_image(user_id=json_obj.user_id, expanded=True)
                elif op['tag_operation'] == 'next':
                    assigner.get_next_image(user_id=json_obj.user_id)
                    flag_pickle_changed = True
                elif op['tag_operation'] == 'skip':
                    assigner.get_next_image(user_id=json_obj.user_id, skip=True)
                    flag_pickle_changed = True
                else:
                    print(JSONResponse(status=1, error_message='\'%s\' is not a valid tagging operation in {add, '
                                                               'add_notes, remove, next, skip}!'
                                                               % op['tag_operation']).json())
                    exit()

            # Get the user's current image
            elif op['command'] == 'current':
                last_tagged_image = assigner.get_current_image(user_id=json_obj.user_id, expanded=True)
            else:
                print(JSONResponse(status=1, error_message='\'%s\' is not a command in {tag, current}!'
                                                           % op['command']).json())
                exit()

        except CatalogNotFoundException as e:
            print(JSONResponse(status=1, error_message=str(e) + ' Try double-checking the path passed: ' +
                                                                json_obj.path).json())
            exit()
        except Exception as e:
            print(JSONResponse(status=1, error_message=str(e)).json())
            if json_obj.debug:
                raise e

try:
    if flag_pickle_changed:
        cache_data = jsonpickle.encode(assigner.save())
        with open(assigner_cache, 'w') as f:
            f.write(cache_data)
except Exception as e:
    print(JSONResponse(status=1, error_message=str(e)).json())
    exit()

# If all the operations were successful, return the final result (before skip / next)
print(JSONResponse(status=0, content=last_tagged_image).json())
