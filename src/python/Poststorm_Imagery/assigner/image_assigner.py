import os
import random

import pandas as pd
from queue import Queue, LifoQueue
from typing import List, Dict, Union

from Poststorm_Imagery import h, s
from Poststorm_Imagery.assigner.image_ref import Image

# The maximum amount of times an image can be skipped before it is added to the max skipped queue
MAX_SKIP_THRESHOLD: int = 2

# Make the randomization of images shown deterministically random for testing purposes (set to None to disable)
RANDOM_SEED: Union[int, str, bytes, bytearray, None] = 405


class ImageAssigner:

    # For this class, use queues instead of lists for the sake of implementing into an asynchronous environment due to
    # the Queue object's ability to enforce blocking.

    random.seed(a=RANDOM_SEED)

    assigner_cache: str

    # storm_id: str  # The id of the storm (e.g. 'dorian' or 'florence')
    # archive_id: str  # The id of the archive (e.g. '20180919a_jpgs')
    scope_path: Union[bytes, str]  # The path of where to find the data and catalog.csv
    catalog_path: Union[bytes, str]  # The path to the catalog file
    small_path: Union[bytes, str, None]  # The path to the resized image scope path

    pending_images_queue: List[Image] or None = list()  # The queue that stores all images left to tag by their ID

    finished_tagged_queue: List[Image] or None = list()  # The queue to store images that have been tagged already

    max_skipped_queue: List[Image] or None = list()  # The queue of images that have passed the threshold for max skips

    # Each user's current image once removed from the beginning of the image queue
    current_image: Dict[str, Image] = {}

    def __init__(self, scope_path: Union[bytes, str],
                 small_path: Union[bytes, str, None] = None, **kwargs):

        # Enable debugging flag (True = output debug statements, False = don't output debug statements)
        debug: bool = (kwargs['debug'] if 'debug' in kwargs else s.DEFAULT_DEBUG)

        # Enable verbosity (0 = only errors, 1 = low, 2 = medium, 3 = high)
        verbosity: int = (kwargs['verbosity'] if 'verbosity' in kwargs else s.DEFAULT_VERBOSITY)

        self.scope_path = h.validate_and_expand_path(scope_path)

        self.catalog_path = os.path.join(self.scope_path, s.CATALOG_FILE_NAME + '.csv')

        if os.path.isfile(self.catalog_path) is False:
            raise CatalogNotFoundException

        try:
            if small_path is not None and os.path.exists(h.validate_and_expand_path(small_path)):
                self.small_path = h.validate_and_expand_path(small_path)
            else:
                self.small_path = None
        except OSError:
            self.small_path = None

        # Add each image into the queue
        for image in self.image_list_from_csv():
            self.pending_images_queue.append(image)
            if debug and verbosity >= 2:
                print('Loaded %s from the %s.csv file' % (str(image), s.CATALOG_FILE_NAME))

        if debug and verbosity >= 1:
            print('Next Pending Image (of %s): %s' % (len(self.pending_images_queue), self.pending_images_queue[0]))

    def image_list_from_csv(self) -> List[Image]:

        image_list: List[Image] = []

        rel_file_paths: list = pd.read_csv(self.catalog_path, usecols=lambda col_label: col_label in {
            'file'}).values.tolist()

        for f in rel_file_paths:
            image_list.append(Image(original_size_path=os.path.join(self.scope_path, f[0]),
                                    small_size_path=os.path.join(self.small_path, f[0])))

        return random.sample(image_list, k=len(image_list))

    def get_current_image_path(self, user_id: str, full_size: bool = False) -> str:
        if full_size:
            return self.current_image[user_id].original_size_path
        else:
            return self.current_image[user_id].small_size_path

    def get_next_image_path(self, user_id: str, full_size: bool = False, skip: bool = False) -> str:
        if full_size:
            return self.get_next_image(user_id=user_id, skip=skip).original_size_path
        else:
            return self.get_next_image(user_id=user_id, skip=skip).small_size_path

    def get_next_image(self, user_id: str, skip: bool = False) -> Image:

        if (not skip) and len(self.current_image[user_id].taggers[user_id]) > 0:
            self.user_done_tagging_current_image(user_id=user_id)
        else:
            self.user_skip_tagging_current_image(user_id=user_id)

        self.assign_next_image(user_id=user_id)

        return self.current_image[user_id]

    def assign_next_image(self, user_id: str) -> Image:
        next_image: Image = self.pending_images_queue.pop()

        if user_id not in (next_image.skippers and next_image.taggers):
            self.current_image[user_id] = next_image
        else:
            next_next_image = self.get_next_image(user_id=user_id)
            self.pending_images_queue.insert(0, next_image)

            return next_next_image

        return self.current_image[user_id]

    def user_done_tagging_current_image(self, user_id: str):
        self.finished_tagged_queue.append(self.current_image[user_id])

    def user_skip_tagging_current_image(self, user_id: str):

        self.current_image[user_id].skippers.append(user_id)

        if len(self.current_image[user_id].skippers) > MAX_SKIP_THRESHOLD:
            self.max_skipped_queue.append(self.current_image[user_id])
        else:
            self.pending_images_queue.append(self.current_image[user_id])

    def save(self):

        # Save a copy of the queues when creating a pickle (without this, the queues will not save in the pickle)
        self.pending_images_queue = self.pending_images_queue.copy()
        self.finished_tagged_queue = self.finished_tagged_queue.copy()
        self.max_skipped_queue = self.max_skipped_queue.copy()
        return self

    def load(self):
        return self


class CatalogNotFoundException(IOError):
    def __init__(self):
        Exception.__init__(self, 'The catalog file was not found!')
