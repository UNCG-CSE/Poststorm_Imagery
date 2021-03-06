#!/usr/bin/env python3

import getpass
import sys
from datetime import datetime
from os import path, mknod, remove, mkdir
from time import sleep

import jsonpickle

from psic import s
from psic.assigner.batch import Batch
from psic.assigner.image_assigner import ImageAssigner
from psic.assigner.image_ref import Image
from psic.assigner.json_response import JSONResponse
from psic.cataloging.make_catalog import CatalogNotFoundException

try:

    # Get the username of the current user to prevent conflicts of multiple users testing same filesystem
    curr_user = getpass.getuser()
    ASSIGNER_FILE_NAME: str = 'assigner_state-' + curr_user + '.json'

    BACKUP_FOLDER: str = './backup/'

    assigner: ImageAssigner
    flag_pickle_changed: bool = False

    # Get everything after the command path as a pickle-able JSON object
    json_obj: Batch = jsonpickle.decode(' '.join(sys.argv[1:]))

    assigner_cache = ASSIGNER_FILE_NAME

    while path.exists(ASSIGNER_FILE_NAME + '.lock'):
        sleep(0.25)

    mknod(ASSIGNER_FILE_NAME + '.lock')

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
            f.close()

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

                        # Register the elapsed time stat in the image for the user
                        assigner.get_current_image(user_id=json_obj.user_id) \
                            .set_stats_tag_elapsed_session(user_id=json_obj.user_id,
                                                           session_seconds=float(int(op['stats_time_elapsed_ms']) / 1000))

                        assigner.get_next_image(user_id=json_obj.user_id)
                        flag_pickle_changed = True
                    elif op['tag_operation'] == 'skip':

                        # Register the elapsed time stat in the image for the user
                        assigner.get_current_image(user_id=json_obj.user_id) \
                            .set_stats_tag_elapsed_session(user_id=json_obj.user_id,
                                                           session_seconds=float(int(op['stats_time_elapsed_ms']) / 1000))

                        assigner.get_next_image(user_id=json_obj.user_id, skip=True)
                        flag_pickle_changed = True
                    else:
                        print(JSONResponse(status=1, error_message='\'%s\' is not a valid tagging operation in {add, '
                                                                   'add_notes, remove, next, skip}!'
                                                                   % op['tag_operation']).json())
                        remove(ASSIGNER_FILE_NAME + '.lock')
                        exit()

                # Get the user's current image
                elif op['command'] == 'current':

                    # If the user is going to be assigned an image for the first time, flag changes ahead of time
                    if assigner.has_a_current_image(user_id=json_obj.user_id):
                        flag_pickle_changed = True

                    last_tagged_image = assigner.get_current_image(user_id=json_obj.user_id, expanded=True)
                else:
                    print(JSONResponse(status=1, error_message='\'%s\' is not a command in {tag, current}!'
                                                               % op['command']).json())
                    f.close()
                    remove(ASSIGNER_FILE_NAME + '.lock')
                    exit()

            except CatalogNotFoundException as e:
                # print(JSONResponse(status=1, error_message=str(e) + ' Try double-checking the path passed: ' +
                #                                                     json_obj.path).json())
                # exit()
                f.close()
                remove(ASSIGNER_FILE_NAME + '.lock')
                raise e
            except Exception as e:
                # print(JSONResponse(status=1, error_message=str(e)).json())
                # if json_obj.debug:
                #     raise e
                # exit()
                f.close()
                remove(ASSIGNER_FILE_NAME + '.lock')
                raise e

        f.close()

    try:
        if flag_pickle_changed:
            with open(assigner_cache, 'w') as f:
                f.write(jsonpickle.encode(assigner.save()))
                f.close()

            # Write a backup every so often
            if assigner.is_time_for_backup():

                # Set last backup date/time to now
                assigner.mark_last_backup_timestamp()

                if not (path.exists(BACKUP_FOLDER) and path.isdir(BACKUP_FOLDER)):
                    mkdir(BACKUP_FOLDER)

                f_name, f_ext = path.splitext(assigner_cache)
                backup_path = path.join(BACKUP_FOLDER, f_name + '-' + str(datetime.today().isoformat()) + f_ext)

                with open(backup_path, 'w') as f:

                    # Write a copy of the data to the backup file
                    f.write(jsonpickle.encode(assigner.save()))
                    f.close()

    except Exception as e:
        remove(ASSIGNER_FILE_NAME + '.lock')
        raise e
        # print(JSONResponse(status=1, error_message=str(e)).json())
        # exit()

    # If all the operations were successful, return the final result (before skip / next)
    print(JSONResponse(status=0, content=last_tagged_image).json())
    remove(ASSIGNER_FILE_NAME + '.lock')

except Exception as e:
    if s.GCLOUD_ERROR_REPORTING:
        from google.cloud import error_reporting

        client = error_reporting.Client()
        client.report(str(e))
        raise e
