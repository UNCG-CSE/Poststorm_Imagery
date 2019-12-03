import re
from os import path
from typing import List, Tuple

from psicollect.collector.archive import Archive
from psicollect.collector.connection_handler import get_http_response
# Matches archive files for most (if not all) formats
from psicollect.collector.response_getter import get_full_content_length

URL_STORMS_REGEX_PATTERN_ARCHIVE_GENERAL = re.compile("[\"\'=]\\s*(https?[^\"\'=]+\\.(tar|zip))\\s*[\"\'>]",
                                                      re.IGNORECASE)
# Groups: <archive_url>, <archive_type>

# Matches archive files for most (if not all) formats
URL_STORMS_REGEX_PATTERN_ARCHIVE_RELATIVE = re.compile("[\"\'=]\\s*([^\"\'=]+\\.(tar|zip))\\s*[\"\'>]",
                                                       re.IGNORECASE)
# Groups: <archive_url>, <archive_type>


class Storm:
    """An object that stores information about a particular storm"""

    storm_url: str  # The full url to the storm's index.html page
    storm_id: str  # The name given to the storm, located in the url to identify it in the list
    storm_title: str  # The full name of the storm as listed on the NOAA page
    storm_year: int  # The year that the storm occurred

    archive_list: List[Archive] = list()  # A list of all archives associated with the storm (from the index.html)
    archive_list_last_pattern: str = None  # The last regular expression used to create the list of archive files

    def __init__(self, storm_url: str, storm_id: str, storm_title: str, storm_year: str or int):
        """Initializes the object with required information for a storm

        :param storm_url: The url to the index.html of the storm
        :param storm_id: The ID (from URL) of the storm
        :param storm_title: The name (link name) of the storm
        :param storm_year: The year the storm occurred
        """
        self.storm_url = storm_url
        self.storm_id = storm_id
        self.storm_title = storm_title
        self.storm_year = int(storm_year)

    def __str__(self):
        """Prints out the storm title and year in a human readable format"""
        return self.storm_title + '(' + str(self.storm_year) + ')'

    def generate_archive_list(self, search_re: str = '.*'):
        """Generates a list of archive files from the given storm

        :param search_re: A regular expression to search all archive files for
        """

        # Clear all existing archive files
        self.archive_list = list()

        # Remember the search query
        self.archive_list_last_pattern = search_re

        # Make search pattern case-insensitive
        search_re = re.compile(search_re, re.IGNORECASE)

        try:

            ##################################################################
            # Define where the program should look in order to find archives #
            ##################################################################

            r_text: str  # The text in which to search for links to archives
            if self.storm_id == 'apr11_tornado':
                # Specific case for Tuscaloosa, AL Tornado (2011), obtaining info requires querying ArcGIS
                # Just give the permanent archive link
                r_text = '"http://geodesy.noaa.gov/storm_archive/storms/apr11_tornado/jgw_met/all_world.zip"'
            else:
                # Load the storm's index.html
                r_text = get_http_response(self.storm_url).text

                # Older storms have a link to the AddedInfo.HTM with archives listed there
                if len(re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_GENERAL, r_text)) == 0 and self.storm_year < 2010:
                    r_text = get_http_response(path.join(path.split(self.storm_url)[0], 'AddedInfo.HTM')).text

            #########################################
            # Assemble a list of archives available #
            #########################################

            url_list: List[Tuple[str, str]] = list()

            for archive_url, archive_type in re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_RELATIVE, r_text):
                if archive_url.startswith('http'):
                    url_list.append((archive_url, archive_type))
                else:
                    new_url = path.join(path.split(self.storm_url)[0], archive_url)
                    if get_full_content_length(new_url) != 0:
                        url_list.append((new_url, archive_type))

            # Find all storm data by regex parsing of URLs
            for archive_url, archive_type in url_list:

                if re.search(search_re, archive_url) is not None:

                    # Flag will be toggled to True if the current url matches an already accounted for archive
                    flag_exists = False

                    for archive in self.archive_list:
                        if archive.url == archive_url:
                            # If the archive already appears in the list

                            flag_exists = True
                            break

                    if flag_exists is False:
                        self.archive_list.append(Archive(archive_url=archive_url))

        except ConnectionError:  # pragma: no cover
            self.archive_list = list()

    """ DISABLED: Does not cover JPEG files reliably

        # Find all storm data by regex parsing of URLs
        for date, url, type_label in re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_1, self.r.text):

            # Search for the given pattern
            if re.search(search_re, date) or re.search(search_re, url) or re.search(search_re, type_label):
                self.archive_list.append(Archive(url, date, type_label))

        for url, date, type_label in re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_2, self.r.text):

            # Search for the given pattern
            if re.search(search_re, date) or re.search(search_re, url) or re.search(search_re, type_label):
                self.archive_list.append(Archive(url, date, type_label))

        if len(self.archive_list) == 0:
            for url in re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_FINAL, self.r.text):
                self.archive_list.append(Archive(url=url))
    """

    def get_archive_list(self, search_re: str = '.*') -> List[Archive]:
        """Get a list of all archive objects with the associated regular expression

        :param search_re: The regular expression to search for. Applies to archive date, url, and label
        :returns: A list of archive references (information about archives from the website)
        """

        # If the user has already asked for a list with the same search expression (answer is not already known)
        if search_re != self.archive_list_last_pattern:
            # Generate the list of archive files (clear old list if one exists)
            self.generate_archive_list(search_re)

        return self.archive_list
