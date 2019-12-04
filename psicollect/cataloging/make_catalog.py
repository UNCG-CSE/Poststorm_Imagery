import hashlib
import math
import os
import re
import time
from datetime import datetime
from typing import Union, List, Dict, Set, Pattern

import pandas as pd
from numpy import NaN

from psicollect.common import h, s

flag_unsaved_changes = False  # Keep track of if files have been committed to the disk


class Cataloging:

    @staticmethod
    def parse_catalog_path(scope_path: str = None) -> str:
        """
        Attempts to find the catalog file given a current path. It does this by first checking to see if there is a
        local copy of the catalog in the scope specified. If there isn't, the search then goes to the project data
        directory to get the possible global copy.

        :param scope_path: The root path of the scope to search for the catalog.csv in or None to default to the
        global, storm non-specific file if one exists ('default.csv')
        :return: The path to the catalog file, including the filename and extension
        :except CatalogNotFoundException: If a suitable catalog file cannot be found in the scope or project dir
        """

        storm_id: str or None = Cataloging._get_storm_from_path(scope_path=scope_path)
        catalog_path: str = h.validate_and_expand_path(Cataloging.get_catalog_path(storm_id=storm_id))
        alt_catalog_path: str = h.validate_and_expand_path(os.path.join(scope_path, s.CATALOG_FILE_DEFAULT))

        if os.path.exists(catalog_path) and os.path.isfile(catalog_path):
            # The catalog exists somewhere in the global catalog directory
            return h.validate_and_expand_path(catalog_path)

        elif os.path.exists(alt_catalog_path) and os.path.isfile(alt_catalog_path):
            # The catalog was found as catalog.csv in the scope path
            return h.validate_and_expand_path(os.path.join(scope_path, s.CATALOG_FILE_DEFAULT))

        else:
            raise CatalogNotFoundException

    @staticmethod
    def get_catalog_path(storm_id: str = None) -> str:
        """
        Get the catalog path as specified in s.py. This will return the absolute path on the local machine including
        the file name and extension (e.g. '/home/psic_user/Poststorm_Imagery/data/catalogs/v1/florence.csv').

        :param storm_id: The id of the storm (usually the name of the storm, lower-cased with '_' instead of spaces)
        :return: The absolute path of where the catalog should be (may not actually exist) including the filename and
        extension
        """

        if storm_id is None:
            return h.validate_and_expand_path(os.path.join(s.CATALOG_DATA_PATH, s.CATALOG_FILE_DEFAULT))

        else:
            return h.validate_and_expand_path(
                os.path.join(s.CATALOG_DATA_PATH, s.CATALOG_FILE.replace('${storm_id}', storm_id)))

    @staticmethod
    def generate_index_from_scope(scope_path: Union[str, bytes] = s.DATA_PATH,
                                  fields_needed: Set = s.DEFAULT_FIELDS.copy(),
                                  save_interval: int = 1000,
                                  require_geom: bool = False,
                                  override_catalog_path: Union[bytes, str, None] = None,
                                  debug: bool = s.DEFAULT_DEBUG,
                                  verbosity: int = s.DEFAULT_VERBOSITY,
                                  **kwargs) -> None:
        """
        A function to generate an index of all the data in the scope specified. Does not generate statistics, but
        instead allows for listing the data details based off of each file's attributes. Returns a Generator (an
        iterable object) that can be looped through with a for-loop or similar.

        :param scope_path: The root path to start indexing files from
        :param fields_needed: The fields to include in the catalog (gathered from the local file system)
        :param save_interval: The interval in which to save the data to the disk when accessing the .geom files,
        measured in file access operations. (0 = never save, 1000 = save after every 1,000 files read, etc.)
        :param require_geom: Whether (True) or not (False) to require a .geom file present in search for valid files
        :param override_catalog_path: If set, the program will not search for a catalog, and instead use the path to
        the catalog provided as a string.
        :param debug: Whether (True) or not (False) to override default debug flag and output additional statements
        :param verbosity: The frequency of debug statement output (1 = LOW, 2 = MEDIUM, 3 = HIGH)
        """

        global flag_unsaved_changes  # Include the global variable defined at top of this script

        if debug:
            print('Attempting to parse the storm name from the given scope path...')

        scope_path = h.validate_and_expand_path(path=scope_path)
        storm_id: str or None = Cataloging._get_storm_from_path(scope_path=scope_path, debug=debug)

        if override_catalog_path is None:  # pragma: no cover
            try:
                catalog_path = Cataloging.parse_catalog_path(scope_path=scope_path)
            except CatalogNotFoundException:
                catalog_path = Cataloging.get_catalog_path(storm_id=storm_id)

        else:
            # A catalog path is provided, so no need to search (used for testing)
            catalog_path = override_catalog_path

        ##########################################
        # Collect matching files from filesystem #
        ##########################################

        # Get a list of all files starting at the path specified
        files: List[str] = h.all_files_recursively(scope_path, unix_sep=True, require_geom=require_geom,
                                                   debug=debug, verbosity=verbosity, **kwargs)

        if len(files) == 0:
            raise CatalogNoEntriesException(curr_dir=scope_path)

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

        current_fields_needed: Set = fields_needed.copy()
        flag_unsaved_changes = False

        catalog: pd.DataFrame

        if os.path.exists(catalog_path) is False:
            # If the catalog file doesn't exist, create a new one

            entries: List[Dict[str, str or int]] = list()

            for i in range(len(files)):
                entry: dict = dict()
                entry['file'] = files[i]
                entry['storm_id'] = Cataloging._get_storm_from_path(os.path.join(scope_path, files[i])).lower()
                entry['archive'] = Cataloging._get_archive_from_path(os.path.join(scope_path, files[i])).lower()
                entry['image'] = Cataloging._get_image_from_path(os.path.join(scope_path, files[i]))
                entries.append(entry)

            catalog: pd.DataFrame = pd.DataFrame(entries)

            # DataFrame is populated with these fields, so remove them from the needed list
            current_fields_needed -= {'file', 'storm_id', 'archive', 'image'}

            if 'size' in current_fields_needed:
                sizes: List[int] = list()

                if debug:
                    print('Calculating sizes of files ... ')

                for i in range(len(files)):
                    sizes.append(os.path.getsize(os.path.join(scope_path, files[i])))

                catalog['size'] = sizes
                flag_unsaved_changes = True
                current_fields_needed.remove('size')

            if 'date' in current_fields_needed:
                dates: List[str] = list()

                if debug:
                    print('Calculating modify time of files ... ')

                for i in range(len(files)):
                    dates.append(Cataloging._get_best_date(os.path.join(scope_path, files[i])))

                catalog['date'] = dates
                flag_unsaved_changes = True
                current_fields_needed.remove('date')

            # Create the file in the scope directory
            Cataloging._force_save_catalog(catalog=catalog, scope_path=scope_path)
        else:
            catalog = pd.read_csv(catalog_path, usecols=lambda col_label: col_label in current_fields_needed)

            # Remove basic info as it should already exist in the CSV file
            current_fields_needed -= {'file', 'storm_id', 'archive', 'image', 'date', 'size'}

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
                        or (type(row[field]) is not str and str(row[field]) != "nan"):
                    print('Found existing data ... field: ' + field + '  row[field]: "' + str(row[field]) +
                          '" type(row[field])' + str(type(row[field])) + ' ... Skipping this field!')
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
                Cataloging._force_save_catalog(catalog=catalog, scope_path=scope_path)

        if debug and verbosity >= 1:
            print()
            print(catalog)

        # Do a final save of the file
        Cataloging._force_save_catalog(catalog=catalog, scope_path=scope_path)

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
    def _get_image_from_path(scope_path: Union[bytes, str] = None) -> str or None:

        scope_path = h.validate_and_expand_path(scope_path)

        image_file: str = os.path.split(scope_path)[1]

        if '.jpg' in image_file:
            return image_file
        else:
            return None

    @staticmethod
    def _get_storm_from_path(scope_path: Union[bytes, str] = None, debug: bool = s.DEFAULT_DEBUG,
                             recurse_count: int = 0) -> str or None:

        if debug:
            print('Looking for storm in path: ' + str(scope_path))

        scope_path = h.validate_and_expand_path(scope_path)

        system_root = os.path.abspath(os.sep)

        if os.path.split(scope_path)[0] == system_root:
            # If the filesystem root directory is reached, a storm-specific catalog cannot be found

            if debug:
                print('No storm found! Returning None')

            return None

        path_tail: str = os.path.split(scope_path)[1]

        if recurse_count > 10:
            raise RecursionError('Could not find storm in path after 10 iterations!')

        if len(path_tail) <= 1 \
                or path_tail[0].islower() \
                or re.match('.*([._]).*', path_tail) \
                or scope_path == s.DATA_PATH:
            # If the current directory is either not defined (input ends with / instead of the dir name)
            # or the first character of the directory's name is lower-cased (storms should have capitals)
            # or the directory is actually a file or archive or is the data path

            # Keep recursively checking each directory to match the pattern (traverse back through path)
            return Cataloging._get_storm_from_path(scope_path=os.path.split(scope_path)[0],
                                                   recurse_count=(recurse_count + 1))

        else:
            if debug:
                print('Found storm name (' + str(path_tail) + ') in path: ' + str(scope_path))

            return path_tail

    @staticmethod
    def _get_archive_from_path(scope_path: Union[bytes, str] = None) -> str or None:

        scope_path = h.validate_and_expand_path(scope_path)

        if len(os.path.split(scope_path)[0]) == 0:

            # If the filesystem root directory is reached, a storm-specific catalog cannot be found
            return None

        path_tail: str = os.path.split(scope_path)[1]

        if len(path_tail) == 0 \
            or ('20' in path_tail and '_jpgs' in path_tail) is False \
                or scope_path == s.DATA_PATH:
            # If the current directory is either not defined (input ends with / instead of the dir name)
            # or does not look like an archive name
            # or is the data path
            # Keep recursively checking each directory to match the pattern (traverse back through path)
            return Cataloging._get_archive_from_path(scope_path=os.path.split(scope_path)[0])

        else:
            return path_tail

    @staticmethod
    def _force_save_catalog(catalog: pd.DataFrame, scope_path: Union[bytes, str]):
        global flag_unsaved_changes  # Include the global variable defined at top of this script

        if flag_unsaved_changes is False:
            return

        flag_save_incomplete = True

        while flag_save_incomplete:
            try:
                storm_id: str = Cataloging._get_storm_from_path(scope_path=scope_path)
                catalog_path: str = Cataloging.get_catalog_path(storm_id=storm_id)

                if os.path.exists(os.path.split(catalog_path)[0]) is False:
                    # Create the necessary directories if they do not exist
                    os.makedirs(os.path.split(catalog_path)[0])

                # Periodically save the file based on the save_interval parameter
                catalog.to_csv(Cataloging.get_catalog_path(storm_id=storm_id))
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

        result: Dict[str] = dict()

        if os.path.exists(geom_path) is False:
            h.print_error('\n\nCould not find .geom file for "' + file_path + '": "' + geom_path + '"')
            for field_id in field_id_set:
                # Since no .geom file was found, fill with NaN values
                result[field_id] = NaN

            return result

        if os.path.getsize(geom_path) == 0:
            h.print_error('\n\nThe .geom file for "' + file_path + '": "' + geom_path + '" is 0 KiBs.\n'
                          'Bad file access may have caused this, so check the archive to see if the image and '
                          'the .geom files in the archive are the same as the unzipped versions!\n')
            for field_id in field_id_set:
                # Since no .geom file was found, fill with NaN values
                result[field_id] = NaN

            return result

        # Generate a new hash object to store the hash data
        hashing: hashlib.md5 = hashlib.md5()

        with open(geom_path, 'rb') as f:
            # Use the geom file's bytes to generate a checksum

            if 'geom_checksum' in field_id_set:
                # Generate a md5 hash to help ensure the correct data is being referenced if compared elsewhere
                hashing.update(f.read())
                result['geom_checksum'] = hashing.hexdigest()
                field_id_set.remove('geom_checksum')

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
            for field_id in field_id_set:
                # Fill missing fields with NaN values
                result[field_id] = NaN

            return result


class CatalogNoEntriesException(IOError):
    def __init__(self, curr_dir: str):
        IOError.__init__(self, 'There were no images found in any sub-directories in ' + curr_dir)


class CatalogNotFoundException(IOError):
    def __init__(self):
        IOError.__init__(self, 'The catalog file was not found!')
