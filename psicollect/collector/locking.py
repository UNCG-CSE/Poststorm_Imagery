import re
from os.path import exists
from typing import Union, TextIO, Dict

from psicollect.common import s


def update_file_lock(base_file: Union[bytes, str], user: str,
                     total_size_byte: int, part_size_byte: None or int = None) -> TextIO:
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

    return lock


def get_lock_info(base_file: Union[bytes, str]) -> Dict:
    """Get the current lock information on a file, returning None for all values not found.  This includes the user
    downloading the file, the total size of the file they're downloading, the amount of the file they already have
    downloaded, and when the former info was last updated (inferred from the modified timestamp of the .lock file).

    :param base_file: The path to the file to read lock info from (not including .lock)
    :return: A dictionary with entries for user, total byte size, and downloaded byte size (`byte_size`)
    """
    if exists(base_file + s.LOCK_SUFFIX) is False:
        return {'user': None, s.LOCK_PART_SIZE_BYTES_FIELD: None, s.LOCK_TOTAL_SIZE_BYTES_FIELD: None}

    with open(base_file + s.LOCK_SUFFIX, 'r') as lock:
        output = {'user': None, s.LOCK_PART_SIZE_BYTES_FIELD: None, s.LOCK_TOTAL_SIZE_BYTES_FIELD: None}

        for line in lock.readlines():

            if line.startswith('user = '):
                output['user'] = str(re.findall('^user = (.*)', line)[0])

            elif line.startswith(s.LOCK_PART_SIZE_BYTES_FIELD + ' = '):
                output[s.LOCK_PART_SIZE_BYTES_FIELD] = \
                    int(re.findall('^' + s.LOCK_PART_SIZE_BYTES_FIELD + ' = (.*)', line)[0])

            elif line.startswith(s.LOCK_TOTAL_SIZE_BYTES_FIELD + ' = '):
                output[s.LOCK_TOTAL_SIZE_BYTES_FIELD] = \
                    int(re.findall('^' + s.LOCK_TOTAL_SIZE_BYTES_FIELD + ' = (.*)', line)[0])

        lock.close()
        return output


def is_locked_by_another_user(base_file: Union[bytes, str], this_user: str) -> bool:
    if exists(base_file + s.LOCK_SUFFIX) is False:
        return False

    with open(base_file + s.LOCK_SUFFIX, 'r') as lock:
        for line in lock.readlines():
            if line.startswith('user = '):
                if line.strip().endswith(this_user):
                    lock.close()
                    return False
                else:
                    lock.close()
                    return True

        lock.close()
        return False
