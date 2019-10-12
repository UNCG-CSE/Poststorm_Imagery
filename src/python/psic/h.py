from __future__ import print_function

import os
import re
import sys
from typing import Union, Dict, Pattern, List

import pytest

from psic import s


@pytest.mark.skip
def print_error(*args, **kwargs) -> None:
    """Take string(s) and print them to console as an error (red text) instead of a normal message (white text).

    :param args: The args passed to the `print` function
    :param kwargs: The kwargs passed to the `print` function
    """
    print(*args, file=sys.stderr, **kwargs)


def to_readable_bytes(byte_count: int) -> str:
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


def update_file_lock(base_file: Union[bytes, str], user: str,
                     total_size_byte: int, part_size_byte: None or int = None):
    """Modify or add a lock file (if one doesn't exist) for any file specified by the parameter,
    `base_file`. A lock is used in the case that multiple people are downloading to the same directory at the same time
    either over the internet on a service like Google Team Drive or elsewhere, where files may not appear to others
    for a very long time, because the file has to be fully uploaded to show to others. This ensures that periodically
    the client will upload .lock file, telling other users' clients some basic information about the downloading user's
    progress. This includes the user downloading the file, the total size of the file they're downloading, the amount
    of the file they already have downloaded, and when the former info was last updated (inferred from the modified
    timestamp of the .lock file).

    :param base_file: The path to the file to lock (not including .lock)
    :param user: The user to lock the file to
    :param total_size_byte: The total size of the file being downloaded in bytes
    :param part_size_byte: The size of the file in bytes that has been downloaded so far
    """
    lock = open(base_file + s.LOCK_SUFFIX, 'w')
    lock.write('user = ' + user + '\n')
    if part_size_byte is not None:
        lock.writelines(s.LOCK_PART_SIZE_BYTES_FIELD + ' = ' + str(part_size_byte) + '\n')
    if total_size_byte is not None:
        lock.writelines(s.LOCK_TOTAL_SIZE_BYTES_FIELD + ' = ' + str(total_size_byte) + '\n')

    lock.close()


def get_lock_info(base_file: Union[bytes, str]) -> Dict:
    """Get the current lock information on a file, returning None for all values not found.  This includes the user
    downloading the file, the total size of the file they're downloading, the amount of the file they already have
    downloaded, and when the former info was last updated (inferred from the modified timestamp of the .lock file).

    :param base_file: The path to the file to read lock info from (not including .lock)
    :return: A dictionary with entries for user, total byte size, and downloaded byte size (`byte_size`)
    """
    if os.path.exists(base_file + s.LOCK_SUFFIX) is False:
        return {'user': None, s.LOCK_PART_SIZE_BYTES_FIELD: None, s.LOCK_TOTAL_SIZE_BYTES_FIELD: None}

    with open(base_file + s.LOCK_SUFFIX, 'r') as lock:
        output = {'user': None, s.LOCK_PART_SIZE_BYTES_FIELD: None, s.LOCK_TOTAL_SIZE_BYTES_FIELD: None}
        for line in lock.readlines():
            if line.startswith('user = '):
                output['user'] = str(re.findall('^user = (.*)', line)[0])
            elif line.startswith(s.LOCK_PART_SIZE_BYTES_FIELD + ' = '):
                output[s.LOCK_PART_SIZE_BYTES_FIELD] = int(re.findall('^' + s.LOCK_PART_SIZE_BYTES_FIELD + ' = (.*)', line)[0])
            elif line.startswith(s.LOCK_TOTAL_SIZE_BYTES_FIELD + ' = '):
                output[s.LOCK_TOTAL_SIZE_BYTES_FIELD] = int(re.findall('^' + s.LOCK_TOTAL_SIZE_BYTES_FIELD + ' = (.*)', line)[0])

        lock.close()
        return output


def is_locked_by_another_user(base_file: Union[bytes, str], this_user: str) -> bool:
    if os.path.exists(base_file + s.LOCK_SUFFIX) is False:
        return False

    with open(base_file + s.LOCK_SUFFIX, 'r') as lock:
        for line in lock.readlines():
            if line.startswith('user = '):
                if line.endswith(this_user):
                    lock.close()
                    return False
                else:
                    lock.close()
                    return True

        lock.close()
        return False


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
                          require_geom: bool = True,
                          file_extension: str = 'jpg',
                          file_search_re: Pattern = '.*',
                          **kwargs) -> List[str]:
    """A method to allow for recursively finding all files (including their absolute path on the local machine in
    order. This method also accepts an optional regular expression to match file names to and/or a specific file
    extension for the purpose of only getting specific file types.

    :param root_path: The path to begin searching recursively for matching files in
    :param unix_sep: Whether to replace all '\' with a '/' in the file paths on Windows
    :param require_geom: Whether or not to return only files with a .geom file associated with them
    :param file_extension: The file extension required to be included in the returned list
    :param file_search_re: The file name (including the extension) to be searched for as a regular expression
    :return: A list of files with their relative path
    """

    # Enable debugging flag (True = output debug statements, False = don't output debug statements)
    debug: bool = (kwargs['debug'] if 'debug' in kwargs else s.DEFAULT_DEBUG)

    # Enable verbosity (0 = only errors, 1 = low, 2 = medium, 3 = high)
    verbosity: int = (kwargs['verbosity'] if 'verbosity' in kwargs else s.DEFAULT_VERBOSITY)

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
