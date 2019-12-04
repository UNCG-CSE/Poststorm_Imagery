from __future__ import print_function

import os
import re
import sys
from typing import Union, Pattern, List

from psicollect.common import s


def print_error(*args, **kwargs) -> None:  # pragma: no cover
    """Take string(s) and print them to console as an error (red text) instead of a normal message (white text).

    :param args: The args passed to the `print` function
    :param kwargs: The kwargs passed to the `print` function
    """
    print(*args, file=sys.stderr, **kwargs)


def to_readable_bytes(byte_count: int or None) -> str:
    """Take in a number of bytes (integer) and write it out in a human readable format (for printing). This
    method will output a number like "23.52 GiBs", "1.3 MiBs", or "324.45 KiBs" for the corresponding byte count.
    1 GiB = 1024 MiBs, 1 MiB = 1024 KiBs, and 1 KiB = 1024 Bytes.

    :param byte_count: The number of bytes to format
    :return: The human-readable string
    """
    if type(byte_count) != int:
        return "??? Bytes"

    if byte_count < 2 ** 20:  # MiB = 2^20
        return str(round(byte_count / 2 ** 10, 2)) + ' KiBs'
    if byte_count < 2 ** 30:  # GiB = 2^30
        return str(round(byte_count / 2 ** 20, 2)) + ' MiBs'
    else:
        return str(round(byte_count / 2 ** 30, 2)) + ' GiBs'


def validate_and_expand_path(path: Union[bytes, str]) -> Union[bytes, str]:
    """
    Validates a path-like object to make sure that it is a possible path (not that it exists, though) then converts
    it to an absolute path (if it is not already) for the system and expands out common variables like $USER to the
    current machine the script is running on.

    :param path: The path to validate and expand variables for
    :returns: The absolute
    """

    # Convert string to absolute path for uniformity
    new_path = os.path.abspath(path)

    # Expand out any path keywords or variables for certain operating system
    new_path = os.path.expanduser(os.path.expandvars(new_path))

    return new_path


def all_files_recursively(root_path: Union[bytes, str],
                          unix_sep: bool = False,
                          require_geom: bool = False,
                          file_extension: str = 'jpg',
                          file_search_re: Pattern = '.*',
                          debug: bool = s.DEFAULT_DEBUG,
                          verbosity: int = s.DEFAULT_VERBOSITY) -> List[str]:
    """A method to allow for recursively finding all files (including their absolute path on the local machine in
    order. This method also accepts an optional regular expression to match file names to and/or a specific file
    extension for the purpose of only getting specific file types.

    :param root_path: The path to begin searching recursively for matching files in
    :param unix_sep: Whether to replace all '\' with a '/' in the file paths on Windows
    :param require_geom: Whether or not to return only files with a .geom file associated with them
    :param file_extension: The file extension required to be included in the returned list
    :param file_search_re: The file name (including the extension) to be searched for as a regular expression
    :param debug: Whether (True) or not (False) to override default debug flag and output additional statements
    :param verbosity: The frequency of debug statement output (1 = LOW, 2 = MEDIUM, 3 = HIGH)
    :return: A list of files with their relative path
    """

    # Make search pattern case-insensitive
    file_search_re = re.compile(file_search_re, re.IGNORECASE)

    files = list()

    if debug and verbosity >= 1:
        print('\nSearching through ' + root_path + ' for the pattern "' + str(file_search_re.pattern) + '" ...\n')

    for (dir_path, dir_names, file_names) in os.walk(top=root_path, followlinks=True, topdown=False):
        for f in file_names:
            abs_file_path = os.path.join(dir_path, f)

            # Check file extensions only if the file_extension parameter is defined
            if f.endswith('.' + file_extension):
                if debug and verbosity >= 1:
                    print('\r' + abs_file_path + ' ... ', end='')

                # Find the path for the related .geom file
                geom_path = validate_and_expand_path(
                    re.sub(pattern='\\.[^.]*$', repl='.geom', string=str(abs_file_path)))

                # Find if the file name ends with a '(#)' meaning that it is a duplicated file and compare to original
                # file's size to see if there are truly duplicates (same size and original is not removed)
                if re.search(' \\(\\d\\)\\.', f) \
                        and os.path.exists(os.path.join(dir_path, re.sub(' \\(\\d\\)\\.', '.', f))) \
                        and os.path.getsize(os.path.join(dir_path, re.sub(' \\(\\d\\)\\.', '.', f))) is not \
                        os.path.getsize(abs_file_path):
                    if debug and verbosity >= 1:
                        # In-line progress (no spam when verbosity is 1)
                        print('duplicate file!', end='')

                        if verbosity >= 2:
                            # Multi-line output of progress (may be quite verbose)
                            print()

                # If the .geom file is required, make sure it exists
                elif require_geom and not os.path.exists(geom_path):
                    if debug and verbosity >= 1:
                        # In-line progress (no spam when verbosity is 1)
                        print('does not have required .geom file!', end='')

                        if verbosity >= 2:
                            # Multi-line output of progress (may be quite verbose)
                            print()

                # If the file's path matches the regular expression pattern
                elif re.search(file_search_re, f):
                    if debug and verbosity >= 1:
                        # In-line progress (no spam when verbosity is 1)
                        print('matches pattern!', end='')

                        if verbosity >= 2:
                            # Multi-line output of progress (may be quite verbose)
                            print()
                    if unix_sep:
                        files.append(str(os.path.relpath(path=abs_file_path,
                                                         start=root_path)).replace('\\', '/'))
                    else:
                        files.append(str(os.path.relpath(path=abs_file_path, start=root_path)))

                # The file just doesn't match the pattern, so output so if in debug
                elif debug and verbosity >= 1:
                    # In-line progress (no spam when verbosity is 1)
                    print('does not match pattern!', end='')

                    if verbosity >= 2:
                        # Multi-line output of progress (may be quite verbose)
                        print()

    return files
