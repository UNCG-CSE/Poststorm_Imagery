#!/usr/bin/env python3

import getpass
import sys
from os import path

import jsonpickle

from psic.assigner.batch import Batch
from psic.assigner.image_assigner import ImageAssigner, CatalogNotFoundException
from psic.assigner.json_response import JSONResponse

# Get the username of the current user to prevent conflicts of multiple users testing same filesystem
curr_user = getpass.getuser()
ASSIGNER_FILE_NAME: str = 'assigner_state-' + curr_user + '.json'

assigner: ImageAssigner
flag_pickle_changed: bool = False

# Get everything after the command path as a pickle-able JSON object
json_obj: Batch = jsonpickle.decode(sys.argv[1:])

assigner_cache = path.join(json_obj.path, ASSIGNER_FILE_NAME)

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


with open(assigner_cache, 'r') as f:
    assigner = jsonpickle.decode(f.read())

    for op in json_obj.operations:

        try:
            if json_obj.debug:
                print('Using assigner object at ' + json_obj.path + ' ... ')

            # Modifying the tags of a user's current image
            if op['command'] == 'tag':
                if op['tag_operation'] == 'add':
                    assigner.get_current_image(user_id=json_obj.user_id)\
                        .add_tag(user_id=json_obj.user_id, tag=op['tag'], content=op['content'])
                    flag_pickle_changed = True
                    print(JSONResponse(status=0, content=assigner.get_current_image(user_id=json_obj.user_id,
                                                                                    expanded=True)).json())
                elif op['tag_operation'] == 'add_notes':
                    assigner.get_current_image(user_id=json_obj.user_id)\
                        .add_tag(user_id=json_obj.user_id, tag='notes', content=op['content'])
                    flag_pickle_changed = True
                    print(JSONResponse(status=0, content=assigner.get_current_image(user_id=json_obj.user_id,
                                                                                    expanded=True)).json())
                elif op['tag_operation'] == 'remove':
                    assigner.get_current_image(user_id=json_obj.user_id)\
                        .remove_tag(user_id=json_obj.user_id, tag=op['tag'])
                    flag_pickle_changed = True
                    print(JSONResponse(status=0, content=assigner.get_current_image(user_id=json_obj.user_id,
                                                                                    expanded=True)).json())
                elif op['tag_operation'] == 'next':
                    print(JSONResponse(status=0, content=assigner.get_next_image(user_id=json_obj.user_id,
                                                                                 expanded=True)).json())
                    flag_pickle_changed = True
                elif op['tag_operation'] == 'skip':
                    print(JSONResponse(status=0, content=assigner.get_next_image(user_id=json_obj.user_id,
                                                                                 skip=True,
                                                                                 expanded=True)).json())
                    flag_pickle_changed = True
                else:
                    print(JSONResponse(status=1, error_message='This tagging operation is not implemented yet!').json())

            # Get the user's current image
            elif op['command'] == 'current':
                print(JSONResponse(status=0, content=assigner.get_current_image(user_id=json_obj.user_id,
                                                                                expanded=True)).json())

        except CatalogNotFoundException as e:
            print(JSONResponse(status=1, error_message=str(e) + ' Try double-checking the path passed: ' + json_obj.path).json())
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
