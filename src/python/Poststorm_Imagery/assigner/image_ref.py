from typing import List, Dict, Union, Set


class Image:

    original_size_path: Union[bytes, str]  # The relative path from the catalog.csv for the full size image
    small_size_path: Union[bytes, str]  # The relative path from the catalog.csv for the resized version of the image

    skippers: Set[str] = set()  # The number of times this image has been skipped
    taggers: Dict[str, Dict] = dict()  # People who have tagged this image and their tags: taggers[user_id] = {'tag_id',
    # 'value'}

    def __init__(self, original_size_path: Union[bytes, str], small_size_path: Union[bytes, str]):
        self.original_size_path = original_size_path
        self.small_size_path = small_size_path

    def __str__(self):
        return self.original_size_path

    def add_tag(self, user_id: str, tag: str, content: str):

        # Make sure this key exists before attempting to access it
        if user_id not in self.taggers.keys():
            self.taggers[user_id] = dict()

        self.taggers[user_id][tag] = content

    def remove_tag(self, user_id: str, tag: str):
        self.taggers[user_id][tag] = None

    def update_tag(self, user_id: str, tag: str, content: str):
        self.add_tag(user_id=user_id, tag=tag, content=content)

    def save(self):

        # Save a copy of the dictionaries when creating a pickle (without this, the dicts will not save in the pickle)
        self.skippers = self.skippers.copy()
        self.taggers = self.taggers.copy()
        return self

    def load(self):
        return self
