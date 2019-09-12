import os
from typing import Union


def get_byte_size_readable(byte_count: int) -> str:
    if byte_count < 2 ** 20:  # MiB = 2^20
        return str(round(byte_count / 2 ** 10, 2)) + ' KiBs'
    if byte_count < 2 ** 30:  # GiB = 2^30
        return str(round(byte_count / 2 ** 20, 2)) + ' MiBs'
    else:
        return str(round(byte_count / 2 ** 30, 2)) + ' GiBs'


def update_file_part_lock(part_file: str or Union[bytes, str], user: str, part_size_byte: None or int = None):
    lock = open(part_file + '.lock', 'w')
    lock.writelines('user = ' + user)
    if part_size_byte is not None:
        lock.writelines('size_bytes = ' + part_size_byte)
    lock.close()


def file_part_is_locked_by_another_user(part_file: str or Union[bytes, str], this_user: str) -> bool:
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
