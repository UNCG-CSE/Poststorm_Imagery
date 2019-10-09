from typing import List, Dict, Union

from Poststorm_Imagery.assigner.user_ref import User


class Image:

    original_size_path: Union[bytes, str]  # The relative path from the catalog.csv for the full size image
    small_size_path: Union[bytes, str]  # The relative path from the catalog.csv for the resized version of the image

    skip_count: int  # The number of times this image has been skipped
    skippers: List[str]  # The number of times this image has been skipped

    tagged_times: int  # The number of unique people that have tagged this image
    taggers: List[User]  # The people who have tagged this image

    def __init__(self, original_size_path: Union[bytes, str], small_size_path: Union[bytes, str]):
        self.original_size_path = original_size_path
        self.small_size_path = small_size_path

