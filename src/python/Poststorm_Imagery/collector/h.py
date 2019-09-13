import os
import re
from typing import Union, Dict

from collector import s


def to_readable_bytes(byte_count: int) -> str:

    if type(byte_count) != int:
        return "??? Bytes"

    if byte_count < 2 ** 20:  # MiB = 2^20
        return str(round(byte_count / 2 ** 10, 2)) + ' KiBs'
    if byte_count < 2 ** 30:  # GiB = 2^30
        return str(round(byte_count / 2 ** 20, 2)) + ' MiBs'
    else:
        return str(round(byte_count / 2 ** 30, 2)) + ' GiBs'


def update_file_lock(base_file: str or Union[bytes, str], user: str,
                     total_size_byte: int, part_size_byte: None or int = None):
    lock = open(base_file + s.LOCK_SUFFIX, 'w')
    lock.write('user = ' + user + '\n')
    if part_size_byte is not None:
        lock.writelines(s.LOCK_PART_SIZE_BYTES_FIELD + ' = ' + str(part_size_byte) + '\n')
    if total_size_byte is not None:
        lock.writelines(s.LOCK_TOTAL_SIZE_BYTES_FIELD + ' = ' + str(total_size_byte) + '\n')

    lock.close()


def get_lock_info(base_file: str or Union[bytes, str]) -> Dict:
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


def is_locked_by_another_user(base_file: str or Union[bytes, str], this_user: str) -> bool:
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
