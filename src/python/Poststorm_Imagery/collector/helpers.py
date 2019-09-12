import os
import re
from typing import Union, Dict


def get_byte_size_readable(byte_count: int) -> str:
    if byte_count < 2 ** 20:  # MiB = 2^20
        return str(round(byte_count / 2 ** 10, 2)) + ' KiBs'
    if byte_count < 2 ** 30:  # GiB = 2^30
        return str(round(byte_count / 2 ** 20, 2)) + ' MiBs'
    else:
        return str(round(byte_count / 2 ** 30, 2)) + ' GiBs'


def update_file_lock(part_file: str or Union[bytes, str], user: str, part_size_byte: None or int = None,
                     total_size_byte: None or int = None):
    lock = open(part_file + '.lock', 'w')
    lock.write('user = ' + user + '\n')
    if part_size_byte is not None:
        lock.writelines('size_bytes = ' + str(part_size_byte) + '\n')
    if total_size_byte is not None:
        lock.writelines('total_size_bytes = ' + str(total_size_byte) + '\n')

    lock.close()


def get_lock_info(part_file: str or Union[bytes, str]) -> Dict:
    if os.path.exists(part_file + '.lock') is False:
        return {'user': None, 'size_bytes': None, 'total_size_bytes': None}

    with open(part_file + '.lock', 'r') as lock:
        output = {'user': None, 'size_bytes': None, 'total_size_bytes': None}
        for line in lock.readlines():
            if line.startswith('user = '):
                output['user'] = str(re.findall('^user = (.*)', line)[0])
            elif line.startswith('size_bytes = '):
                output['size_bytes'] = int(re.findall('^size_bytes = (.*)', line)[0])
            elif line.startswith('total_size_bytes = '):
                output['total_size_bytes'] = int(re.findall('^total_size_bytes = (.*)', line)[0])

        lock.close()
        return output


def is_locked_by_another_user(part_file: str or Union[bytes, str], this_user: str) -> bool:
    if os.path.exists(part_file) is False:
        return False

    with open(part_file + '.lock', 'r') as lock:
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
