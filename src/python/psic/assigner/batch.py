from typing import Union, List

from psic import s


class Batch:

    path: Union[bytes, str]  # The path of where to find the data and catalog.csv
    small_path: Union[bytes, str]  # The path to the resized image scope path
    user_id: str  # The user to perform the operations as
    operations: List[dict]  # An ordered list of operations to execute

    stats_time_elapsed_ms: int or None  # The number of ms elapsed in this user's current / final session

    debug: bool  # True for debug statements

    def __init__(self, path: Union[bytes, str], small_path: Union[bytes, str], stats_time_elapsed_ms: int = None,
                 operations: List[dict] or None = None, debug: bool = s.DEFAULT_DEBUG):

        if operations is None:
            operations = list()

        self.scope_path = path
        self.small_path = small_path
        self.operations = operations
        self.stats_time_elapsed_ms = stats_time_elapsed_ms
        self.debug = debug
