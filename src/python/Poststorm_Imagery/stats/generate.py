from typing import Union, List

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

    if debug:
        print('Files in "scope_path:"')
        for f in files:
            print('\t-', f)


# Temporary debug statement for testing
generate_index_from_scope(debug=True, scope_path='/mnt/Secondary/mcmoretz@uncg.edu/C-Sick/data/Barry',
                          file_extension='jpg')
