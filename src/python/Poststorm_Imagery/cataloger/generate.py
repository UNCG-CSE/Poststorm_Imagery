import math
import os
import re
import time
from typing import Union, List, Dict, Set

import pandas as pd

from src.python.Poststorm_Imagery import s, h

CATALOG_FILE = s.CATALOG_FILE_NAME + '.csv'

DEFAULT_FIELDS = {'file', 'size', 'time',
                  'll_lat', 'll_lon', 'lr_lat', 'lr_lon',
                  'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}

flag_unsaved_changes = False  # Keep track of if files have been committed to the disk


def generate_index_from_scope(scope_path: Union[str, bytes] = s.DATA_PATH, fields_needed: Set = None,
                              save_interval: int = 1000, **kwargs) -> None:
    """
    A function to generate an index of all the data in the scope specified. Does not generate statistics, but instead
    allows for listing the data details based off of each file's attributes. Returns a Generator (an iterable object)
    that can be looped through with a for-loop or similar.

    :param scope_path: The root path to start indexing files from
    :param fields_needed: The fields to include in the catalog (gathered from the local file system)
    :param save_interval: The interval in which to save the data to the disk when accessing the .geom files,
    measured in file access operations. (0 = never save, 1000 = save after every 1,000 files read, etc.)
    """

    # If left empty, set to the default list of fields (sets are mutable)
    if fields_needed is None:
        fields_needed = DEFAULT_FIELDS.copy()

    debug = (kwargs['debug'] if 'debug' in kwargs else False)
    global flag_unsaved_changes  # Include the global variable defined at top of this script

    scope_path = h.validate_and_expand_path(path=scope_path)
    catalog_path = os.path.join(scope_path, CATALOG_FILE)

    # Get a list of all files starting at the path specified
    files: List[str] = h.all_files_recursively(scope_path, unix_sep=True, require_geom=True, **kwargs)

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

    if debug:
        print('\nGenerating DataFrame and calculating statistics ... \n')

    catalog: pd.DataFrame or None = None
    all_fields_needed: Set = {'file', 'size', 'time',
                                  'll_lat', 'll_lon', 'lr_lat', 'lr_lon',
                                  'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}

    current_fields_needed: Set = all_fields_needed.copy()
    flag_unsaved_changes = False

    if os.path.exists(catalog_path) is False:
        # If the catalog file doesn't exist, create a new one with the basic file info
        catalog = pd.DataFrame(data=files, columns=['file'])
        current_fields_needed.remove('file')

        if 'size' in current_fields_needed:
            if debug:
                print('Calculating sizes of files ... ')
            catalog['size'] = catalog['file'].apply(lambda x: os.path.getsize(os.path.join(scope_path, x)))
            current_fields_needed.remove('size')
            flag_unsaved_changes = True
        if 'time' in current_fields_needed:
            if debug:
                print('Calculating modify time of files ... ')
            catalog['time'] = catalog['file'].apply(lambda x: os.path.getmtime(os.path.join(scope_path, x)))
            current_fields_needed.remove('time')
            flag_unsaved_changes = True

        # Create the file in the scope directory
        force_save_catalog(catalog=catalog, catalog_path=catalog_path)
    else:
        catalog = pd.read_csv(catalog_path, usecols=lambda col_label: col_label in current_fields_needed)

        # Remove the size and time from the sets as they should already exist in the CSV file
        current_fields_needed -= {'file', 'size', 'time'}

    if debug:
        print('Basic data is complete! Moving on to .geom specific data ... ')

    for field in current_fields_needed:

        # If a column for each field does not exist, create one for each field with all the values as empty strings
        if field not in catalog:
            catalog[field] = ''
            flag_unsaved_changes = True

    stat_files_accessed: int = 0

    # For any remaining fields needed (i.e. ll_lat), look for them in the .geom files
    for i, row in catalog.iterrows():

        formatted_counter = '{:.2f}'.format(float((i / len(files)) * 100))

        print('\rProcessing file ' + str(i + 1) + ' of ' + str(len(files)) +
              ' (' + formatted_counter + '%) ' + '.' * (math.floor(((i + 1) % 9) / 3) + 1), end=' ')

        row_fields_needed = current_fields_needed.copy()

        # Remove redundant queries to .geom file if the data is already present in the catalog
        for field in current_fields_needed:
            if (type(row[field]) is str and len(row[field]) > 0) \
                    or (type(row[field]) is not str and str(row[field]) is "nan"):
                print('field: ' + field + '  row[field]: "' + str(row[field]) + '" type(row[field])' + str(type(row[
                                                                                                                field])))
                row_fields_needed.remove(field)

        # Only query the .geom file if there are fields still unfilled
        if len(row_fields_needed) > 0:

            # Look up the fields that are needed and still missing data
            geom_data: Dict[str, str] or None = get_geom_fields(
                field_id_set=row_fields_needed, file_path=os.path.join(
                    scope_path, os.path.normpath(row['file'])), **kwargs)
            stat_files_accessed += 1

            if geom_data is not None:

                # Store the values in the catalog's respective column by field name, in memory
                for key, value in geom_data.items():
                    catalog.at[i, key] = value
                    flag_unsaved_changes = True

        if save_interval > 0 and stat_files_accessed % save_interval is 0:

            print('\nSaving partially completed catalog to disk (' + str(stat_files_accessed) +
                  ' .geom files accessed) ... ')
            force_save_catalog(catalog=catalog, catalog_path=catalog_path)

    if debug:
        print()
        print(catalog)

    # Do a final save of the file
    force_save_catalog(catalog=catalog, catalog_path=catalog_path)


def force_save_catalog(catalog: pd.DataFrame, catalog_path: str):
    global flag_unsaved_changes  # Include the global variable defined at top of this script

    if flag_unsaved_changes is False:
        return

    flag_save_incomplete = True

    while flag_save_incomplete:
        try:
            # Periodically save the file based on the save_interval parameter
            catalog.to_csv(catalog_path)
            flag_unsaved_changes = False
            flag_save_incomplete = False
        except PermissionError as e:
            h.print_error(str(e) + '\nTry closing the file if it is open in another program!\nWill attempt '
                                   'to save again in 10 seconds ... \n')
            time.sleep(10)

    print('Saved catalog to disk!\n')
    flag_unsaved_changes = False


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

    if os.path.getsize(geom_path) is 0:
        h.print_error('\nThe .geom file for "' + file_path + '": "' + geom_path + '" is 0 KiBs.\n'
                      'Bad file access may have caused this, so check the archive to see if the image and the .geom '
                      'files in the archive are the same as the unzipped versions!\n')
        return None

    result: Dict[str] = dict()

    with open(geom_path, 'r') as f:
        for line in f.readlines():

            # If there are no more fields to find, close the file and return the resulting dictionary or string
            if len(field_id_set) is 0:
                f.close()

                # if debug:
                #     print('\rFound ' + str(len(result)) + ' value(s) in ' + geom_path, end='')

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
        h.print_error('\nCould not find any values for fields ' + str(field_id_set) + ' in ' + geom_path)
        return None
