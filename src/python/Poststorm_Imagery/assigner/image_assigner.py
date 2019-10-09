from queue import Queue
from typing import List, Dict

from Poststorm_Imagery.assigner.image_ref import Image
from Poststorm_Imagery.assigner.user_ref import User

MAX_SKIP_THRESHOLD: int = 2


class ImageAssigner:

    # For this class, use queues instead of lists for the sake of implementing into an asynchronous environment due to
    # the Queue object's ability to enforce blocking.

    storm_id: str  # The id of the storm (e.g. 'dorian' or 'florence')
    archive_id: str  # The id of the archive (e.g. '20180919a_jpgs')

    pending_images_queue: Queue[Image] = Queue()  # The queue that stores all images left to tag by their ID
    finished_tagged_queue: Queue[Image] = {}  # The queue to store images that have been tagged already
    max_skipped_queue: Queue[Image] = Queue()  # The queue of images that have passed the threshold for max skips

    # Each user's current image once removed from the beginning of the image queue
    current_image: Dict[str, Image] = {}

    def __init__(self, storm_id: str, archive_id: str):
        self.storm_id = storm_id
        self.archive_id = archive_id

    def get_current_image(self, user_id: str, full_size: bool = False) -> Image:
        return self.current_image[user_id]

    def get_next_image(self, user_id: str, full_size: bool = False) -> Image:
        self.current_image[user_id] = self.pending_images_queue.get()
        self.pending_images_queue.task_done()

        return self.current_image[user_id]
