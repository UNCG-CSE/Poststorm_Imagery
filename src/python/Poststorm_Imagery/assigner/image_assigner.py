import random
from os import path
from typing import List, Dict, Union

import pandas as pd

from src.python.Poststorm_Imagery import h, s
from src.python.Poststorm_Imagery.assigner.image_ref import Image

# The maximum amount of times an image can be skipped and remain in the pending queue
MAX_ALLOWED_SKIPS: int = 1

# Make the randomization of images shown deterministically random for testing purposes (set to None to disable)
RANDOM_SEED: Union[int, str, bytes, bytearray, None] = 405


class ImageAssigner:
    """
    Creating an instance of the ImageAssigner class allows for storing all the relevant information related to
    tagging images and processing their data. This class is mainly meant to be used in conjunction with a web-server
    that has validation techniques built in. It is **not** designed to be run client-side as there is no validation of
    identity (user ID is passed as a parameter in most functions).

    This class assumes that there exists a CSV file called `catalog.csv` at the specified scope_path and that the CSV
    file contains a column with a header named `file` that contains the relative paths of each image to be queued for
    tagging (in the scope of the directory containing the catalog.csv).
    """

    # For this class, use queues instead of lists for the sake of implementing into an asynchronous environment due to
    # the Queue object's ability to enforce blocking.

    random.seed(a=RANDOM_SEED)

    # storm_id: str  # The id of the storm (e.g. 'dorian' or 'florence')
    # archive_id: str  # The id of the archive (e.g. '20180919a_jpgs')
    debug: bool = False
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
        self.debug: bool = (kwargs['debug'] if 'debug' in kwargs else s.DEFAULT_DEBUG)

        # Enable verbosity (0 = only errors, 1 = low, 2 = medium, 3 = high)
        verbosity: int = (kwargs['verbosity'] if 'verbosity' in kwargs else s.DEFAULT_VERBOSITY)

        self.scope_path = h.validate_and_expand_path(scope_path)

        self.catalog_path = path.join(self.scope_path, s.CATALOG_FILE_NAME + '.csv')

        if path.isfile(self.catalog_path) is False:
            raise CatalogNotFoundException

        try:
            if small_path is not None and path.exists(h.validate_and_expand_path(small_path)):
                self.small_path = h.validate_and_expand_path(small_path)
            else:
                self.small_path = None
        except OSError:
            self.small_path = None

        # Add each image into the queue
        for image in self._image_list_from_csv():
            self.pending_images_queue.append(image)
            if self.debug and verbosity >= 2:
                print('Loaded %s from the %s.csv file' % (str(image), s.CATALOG_FILE_NAME))

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
            image_list.append(Image(original_size_path=f[0],
                                    small_size_path=f[0]))

        # TODO: Should probably ensure that each image exists and has a smaller version and possibly create a smaller
        #  image if it doesn't exist.
        return random.sample(image_list, k=len(image_list))

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
                path.join(self.scope_path, self.current_image[user_id].original_size_path))
        else:
            return h.validate_and_expand_path(
                path.join(self.scope_path, self.current_image[user_id].small_size_path))

    def get_current_image(self, user_id: str) -> Image:
        """
        Get the Image object that contains information about the specified user's current image.

        :param user_id: The user to get the current image of
        :return: The user's current image as an object
        """

        # If the user has no current image, assign them one from the pending queue
        if user_id not in self.current_image.keys():
            self.current_image[user_id] = self._get_next_suitable_image(user_id=user_id)

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
                path.join(self.scope_path, self.get_next_image(user_id=user_id, skip=skip).original_size_path))
        else:
            return h.validate_and_expand_path(
                path.join(self.scope_path, self.get_next_image(user_id=user_id, skip=skip).small_size_path))

    def get_next_image(self, user_id: str, skip: bool = False) -> Image:
        """
        Get the Image object that contains information about the specified user's next suitable image in the pending
        queue. This function will essentially take the next element from the pending queue and assign it to the
        specified user. No other users will be able to tag the image until this person either skips it (and is sent to
        the pending queue) or it is tagged and multiple people are required to tag each image.

        :param user_id: The user to get the next suitable image of
        :param skip: Whether (True) or not (False) to flag the user's previous image (current image before execution) as
        being skipped by that user. This will happen automatically if the user doesn't apply any flags to the image.
        :return: The user's next suitable image as an object
        """

        # If the user has no current image, assign them one from the pending queue and finish
        if user_id not in self.current_image.keys():
            self.current_image[user_id] = self._get_next_suitable_image(user_id=user_id)
            return self.current_image[user_id]

        if (not skip) and (user_id in self.current_image[user_id].taggers.keys()) \
                and len(self.current_image[user_id].taggers[user_id].keys()) > 0:
            self._user_done_tagging_current_image(user_id=user_id)
        else:
            self._user_skip_tagging_current_image(user_id=user_id)

        self.current_image[user_id] = self._get_next_suitable_image(user_id=user_id)

        return self.current_image[user_id]

    def _get_next_suitable_image(self, user_id: str) -> Image:
        next_image: Image = self.pending_images_queue.pop()

        if user_id in (next_image.skippers or next_image.taggers.keys()):
            if self.debug:
                print('User has already processed %s (tagged or skipped)' % next_image.original_size_path)

            # Recursively search until an image that has not been tagged or skipped by this user is found
            next_next_image = self._get_next_suitable_image(user_id=user_id)
            self.pending_images_queue.append(next_image)

            return next_next_image
        else:
            return next_image

    def _user_done_tagging_current_image(self, user_id: str):
        self.finished_tagged_queue.append(self.current_image[user_id])

    def _user_skip_tagging_current_image(self, user_id: str):

        self.current_image[user_id].skippers.add(user_id)

        if len(self.current_image[user_id].skippers) > MAX_ALLOWED_SKIPS:
            self.max_skipped_queue.append(self.current_image[user_id])
        else:
            self.pending_images_queue.append(self.current_image[user_id])

    def save(self):
        """
        Force inclusion of important objects regardless of copy depth of pickle function. This should only be used
        when the object won't be modified anymore and is about to be saved as a pickle.

        :return: The object with copies of un-included objects that are normally excluded when creating a shallow copy
        """

        # Ensure that data for each image is saved
        for i in range(len(self.pending_images_queue)):
            self.pending_images_queue[i] = self.pending_images_queue[i].save()

        # Save a copy of the queues when creating a pickle (without this, the queues will not save in the pickle)
        self.pending_images_queue = self.pending_images_queue.copy()
        self.finished_tagged_queue = self.finished_tagged_queue.copy()
        self.max_skipped_queue = self.max_skipped_queue.copy()
        self.current_image = self.current_image.copy()
        return self


class CatalogNotFoundException(IOError):
    def __init__(self):
        Exception.__init__(self, 'The catalog file was not found!')
