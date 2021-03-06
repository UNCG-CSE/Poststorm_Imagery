import operator
import re
from copy import deepcopy
from datetime import datetime
from os import path
from typing import Dict, Union, Set

from psic.common import h
from psic.resizer.generate import ResizeImages


def _cast_valid_types(content: Union[str, int, bool]) -> Union[str, bool, int]:
    """
    Cast an input that explicitly reads "true" or "false" (case-insensitive) as a boolean type and cast all strings
    of only digits as an integer type. This function does nothing and returns the same value if the input is not a
    string.

    :param content: The string of content to parse out compatible types for
    :return: The value casted as the type detected
    """
    if type(content) == str:

        # Check if the response matches a boolean's text (must be explicit to prevent coercion of ints like '1' -> True)
        if content.lower() == ('true' or 'false'):
            content = bool(content)

        # Check if the response is an integer and only an integer (explicitly define match to avoid type coercion)
        elif re.fullmatch('\\d+', content):
            content = int(content)

    return content


class Image:

    rel_path: str  # The relative path from the catalog.csv for the full size image

    skippers: Set[str] = None  # The number of times this image has been skipped

    # People who have tagged this image and their tags: taggers[user_id] = {'tag_id': 'value'}
    taggers: Dict[str, Dict] = None

    # The final results: final_tags[tag_id] = value
    final_tags: dict or None = None

    # Some statistical variables: stats_<stat_name>[user_id] = value
    stats_tagging_start: Dict[str, float] = None  # The timestamp of the time the user started tagging
    stats_tagging_stop: Dict[str, float] = None  # The timestamp of the time the user finished tagging / skipped
    stats_tag_elapsed_session: Dict[str, float] = None  # The time in seconds for the final session that the user took
    # to tag an image
    stats_tag_elapsed_assigned: Dict[str, float] = None  # The time between being assigned the image and finishing tagging
    # in seconds

    def mark_tagging_start(self, user_id: str):
        if self.stats_tagging_start is None:
            self.stats_tagging_start = dict()
        self.stats_tagging_start[user_id]: float = datetime.now().timestamp()

    def mark_tagging_stop(self, user_id: str):
        if self.stats_tagging_stop is None:
            self.stats_tagging_stop = dict()
        self.stats_tagging_stop[user_id]: float = datetime.now().timestamp()

        # Save the elapsed time of the tagging session in seconds
        self.set_stats_tag_elapsed_assigned(user_id=user_id)

    def set_stats_tag_elapsed_session(self, user_id: str, session_seconds: float):
        if self.stats_tag_elapsed_session is None:
            self.stats_tag_elapsed_session = dict()
        self.stats_tag_elapsed_session[user_id]: float = session_seconds

    def set_stats_tag_elapsed_assigned(self, user_id: str):
        if self.stats_tag_elapsed_assigned is None:
            self.stats_tag_elapsed_assigned = dict()
        self.stats_tag_elapsed_assigned[user_id]: float = self.stats_tagging_stop[user_id] - self.stats_tagging_start[user_id]

    def __init__(self, rel_path: str):
        self.rel_path = rel_path

    def __str__(self):
        return self.rel_path

    def get_rel_path(self) -> str:
        """Simply get the relative path of the image.

        :return: The relative path (e.g. '20180919a_jpgs/jpg/C3240590.jpg')
        """
        return self.rel_path

    def get_tags(self, user_id: str) -> dict:
        """Simply get a set of users' ids who have tagged this image.

        :return: The people (by id) who have tagged this image
        """
        if self.taggers[user_id] is None:
            return dict()

        return self.taggers[user_id]

    def get_taggers(self) -> Set:
        """Simply get a set of users' ids who have tagged this image.

        :return: The people (by id) who have tagged this image
        """
        if self.taggers is None:
            return set()

        return set(self.taggers.keys())

    def get_skippers(self) -> Set:
        """Simply get a set of users' ids who have skipped tagging this image.

        :return: The people (by id) who have skipped this image
        """
        if self.skippers is None:
            return set()

        return self.skippers

    def add_skipper(self, user_id: str) -> None:
        """
        Add a user to the set of skippers for this image.

        :param user_id: The user to add as a skipper
        """
        if self.skippers is None:
            self.skippers = set()

        self.skippers.add(user_id)

    def add_tag(self, user_id: str, tag: str, content: str) -> None:
        """
        Add a tag to the image under a specific user's name. If the tag already exists either with the same value or
        a different value, automatically update it with the new value.

        :param user_id: The user to add the tag under
        :param tag: The tag id or name to use
        :param content: The value of the tag (e.g. a string or True/False)
        """

        # Make sure this key exists before attempting to access it
        if self.taggers is None:
            self.taggers = dict()
        if user_id not in self.get_taggers():
            self.taggers[user_id] = dict()

        # If a valid type is found in the string, cast as either bool or int, otherwise keep as a string
        if 'note' not in tag:
            content = _cast_valid_types(content=content)

        self.taggers[user_id][tag]: Union[str, bool, int] = content

    def remove_tag(self, user_id: str, tag: str) -> None:
        """
        Remove a tag from the image under a specific user's name. This will add an entry in the taggers dictionary,
        though it may be empty as a result of removing a tag if it was the only tag remaining.

        :param user_id: The user to remove the tag from under
        :param tag: The tag id or name to use
        """

        # Make sure this key exists before attempting to access it
        if user_id not in self.get_taggers():
            self.taggers[user_id] = dict()

        self.taggers[user_id][tag] = None

    def update_tag(self, user_id: str, tag: str, content: str) -> None:
        """
        Same as the add_tag function. See the add_tag function.

        :param user_id: The user to add the tag under
        :param tag: The tag id or name to use
        :param content: The value of the tag (e.g. a string or True/False)
        """
        self.add_tag(user_id=user_id, tag=tag, content=content)

    def save(self):
        """
        Force inclusion of important objects regardless of copy depth of pickle function. This should only be used
        when the object won't be modified anymore and is about to be saved as a pickle.

        :return: The object with copies of un-included objects that are normally excluded when creating a shallow copy
        """

        # Save a copy of the dictionaries when creating a pickle (without this, the dicts will not save in the pickle)
        if self.skippers is not None:
            self.skippers = self.skippers.copy()
        if self.taggers is not None:
            self.taggers = self.taggers.copy()
        if self.final_tags is not None:
            self.final_tags = self.final_tags.copy()
        if self.stats_tagging_start is not None:
            self.stats_tagging_start = self.stats_tagging_start.copy()
        if self.stats_tagging_stop is not None:
            self.stats_tagging_stop = self.stats_tagging_stop.copy()
        if self.stats_tag_elapsed_session is not None:
            self.stats_tag_elapsed_session = self.stats_tag_elapsed_session.copy()
        if self.stats_tag_elapsed_assigned is not None:
            self.stats_tag_elapsed_assigned = self.stats_tag_elapsed_assigned.copy()
        return self

    def expanded(self, scope_path: Union[str, bytes], small_path: Union[str, bytes]):
        """
        This function allows for making a copy of the object that includes absolute paths (starting all the way from
        root or the file's drive letter all the way to to the file name including the file type suffix. This is
        useful for the runner in order to pass the context that these Python scripts are running in to the program
        running them through the JSON API.

        :param scope_path: The path to the `full size` image data directory
        :param small_path: The path to the `small` image data directory
        :return: A copy of the Image object that has all path variables expanded to the absolute path of the scope path
        specified
        """
        expanded_copy = deepcopy(x=self)
        expanded_copy.original_size_path = h.validate_and_expand_path(path.join(scope_path, self.rel_path))
        expanded_copy.small_size_path = h.validate_and_expand_path(path.join(small_path, self.rel_path))

        if not (path.exists(expanded_copy.small_size_path) and path.isfile(expanded_copy.small_size_path)
                and path.getsize(expanded_copy.small_size_path) > 1000):
            # If there is no resized version of the image or it might be corrupted

            # Try to resize the image on the fly
            if not ResizeImages.resize_image_at_path(original_path=expanded_copy.original_size_path,
                                                     small_path=expanded_copy.small_size_path,
                                                     scale=0.15):
                # If the image cannot be resized

                expanded_copy.small_size_path = expanded_copy.original_size_path

            elif not (path.exists(expanded_copy.small_size_path)
                      and path.isfile(expanded_copy.small_size_path)
                      and path.getsize(expanded_copy.small_size_path) > 1000):
                # If the small version of the image is still missing or corrupted

                expanded_copy.small_size_path = expanded_copy.original_size_path

        return expanded_copy

    def _sum_tag_values_by_users(self) -> Dict[str, Dict[str, int]]:
        """
        Get a dictionary of tags and a count of how many times users who have tagged the image tagged it with a
        specific value, grouping them by the value they tagged it with. Note that this ignores tags where the value
        is a string, to ignore extra comments and other non-categorical data.

        :return: A dictionary of dictionaries containing the tag's name as the first key, followed by the inner
        dictionary containing the values for that tag and the number of times a user chose that value for the
        specific tag
        """

        tag_totals: Dict[str, Dict[str, int]] = dict()  # tag_totals[tag][value] = <number of user_ids>

        # Create a dictionary that contains all the image's tags and values as well as a count of how many people
        # tagged the image with the same values.

        for user_id in self.get_taggers():
            for tag, value in self.taggers[user_id].items():
                if type(value) is not str:

                    if tag not in tag_totals.keys():
                        tag_totals[tag] = dict()

                    if str(value) not in tag_totals[tag]:
                        tag_totals[tag][str(value)] = 1
                    else:
                        tag_totals[tag][str(value)] += 1

        return tag_totals

    def all_user_tags_equal(self) -> bool:
        """
        Compare all the current tags for an image and see if there is a consensus on what tags the images should
        have. This function will only compare values whose types are not strings. This is to avoid comparing tags
        that contain text like the additional notes section that will ultimately vary by user tagging it.

        :return: Whether (True) or not (False) all users' non-string tags have equal values
        :except NotEnoughTaggersError: The number of current taggers for this image is less than 2
        :except UsersHaveDifferentTagsError: There is an issue with saving user's tags (incomplete or inconsistent)
        """

        # Make sure there are at least 2 sets of tags to compare (function should not be called otherwise)
        if len(self.get_taggers()) < 2:
            # raise NotEnoughTaggersError
            return True

        # Total up all the values for each tag grouped by user's id
        tag_totals: Dict[str, Dict[str, int]] = self._sum_tag_values_by_users()

        for tag in tag_totals:

            if len(tag_totals[tag].keys()) > 1:
                # If there are users with different responses for a non-string tag
                return False

            agreed_upon_value = list(tag_totals[tag].keys())[0]
            if tag_totals[tag][agreed_upon_value] != len(self.get_taggers()):
                # If one user has non-string tags added that the other doesn't
                # raise UsersHaveDifferentTagsError
                return False

        # All tags have exactly one value for each tag name
        return True

    def get_best_tags(self) -> Dict[str, Union[bool, int, str]] or None:
        """
        This function allows you to get the tags that have the most user's opinions on tags in common. If there is a
        clear winner for each tag, then this function returns the set of winning tags. If there is any ambiguity in
        which tag should be chosen (i.e. all people who tagged the image chose different tags), then the function
        will return None. In the case of None, the image should probably have an additional person tag it then
        re-checked to ensure there is a majority for one value for each tag.

        :return: A dictionary of tags as keys and their values as booleans, integers, or strings with no reference to
        the original users who tagged them as such. If there is some ambiguity, it returns None.
        """

        tags_flattened: Dict[str, Union[bool, int, str]] = dict()  # tags_flattened[tag] = <value>

        # Create a dictionary that contains all the image's final tags and values.

        if self.all_user_tags_equal():
            first_user = list(self.get_taggers())[0]
            for tag, value in self.taggers[first_user].items():
                if type(value) is not str:
                    # Add all non-string tags to the result of tags found
                    tags_flattened[tag] = value

        else:
            # tag_totals[tag][value] = <number of user_ids>
            tag_totals: Dict[str, Dict[str, int]] = self._sum_tag_values_by_users()

            for tag in tag_totals:

                all_max_value_names: Set[str] = set()

                # Get the first key of the value name with the most occurrences
                max_value_name = max(tag_totals[tag].items(), key=operator.itemgetter(1))[0]
                for value_name, count in tag_totals[tag].items():
                    if count == tag_totals[tag][max_value_name]:

                        # Make a set of all tag values that have equally high amount of same values for a tag
                        all_max_value_names.add(value_name)

                if len(all_max_value_names) == 1:
                    # There exists only one value for a tag that has the most votes (i.e. 2 of 3 people agree)

                    if 'note' not in tag:
                        tags_flattened[tag] = _cast_valid_types(content=list(all_max_value_names)[0])

                else:
                    # There is no clear winner for this tag
                    return None

        return tags_flattened

    def finalize_tags(self):
        """Calculate the best tags then set the final tags variable"""
        self.final_tags = self.get_best_tags()


class NotEnoughTaggersError(ValueError):
    def __init__(self):
        Exception.__init__(self, 'Tried to compare taggers\' tags when there were less than 2!')


class UsersHaveDifferentTagsError(ValueError):
    def __init__(self):
        Exception.__init__(self, 'One or more users has missing values for tags even though their submission was '
                                 'considered complete! This is likely due to an error in the front-end submission.')
