import math
import os
import re
import time
from datetime import datetime
from typing import Union, List, Dict, Set, Pattern

import pandas as pd

from psic import s, h

flag_unsaved_changes = False  # Keep track of if files have been committed to the disk


class Cataloging:

    CATALOG_FILE = s.CATALOG_FILE_NAME + '.csv'

    @staticmethod
    def generate_index_from_scope(scope_path: Union[str, bytes] = s.DATA_PATH, fields_needed: Set = s.DEFAULT_FIELDS.copy(),
                                  save_interval: int = 1000,
                                  debug: bool = s.DEFAULT_DEBUG,
                                  verbosity: int = s.DEFAULT_VERBOSITY,
                                  **kwargs) -> None:
        """
        A function to generate an index of all the data in the scope specified. Does not generate statistics, but instead
        allows for listing the data details based off of each file's attributes. Returns a Generator (an iterable object)
        that can be looped through with a for-loop or similar.

        :param scope_path: The root path to start indexing files from
        :param fields_needed: The fields to include in the catalog (gathered from the local file system)
        :param save_interval: The interval in which to save the data to the disk when accessing the .geom files,
        measured in file access operations. (0 = never save, 1000 = save after every 1,000 files read, etc.)
        :param debug: Whether (True) or not (False) to override default debug flag and output additional statements
        :param verbosity: The frequency of debug statement output (1 = LOW, 2 = MEDIUM, 3 = HIGH)
        """

        global flag_unsaved_changes  # Include the global variable defined at top of this script

        scope_path = h.validate_and_expand_path(path=scope_path)
        catalog_path = os.path.join(scope_path, Cataloging.CATALOG_FILE)

        ##########################################
        # Collect matching files from filesystem #
        ##########################################

        # Get a list of all files starting at the path specified
        files: List[str] = h.all_files_recursively(scope_path, unix_sep=True, require_geom=True,
                                                   debug=debug, verbosity=verbosity, **kwargs)

        if debug and verbosity >= 2:
            print()
            print('Matching files in "' + str(scope_path) + '"\n')

            if verbosity < 3 and len(files) > 10:
                # Print only the first five and last five elements (similar to pandas's DataFrames)
                for i in (list(range(1, 6)) + list(range(len(files) - 4, len(files) + 1))):

                    # Right-align the file numbers, because why not
                    print(('{:>' + str(len(str(len(files) + 1))) + '}').format(i) + '  ' + files[i - 1])
                    if i == 5:
                        print(('{:>' + str(len(str(len(files) + 1))) + '}').format('...'))

            else:
                file_list_number = 1

                # Print all elements if there are 10 or less
                for f in files:

                    # Right-align the file numbers, because why not
                    print(('{:>' + str(len(str(len(files) + 1))) + '}').format(file_list_number) + '  ' + f)
                    file_list_number += 1

        ####################################################################
        # Load / generate the table (DataFrame) if it doesn't exist        #
        # and populate with file path, file size, and date image was taken #
        ####################################################################

        if debug:
            print('\nGenerating DataFrame and calculating statistics ... \n')

        catalog: pd.DataFrame or None

        current_fields_needed: Set = fields_needed.copy()
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
            if 'date' in current_fields_needed:
                if debug:
                    print('Calculating modify time of files ... ')
                catalog['date'] = catalog['file'].apply(
                    lambda x: Cataloging._get_best_date(os.path.join(scope_path, x)))
                current_fields_needed.remove('date')
                flag_unsaved_changes = True

            # Create the file in the scope directory
            Cataloging._force_save_catalog(catalog=catalog, catalog_path=catalog_path)
        else:
            catalog = pd.read_csv(catalog_path, usecols=lambda col_label: col_label in current_fields_needed)

            # Remove the size and time from the sets as they should already exist in the CSV file
            current_fields_needed -= {'file', 'size', 'date'}

        ##########################################################################################
        # Collect information from the .geom files about latitude and longitude of image corners #
        ##########################################################################################

        if debug and verbosity >= 1:
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
                        or (type(row[field]) is not str and str(row[field]) == "nan"):
                    print('field: ' + field + '  row[field]: "' + str(row[field]) +
                          '" type(row[field])' + str(type(row[field])))
                    row_fields_needed.remove(field)

            # Only query the .geom file if there are fields still unfilled
            if len(row_fields_needed) > 0:

                # Look up the fields that are needed and still missing data
                geom_data: Dict[str, str] or None = Cataloging._get_geom_fields(
                    field_id_set=row_fields_needed, file_path=os.path.join(
                        scope_path, os.path.normpath(row['file'])), debug=debug, verbosity=verbosity)
                stat_files_accessed += 1

                if geom_data is not None:

                    # Store the values in the catalog's respective column by field name, in memory
                    for key, value in geom_data.items():
                        catalog.at[i, key] = value
                        flag_unsaved_changes = True

            if save_interval > 0 and stat_files_accessed % save_interval == 0:

                print('\rSaving catalog to disk (' + str(stat_files_accessed) +
                      ' .geom files accessed) ... ', end='')
                Cataloging._force_save_catalog(catalog=catalog, catalog_path=catalog_path)

        if debug and verbosity >= 1:
            print()
            print(catalog)

        # Do a final save of the file
        Cataloging._force_save_catalog(catalog=catalog, catalog_path=catalog_path)

    #####################################
    # Catalog-Specific Helper Functions #
    #####################################

    @staticmethod
    def _get_best_date(file_path: Union[bytes, str],
                       debug: bool = s.DEFAULT_DEBUG,
                       verbosity: int = s.DEFAULT_VERBOSITY) -> str:

        # Assume years can only be 2000 to 2099 (current unix time ends at 2038 anyways)
        pattern: Pattern = re.compile('[\\D]*(20\\d{2})(\\d{2})(\\d{2})\\D')

        # Search the entire path for a matching date format, take the last occurrence
        if re.search(pattern, file_path):
            year, month, day = re.search(pattern, file_path).groups()

            if debug and verbosity >= 1:
                # In-line progress (no spam when verbosity is 1)
                print('\rFound year: %s, month: %s, day: %s in PATH: %s' % (year, month, day, file_path), end='')

                if verbosity >= 2:
                    # Multi-line output of progress (may be quite verbose)
                    print()

            return year + '/' + month + '/' + day

        # If no date can be parsed from file path or file name, then fallback to timestamp (sometimes off by a day)
        else:
            h.print_error('Could not find any date in ' + file_path + ' ... resorting to file modify time!')
            return Cataloging._timestamp_to_utc(os.path.getmtime(file_path))

    @staticmethod
    def _timestamp_to_utc(timestamp: str or int) -> str:
        timestamp = datetime.utcfromtimestamp(timestamp)
        return timestamp.strftime("%Y/%m/%d")

    @staticmethod
    def _force_save_catalog(catalog: pd.DataFrame, catalog_path: str):
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
            except PermissionError as e:  # pragma: no cover
                h.print_error(str(e) + '\nTry closing the file if it is open in another program!\nWill attempt '
                                       'to save again in 10 seconds ... \n')
                time.sleep(10)

        print('Saved catalog to disk! ', end='')
        flag_unsaved_changes = False

    @staticmethod
    def _get_geom_fields(field_id_set: Set[str] or str, file_path: Union[bytes, str],
                         debug: bool = s.DEFAULT_DEBUG, verbosity: int = s.DEFAULT_VERBOSITY) \
            -> Union[Dict[str, str], str, None]:

        is_single_input = False

        # If only one id is entered (a single string), convert to a set of 1 element
        if type(field_id_set) is str:
            field_id_set: Set[str] = {field_id_set}
            is_single_input = True

        # Get the .geom file that corresponds to this file (substitute existing extension for ".geom")
        geom_path = h.validate_and_expand_path(re.sub(pattern='\\.[^.]*$', repl='.geom', string=str(file_path)))

        if os.path.exists(geom_path) is False:
            h.print_error('\n\nCould not find .geom file for "' + file_path + '": "' + geom_path + '"')
            return None

        if os.path.getsize(geom_path) == 0:
            h.print_error('\n\nThe .geom file for "' + file_path + '": "' + geom_path + '" is 0 KiBs.\n'
                          'Bad file access may have caused this, so check the archive to see if the image and the .geom'
                          ' files in the archive are the same as the unzipped versions!\n')
            return None

        result: Dict[str] = dict()

        with open(geom_path, 'r') as f:
            for line in f.readlines():

                # If there are no more fields to find, close the file and return the resulting dictionary or string
                if len(field_id_set) == 0:
                    f.close()

                    if debug and verbosity >= 2:
                        print('\rFound ' + str(len(result)) + ' value(s) in ' + geom_path, end='')

                        if verbosity >= 3:
                            print()  # RIP your console if you get here

                    if is_single_input and len(result) == 1:
                        # Return the first (and only value) as a single string
                        return str(list(result.values())[0])

                    return result

                field_id_set_full = field_id_set.copy()
                for field_id in field_id_set_full:
                    value = re.findall(field_id + ':\\s+(.*)', line)
                    if len(value) == 1:
                        result[field_id] = str(value[0])
                        field_id_set.remove(field_id)

            f.close()
            h.print_error('\nCould not find any values for fields ' + str(field_id_set) + ' in ' + geom_path)
            return None
