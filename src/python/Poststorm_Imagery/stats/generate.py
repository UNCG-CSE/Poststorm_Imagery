import os
import sys
from typing import Union, List

import pandas as pd

from src.python.Poststorm_Imagery.collector import s, h


def generate_index_from_scope(scope_path: Union[str, bytes] = s.DATA_PATH, debug: bool = False, **kwargs) -> None:
    """
    A function to generate an index of all the data in the scope specified. Does not generate statistics, but instead
    allows for listing the data details based off of each file's attributes. Returns a Generator (an iterable object)
    that can be looped through with a for-loop or similar.

    :param scope_path: The root path to start indexing files from
    :param debug: Whether to print out what's happening
    """

    scope_path = h.validate_and_expand_path(scope_path)

    # Get a list of all files starting at the path specified
    files: List[str] = h.all_files_recursively(scope_path, **kwargs)

    if debug and False:
        file_list_number = 1
        print('Files in "' + str(scope_path) + ':"')

        for f in files:
            print(str(file_list_number) + '. ' + ' ' * (6 - len(str(file_list_number))) + f)
            file_list_number += 1

    """
    if '\\' in files[0]:
        for i in range(len(files)):
            files[i] = files[i].replace('\\', '/')
    """

    file_stats = pd.DataFrame(data=files, columns=['File'])

    file_stats['Size'] = file_stats['File'].apply(lambda row: os.path.getsize(os.path.join(scope_path, row)))
    file_stats['Time'] = file_stats['File'].apply(lambda row: os.path.getmtime(os.path.join(scope_path, row)))

    if debug:
        print(file_stats)


# Temporary debug statement for testing
generate_index_from_scope(debug=True, scope_path='F:\\Shared drives\\C-Sick\\data\\Barry', file_extension='jpg')
