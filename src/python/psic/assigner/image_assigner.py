import random
from datetime import datetime
from os import path
from typing import List, Dict, Union

import pandas as pd

from psic import s
from psic.assigner.image_ref import Image
from psic.common import h
from psic.cataloging.make_catalog import Cataloging

# The maximum amount of times an image can be skipped and remain in the pending queue
MAX_ALLOWED_SKIPS: int = 1

MINIMUM_TAGGERS_NEEDED: int = 2

# Make the randomization of images shown deterministically random for testing purposes (set to None to disable)
RANDOM_SEED: Union[int, str, bytes, bytearray, None] = 405

MINUTES_BETWEEN_BACKUPS: float = 15


class ImageAssigner:
    """
    Creating an instance of the ImageAssigner class allows for storing all the relevant information related to
    tagging images and processing their data. This class is mainly meant to be used in conjunction with a web-server
    that has validation techniques built in. It is **not** designed to be run client-side as there is no validation of
    identity (user ID is passed as a parameter in most functions).

    This class assumes that there exists a CSV file called `catalog.csv` at the specified scope_path or in the
    project catalog folder specified in s.py and that the CSV file contains a column with a header named `file` that
    contains the relative paths of each image to be queued for tagging (in the scope path provided).
    """

    random.seed(a=RANDOM_SEED)

    # storm_id: str  # The id of the storm (e.g. 'dorian' or 'florence')
    # archive_id: str  # The id of the archive (e.g. '20180919a_jpgs')
    debug: bool
    scope_path: Union[bytes, str]  # The path of where to find the data
    catalog_path: Union[bytes, str]  # The path to the catalog file
    small_path: Union[bytes, str]  # The path to the resized image scope path

    pending_images_queue: List[Image] or None = list()  # The queue that stores all images left to tag by their ID

    finished_tagged_queue: List[Image] or None = list()  # The queue to store images that have been tagged already

    max_skipped_queue: List[Image] or None = list()  # The queue of images that have passed the threshold for max skips

    # Each user's current image once removed from the beginning of the image queue
    current_image: Dict[str, Image] = {}

    last_backup_timestamp: float  # The last time a backup of the assigner state was made

    def __init__(self, scope_path: Union[bytes, str],
                 small_path: Union[bytes, str],
                 debug: bool = s.DEFAULT_DEBUG,
                 verbosity: int = s.DEFAULT_VERBOSITY):

        self.debug = debug

        self.scope_path = h.validate_and_expand_path(scope_path)

        self.catalog_path = Cataloging.find_catalog_path(scope_path=scope_path)

        if path.exists(h.validate_and_expand_path(small_path)):
            self.small_path = h.validate_and_expand_path(small_path)
        else:
            raise OSError('Could not find the path: %s on the local file-system!' % small_path)

        # Add each image into the queue
        for image in self._image_list_from_csv():
            self.pending_images_queue.append(image)
            if self.debug and verbosity >= 2:
                print('Loaded %s from the %s file' % (str(image), self.catalog_path))

        # Set a starting value for the last time the assigner was backed up
        self.last_backup_timestamp = datetime.now().timestamp()

        if self.debug and verbosity >= 1:
            print('Next Pending Image (of %s): %s' % (len(self.pending_images_queue), self.pending_images_queue[0]))

    def _image_list_from_csv(self) -> List[Image]:
        """
        Grab all image information from the catalog and save it to a list. This list is then shuffled before return.

        :return: A shuffled list of all images in the scope of this object.
        """

        image_list: List[Image] = []

        rel_file_paths: list = pd.read_csv(self.catalog_path, usecols=lambda col_label: col_label in {
            'file'}).values.tolist()

        for f in rel_file_paths:
            image_list.append(Image(rel_path=f[0]))

        return random.sample(image_list, k=len(image_list))

    def is_time_for_backup(self, max_minutes=MINUTES_BETWEEN_BACKUPS) -> bool:
        """
        A method to get if it is time for a new backup to be taken. This simply takes the number of minutes specified or
        the default value defined in the class and sees if the time since the last backup exceeds the specified number
        of minutes. This method does not change any values. It only does a comparison.

        :param max_minutes: The max number of minutes to wait in-between backups
        :return: Whether (True) or not (False) it is time for the next backup to occur
        """

        # Calculate the difference between the last backup and now
        return (datetime.now().timestamp() - self.get_last_backup_timestamp()) > (max_minutes * 60)

    def get_last_backup_timestamp(self) -> float:
        return self.last_backup_timestamp

    def mark_last_backup_timestamp(self):
        self.last_backup_timestamp = datetime.now().timestamp()

    def get_current_image_path(self, user_id: str, full_size: bool = False) -> str:
        """
        Simply get the absolute path of the specified user's current image. Returns as just the full path with no
        decorations and no extra characters.

        :param user_id: The user to get the current image path of
        :param full_size: Whether or not to return the path to the full size image (True) or the reduced size image (
        False)
        :return: The absolute path to the image requested
        """
        if full_size:
            return h.validate_and_expand_path(
                path.join(self.scope_path, self.current_image[user_id].rel_path))
        else:
            return h.validate_and_expand_path(
                path.join(self.scope_path, self.current_image[user_id].rel_path))

    def has_a_current_image(self, user_id: str) -> bool:
        """
        Check if the user has an image currently. This can be used to check for cases where the user has not been
        assigned an image yet (i.e. they logged into the dashboard for the first time).

        :return: Whether (True) or not (False) the user currently is assigned an image"""
        return user_id in self.current_image.keys()

    def get_current_image(self, user_id: str, expanded: bool = False) -> Image:
        """
        Get the Image object that contains information about the specified user's current image.

        :param user_id: The user to get the current image of
        :param expanded: Whether (True) or not (False) to return a *copy* of the current image with the path
        variables converted from relative to absolute
        :return: The user's current image as an object
        """

        # If the user has no current image, assign them one from the pending queue

        if user_id not in self.current_image.keys():
            self.get_next_image(user_id=user_id)

        if expanded:
            return self.current_image[user_id].expanded(scope_path=self.scope_path, small_path=self.small_path)
        else:
            return self.current_image[user_id]

    def get_next_image_path(self, user_id: str, full_size: bool = False, skip: bool = False) -> str:
        """
        Simply get the absolute path of the specified user's next suitable image in the pending queue. Returns as just
        the full path with no decorations and no extra characters. This function will essentially take the next
        element from the pending queue and assign it to the specified user. No other users will be able to tag the
        image until this person either skips it (and is sent to the pending queue) or it is tagged and multiple
        people are required to tag each image.

        :param user_id: The user to get the next suitable image's path of
        :param full_size: Whether or not to return the path to the full size image (True) or the reduced size image (
        False)
        :param skip: Whether (True) or not (False) to flag the user's previous image (current image before execution) as
        being skipped by that user. This will happen automatically if the user doesn't apply any flags to the image.
        :return: The absolute path to the image requested
        """
        if full_size:
            return h.validate_and_expand_path(
                path.join(self.scope_path, self.get_next_image(user_id=user_id, skip=skip).rel_path))
        else:
            return h.validate_and_expand_path(
                path.join(self.small_path, self.get_next_image(user_id=user_id, skip=skip).rel_path))

    def get_next_image(self, user_id: str, expanded: bool = False, skip: bool = False) -> Image:
        """
        Get the Image object that contains information about the specified user's next suitable image in the pending
        queue. This function will essentially take the next element from the pending queue and assign it to the
        specified user. No other users will be able to tag the image until this person either skips it (and is sent to
        the pending queue) or it is tagged and multiple people are required to tag each image.

        :param user_id: The user to get the next suitable image of
        :param expanded: Whether (True) or not (False) to return a *copy* of the current image with the path
        variables converted from relative to absolute
        :param skip: Whether (True) or not (False) to flag the user's previous image (current image before execution) as
        being skipped by that user. This will happen automatically if the user doesn't apply any flags to the image.
        :return: The user's next suitable image as an object
        """

        # If the user has no current image, assign them one from the pending queue and finish

        if user_id not in self.current_image.keys():
            self.current_image[user_id] = self._get_next_suitable_image(user_id=user_id)

            # Record that the user started tagging the image
            self.current_image[user_id].mark_tagging_start(user_id=user_id)

            return self.current_image[user_id]

        if (not skip) and (user_id in self.current_image[user_id].get_taggers()) \
                and len(self.current_image[user_id].get_tags(user_id=user_id).keys()) > 0:
            self._user_done_tagging_current_image(user_id=user_id)
        else:
            self._user_skip_tagging_current_image(user_id=user_id)

        # Record that the user stopped tagging the most recent image
        self.current_image[user_id].mark_tagging_stop(user_id=user_id)

        # Set the chosen image as the user's current image
        self.current_image[user_id] = self._get_next_suitable_image(user_id=user_id)

        # Record that the user started tagging the new image
        self.current_image[user_id].mark_tagging_start(user_id=user_id)

        if expanded:
            return self.current_image[user_id].expanded(scope_path=self.scope_path, small_path=self.small_path)
        else:
            return self.current_image[user_id]

    def _get_next_suitable_image(self, user_id: str) -> Image:
        next_image: Image = self.pending_images_queue.pop()

        if (user_id in next_image.get_skippers()) or (user_id in next_image.get_taggers()):
            if self.debug:
                print('User has already processed %s (tagged or skipped)' % next_image.rel_path)

            # Recursively search until an image that has not been tagged or skipped by this user is found
            next_next_image = self._get_next_suitable_image(user_id=user_id)
            self.pending_images_queue.append(next_image)

            return next_next_image
        else:
            return next_image

    def _user_done_tagging_current_image(self, user_id: str):
        if len(self.current_image[user_id].get_taggers()) >= MINIMUM_TAGGERS_NEEDED \
                and self.current_image[user_id].get_best_tags() is not None:
            # If enough people have tagged this image and there's a consensus

            self.current_image[user_id].finalize_tags()

            # Majority of users agree on a tag for this image
            self.finished_tagged_queue.append(self.current_image[user_id])
        else:
            # If image needs more people to tag it
            self.pending_images_queue.append(self.current_image[user_id])

    def _user_skip_tagging_current_image(self, user_id: str):

        self.current_image[user_id].add_skipper(user_id)

        if len(self.current_image[user_id].get_skippers()) > MAX_ALLOWED_SKIPS:
            # If the image has exceeded the allowed number of skips
            self.max_skipped_queue.append(self.current_image[user_id])
        else:
            # If the image can be skipped by at least one more unique user before being moved to the max skipped queue
            self.pending_images_queue.append(self.current_image[user_id])

    def save(self):
        """
        Force inclusion of important objects regardless of copy depth of pickle function. This should only be used
        when the object won't be modified anymore and is about to be saved as a pickle.

        :return: The object with copies of un-included objects that are normally excluded when creating a shallow copy
        """

        for i in range(len(self.pending_images_queue)):
            # Ensure that data for each image is saved
            self.pending_images_queue[i] = self.pending_images_queue[i].save()

        # Save a copy of the queues when creating a pickle (without this, the queues will not save in the pickle)
        self.pending_images_queue = self.pending_images_queue.copy()
        self.finished_tagged_queue = self.finished_tagged_queue.copy()
        self.max_skipped_queue = self.max_skipped_queue.copy()
        self.current_image = self.current_image.copy()
        return self
