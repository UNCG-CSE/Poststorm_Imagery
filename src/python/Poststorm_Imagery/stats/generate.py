import os
import re
from typing import Union, List

import pandas as pd

from src.python.Poststorm_Imagery.collector import s, h


def generate_index_from_scope(scope_path: Union[str, bytes] = s.DATA_PATH, **kwargs) -> None:
    """
    A function to generate an index of all the data in the scope specified. Does not generate statistics, but instead
    allows for listing the data details based off of each file's attributes. Returns a Generator (an iterable object)
    that can be looped through with a for-loop or similar.

    :param scope_path: The root path to start indexing files from
    :param debug: Whether to print out what's happening
    """
    debug = (kwargs['debug'] if 'debug' in kwargs else False)

    scope_path = h.validate_and_expand_path(scope_path)

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
        print()
        print('Generating DataFrame and calculating statistics...\n')

    file_stats = pd.DataFrame(data=files, columns=['file'])

    # file_stats['size'] = file_stats['file'].apply(lambda row: os.path.getsize(os.path.join(scope_path, row)))
    # file_stats['time'] = file_stats['file'].apply(lambda row: os.path.getmtime(os.path.join(scope_path, row)))
    file_stats['ll_lat'] = file_stats['file'].apply(
        lambda row: get_geom_field(field_id='ll_lat', file_path=os.path.join(scope_path, row), **kwargs))

    if debug:
        print(file_stats)


def get_geom_field(field_id: str, file_path: Union[bytes, str], **kwargs) -> str or None:
    debug = (kwargs['debug'] if 'debug' in kwargs else False)

    # Get the .geom file that corresponds to this file (substitute existing extension for ".geom")
    geom_path = h.validate_and_expand_path(re.sub(pattern='\\.[^.]*$', repl='.geom', string=str(file_path)))

    if os.path.exists(geom_path) is False:
        h.print_error('Could not find .geom file for "' + file_path + '": "' + geom_path + '"')
        return None

    with open(geom_path, 'r') as f:
        for line in f.readlines():
            value = re.findall(field_id + ':\\s+(.*)', line)
            if len(value) > 0:

                f.close()
                if debug:
                    print('Found value "' + field_id + '" as ' + str(value[0]) + ' in ' + geom_path)
                return value[0]

        f.close()
        h.print_error('Could not find field "' + field_id + '" in "' + geom_path + '"')
        return None
