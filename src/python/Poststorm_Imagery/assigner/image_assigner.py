import os

import pandas as pd
from queue import Queue
from typing import List, Dict, Union

from Poststorm_Imagery import h, s
from Poststorm_Imagery.assigner.image_ref import Image

MAX_SKIP_THRESHOLD: int = 2


class ImageAssigner:

    # For this class, use queues instead of lists for the sake of implementing into an asynchronous environment due to
    # the Queue object's ability to enforce blocking.

    storm_id: str  # The id of the storm (e.g. 'dorian' or 'florence')
    archive_id: str  # The id of the archive (e.g. '20180919a_jpgs')
    scope_path: Union[bytes, str]  # The path of where to find the data and catalog.csv
    catalog_path: Union[bytes, str]  # The path to the catalog file
    small_path: Union[bytes, str, None]  # The path to the resized image scope path

    pending_images_queue: Queue[Image] = Queue()  # The queue that stores all images left to tag by their ID
    finished_tagged_queue: Queue[Image] = Queue()  # The queue to store images that have been tagged already
    max_skipped_queue: Queue[Image] = Queue()  # The queue of images that have passed the threshold for max skips

    # Each user's current image once removed from the beginning of the image queue
    current_image: Dict[str, Image] = {}

    def __init__(self, storm_id: str, archive_id: str,
                 scope_path: Union[bytes, str],
                 small_path: Union[bytes, str, None] = None):

        self.storm_id = storm_id
        self.archive_id = archive_id
        self.scope_path = h.validate_and_expand_path(scope_path)

        self.catalog_path = os.path.join(self.scope_path, s.CATALOG_FILE_NAME)

        if os.path.exists(self.catalog_path) is False:
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
            self.pending_images_queue.put(image)
            self.pending_images_queue.task_done()

    def image_list_from_csv(self) -> List[Image]:

        image_list: List[Image] = []

        with pd.read_csv(self.catalog_path, usecols=lambda col_label: col_label in {'file'}) as f:
            image_list.append(Image(original_size_path=f['file'], small_size_path=self.small_path))

        return image_list

    def get_current_image_path(self, user_id: str, full_size: bool = False) -> str:
        if full_size:
            return self.current_image[user_id].original_size_path
        else:
            return self.current_image[user_id].small_size_path

    def get_next_image_path(self, user_id: str, full_size: bool = False) -> str:
        self.current_image[user_id] = self.pending_images_queue.get()
        self.pending_images_queue.task_done()

        if full_size:
            return self.current_image[user_id].original_size_path
        else:
            return self.current_image[user_id].small_size_path

    def get_current_image(self, user_id: str, skip: bool = False) -> Image:

        if (not skip) and len(self.current_image[user_id].tags[user_id]) > 0:
            self.user_done_tagging_current_image(user_id=user_id)
        else:
            self.user_skip_tagging_current_image(user_id=user_id)

        return self.current_image[user_id]

    def get_next_image(self, user_id: str) -> Image:
        self.current_image[user_id] = self.pending_images_queue.get()
        self.pending_images_queue.task_done()

        return self.current_image[user_id]

    def add_tag(self, user_id: str, **kwargs):
        self.current_image[user_id].add_tag(user_id=user_id, **kwargs)

    def user_done_tagging_current_image(self, user_id: str):
        self.finished_tagged_queue.put(self.current_image[user_id])
        self.finished_tagged_queue.task_done()

    def user_skip_tagging_current_image(self, user_id: str):

        self.current_image[user_id].skippers.append(user_id)
        self.current_image[user_id].skip_count += 1

        if self.current_image[user_id].skip_count > MAX_SKIP_THRESHOLD:
            self.max_skipped_queue.put(self.current_image[user_id])
            self.max_skipped_queue.task_done()
        else:
            self.pending_images_queue.put(self.current_image[user_id])
            self.pending_images_queue.task_done()


class CatalogNotFoundException(IOError):
    def __init__(self):
        Exception.__init__(self, 'The catalog file was not found!')
