import os
from typing import Union

from src.python.Poststorm_Imagery.collector import s, h


def generate_index_from_scope(scope_path: Union[str, bytes] = s.DATA_PATH, debug: bool = False) -> None:
    """
    A function to generate an index of all the data in the scope specified. Does not generate statistics, but instead
    allows for listing the data details based off of each file's attributes.
    """

    DOWNLOAD_PATH = h.validate_and_expand_path(scope_path)
