import math
import os
import re
import time
from typing import Union, List, Dict, Set

import pandas as pd

from src.python.Poststorm_Imagery.collector import s, h

MANIFEST_FILE = s.MANIFEST_FILE_NAME + '.csv'

DEFAULT_FIELDS = {'file', 'size', 'time',
                  'll_lat', 'll_lon', 'lr_lat', 'lr_lon',
                  'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}


def generate_index_from_scope(scope_path: Union[str, bytes] = s.DATA_PATH, fields_needed: Set = None,
                              save_interval: int = 1000, **kwargs) -> None:
    """
    A function to generate an index of all the data in the scope specified. Does not generate statistics, but instead
    allows for listing the data details based off of each file's attributes. Returns a Generator (an iterable object)
    that can be looped through with a for-loop or similar.

    :param scope_path: The root path to start indexing files from
    :param fields_needed: The fields to include in the manifest (gathered from the local file system)
    :param save_interval: The interval in which to save the data to the disk when accessing the .geom files,
    measured in file access operations. (0 = never save, 1000 = save after every 1,000 files read, etc.)
    """

    # If left empty, set to the default list of fields (sets are mutable)
    if fields_needed is None:
        fields_needed = DEFAULT_FIELDS.copy()

    debug = (kwargs['debug'] if 'debug' in kwargs else False)

    scope_path = h.validate_and_expand_path(scope_path)
    manifest_path = os.path.join(scope_path, MANIFEST_FILE)

    # Get a list of all files starting at the path specified
    files: List[str] = h.all_files_recursively(scope_path, **kwargs)

    if debug:
        print()
        print('Files in "' + str(scope_path) + '"\n')

        if len(files) > 10:
            # Print only the first five and last five elements (similar to pandas's DataFrames)
            for i in (list(range(1, 6)) + list(range(len(files) - 4, len(files) + 1))):

                # Right-align the file numbers, because why not
                print(('{:>' + str(len(str(len(files) + 1))) + '}').format(i) + '  ' + files[i - 1])
                if i is 5:
                    print(('{:>' + str(len(str(len(files) + 1))) + '}').format('...'))

        else:
            file_list_number = 1

            # Print all elements if there are 10 or less
            for f in files:

                # Right-align the file numbers, because why not
                print(('{:>' + str(len(str(len(files) + 1))) + '}').format(file_list_number) + '  ' + f)
                file_list_number += 1

    """
    if '\\' in files[0]:
        for i in range(len(files)):
            files[i] = files[i].replace('\\', '/')
    """

    if debug:
        print('\nGenerating DataFrame and calculating statistics...\n')

    manifest: pd.DataFrame or None = None
    all_fields_needed: Set = {'file', 'size', 'time',
                                  'll_lat', 'll_lon', 'lr_lat', 'lr_lon',
                                  'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}

    current_fields_needed: Set = all_fields_needed.copy()
    flag_unsaved_changes = False  # Keep track of if files have been committed to the disk

    if os.path.exists(manifest_path) is False:
        # If the manifest file doesn't exist, create a new one with the basic file info
        manifest = pd.DataFrame(data=files, columns=['file'])
        current_fields_needed.remove('file')

        if 'size' in current_fields_needed:
            manifest['size'] = manifest['file'].apply(lambda row: os.path.getsize(os.path.join(scope_path, row)))
            current_fields_needed.remove('size')
            flag_unsaved_changes = True
        if 'time' in current_fields_needed:
            manifest['time'] = manifest['file'].apply(lambda row: os.path.getmtime(os.path.join(scope_path, row)))
            current_fields_needed.remove('time')
            flag_unsaved_changes = True

        # Create the file in the scope directory
        manifest.to_csv(manifest_path)
        flag_unsaved_changes = False
        if debug:
            print('Saved manifest to disk!\n')
    else:
        manifest = pd.read_csv(manifest_path, usecols=lambda col_label: col_label in current_fields_needed)

        # Remove the size and time from the sets as they should already exist in the CSV file
        current_fields_needed -= {'file', 'size', 'time'}

    for field in current_fields_needed:

        # If a column for each field does not exist, create one for each field with all the values as empty strings
        if field not in manifest:
            manifest[field] = ''
            flag_unsaved_changes = True

    # TODO: Rewrite as an efficient operation with a resume option
    """ DISABLED: Not viable for time intensive operations as there is no way to resume if stopped
    manifest['ll_lat'], manifest['ll_lon'] = manifest['file'].apply(
        lambda row: get_geom_fields(field_id_set={'ll_lat', 'll_lon'},
                                    file_path=os.path.join(scope_path, row), **kwargs))
    """

    stat_files_accessed: int = 0

    # For any remaining fields needed (i.e. ll_lat), look for them in the .geom files
    for i, row in manifest.iterrows():
        row_fields_needed = current_fields_needed.copy()

        # Remove redundant queries to .geom file if the data is already present in the manifest
        for field in current_fields_needed:
            if type(row[field]) in {str, int} or math.isnan(row[field]) is False:
                print(row[field])
                row_fields_needed.remove(field)

        # Only query the .geom file if there are fields still unfilled
        if len(row_fields_needed) > 0:

            # Look up the fields that are needed and still missing data
            geom_data: Dict[str, str] or None = get_geom_fields(
                field_id_set=row_fields_needed, file_path=os.path.join(scope_path, row['file']), **kwargs)
            stat_files_accessed += 1

            # Store the values in the manifest's respective column by field name, in memory
            for key, value in geom_data.items():
                manifest.at[i, key] = value
                flag_unsaved_changes = True

        if flag_unsaved_changes and save_interval > 0 and stat_files_accessed % save_interval is 0:

            if debug:
                print('\nSaving partially completed manifest to disk (' + str(stat_files_accessed) + ' .geom files '
                                                                                              'accessed)...')
            flag_save_incomplete = True
            while flag_save_incomplete:
                try:
                    # Periodically save the file based on the save_interval parameter
                    manifest.to_csv(manifest_path)
                    flag_unsaved_changes = False
                    flag_save_incomplete = False
                except PermissionError as e:
                    h.print_error(str(e) + '\nTry closing the file if it is open in another program!\nWill attempt '
                                           'to save again in 10 seconds...\n')
                    time.sleep(10)

            if debug:
                print('Saved manifest to disk!\n')

    if debug:
        print(manifest)
        print('Saved manifest to disk!\n')

    # Do a final save of the file
    manifest.to_csv(manifest_path)


def get_geom_fields(field_id_set: Set[str] or str, file_path: Union[bytes, str], **kwargs) \
        -> Union[Dict[str, str], str, None]:
    debug = (kwargs['debug'] if 'debug' in kwargs else False)

    is_single_input = False

    # If only one id is entered (a single string), convert to a set of 1 element
    if type(field_id_set) is str:
        field_id_set: Set[str] = {field_id_set}
        is_single_input = True

    # Get the .geom file that corresponds to this file (substitute existing extension for ".geom")
    geom_path = h.validate_and_expand_path(re.sub(pattern='\\.[^.]*$', repl='.geom', string=str(file_path)))

    if os.path.exists(geom_path) is False:
        h.print_error('\nCould not find .geom file for "' + file_path + '": "' + geom_path + '"')
        return None

    result: Dict[str] = dict()

    with open(geom_path, 'r') as f:
        for line in f.readlines():

            # If there are no more fields to find, close the file and return the resulting dictionary or string
            if len(field_id_set) is 0:
                f.close()

                if debug:
                    print('Found value(s) ' + str(result) + ' in ' + geom_path)

                if is_single_input and len(result) is 1:
                    # Return the first (and only value) as a single string
                    return str(list(result.values())[0])

                return result

            field_id_set_full = field_id_set.copy()
            for field_id in field_id_set_full:
                value = re.findall(field_id + ':\\s+(.*)', line)
                if len(value) is 1:
                    result[field_id] = str(value[0])
                    field_id_set.remove(field_id)

        f.close()
        h.print_error('Could not find any values for fields in "' + str(field_id_set))
        return None
