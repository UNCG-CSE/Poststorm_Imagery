from typing import Union, List


class Batch:

    scope_path: Union[bytes, str]  # The path of where to find the data and catalog.csv
    small_path: Union[bytes, str]  # The path to the resized image scope path
    operations: List[dict]           # An ordered list of operations to execute

    def __init__(self, scope_path: Union[bytes, str], small_path: Union[bytes, str],
                 operations: List[dict] or None = None):

        if operations is None:
            operations = list()

        self.scope_path = scope_path
        self.small_path = small_path
        self.operations = operations
