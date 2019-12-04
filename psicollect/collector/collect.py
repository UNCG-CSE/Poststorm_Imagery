#!/usr/bin/env python3

import argparse
import getpass
import os
import time
from datetime import datetime
from math import floor
from typing import List, Union

from requests.exceptions import RequestException

from psicollect.collector.archive import Archive
from psicollect.collector.connection_handler import ConnectionHandler
from psicollect.collector.locking import get_lock_info, is_locked_by_another_user
from psicollect.collector.storm import Storm
from psicollect.common import h, s

DATA_PATH: Union[bytes, str] = os.path.abspath(s.DATA_PATH)

################################################
# Define command-line parameters and arguments #
################################################

parser = argparse.ArgumentParser(prog=(s.ROOT_CMD + ' collect'))

parser.add_argument('--storm', '-s', default='.*',
                    help='Search all storms for a specific term or match a regular expression. '
                         'Search applies to storm title (including prefixes like "Hurricane") '
                         'as well as the year the storm occurred. Defaults to ALL storms (%(default)s).')

parser.add_argument('--archive', '-a', default='.*',
                    help='Search archive files for a specific term or match a regular expression. '
                         'Search applies to the date string listed on the website (format varies based on storm) if '
                         'found as well as the file name (excluding the extension) and the label (usually "TIF" or '
                         '"RAW JPEG". Defaults to ALL archive files (%(default)s).')

parser.add_argument('--path', '-p', default=s.ARCHIVE_CACHE_PATH,
                    help='The path on your system to download the archive files to (Default: %(default)s).')

parser.add_argument('--user', '-u', default=getpass.getuser(),
                    help='The current user downloading the file (Default: %(default)s).')

parser.add_argument('--download', '-d', action='store_true',
                    help='If included, the program will automatically download all files found, sequentially '
                         '(Default: %(default)s).')

parser.add_argument('--no_status', '-n', action='store_true',
                    help='If included, the program will generate no status report (useful for downloading files '
                         'immediately, without waiting on a report to print) (Default: %(default)s).')

parser.add_argument('--overwrite', '-o', action='store_true',
                    help='If included, the program will overwrite any existing archive files found in the directory by '
                         'the same name (Default: %(default)s).')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = parser.parse_args()

# Clean up path input and validate it
DOWNLOAD_PATH = h.validate_and_expand_path(OPTIONS.path)

c = ConnectionHandler()

storms: List[Storm] = c.get_storm_list(OPTIONS.storm)

# Only display status report if user requests it, otherwise just start downloads
if OPTIONS.no_status is False:

    storm_number: int = 1  # Displayed number associates with storm list
    stat_total_archive_size: int = 0  # Running total of bytes on website
    stat_total_archive_downloaded: int = 0  # Running total of bytes downloaded (all local archive files)

    ############################################
    # Print out a report of what is downloaded #
    ############################################

    print('Download Status Report (' + datetime.now().strftime(s.FORMAT_TIME) + ') <-s ' + OPTIONS.storm +
          ' -t ' + OPTIONS.archive + ' -p ' + OPTIONS.path + '>\n')

    for storm in storms:
        stat_storm_archive_size: int = 0  # Running total of bytes downloaded (by storm)
        stat_storm_archive_downloaded: int = 0  # Running total of bytes downloaded (by storm)
        archive_list: List[Archive] = storm.get_archive_list(OPTIONS.archive)  # All archives for each storm

        # Output storm number, name, and year
        print(str(storm_number) + '.  \t' + str(storm))

        # Display archive file statistics if any archives are found
        if len(archive_list) > 0:
            for archive in archive_list:

                # The path of the archive file including the file suffix
                archive_file_path = os.path.join(os.path.join(DOWNLOAD_PATH, storm.storm_id.title()),
                                                 str(archive.name) + archive.get_ext())

                total_size: int or None = None  # Size of the archive file in bytes

                # Create an appending string to print statuses next to archive info
                exists_str: str = ''

                ###############################################
                # The fully downloaded file is being uploaded #
                ###############################################

                if os.path.exists(archive_file_path + s.LOCK_SUFFIX):

                    lock_info = get_lock_info(base_file=archive_file_path)
                    user: str = lock_info['user']
                    total_size = lock_info[s.LOCK_TOTAL_SIZE_BYTES_FIELD]

                    # Resort to querying the website if the total size cannot be determined locally
                    if type(total_size) is not int:
                        total_size = archive.get_file_size_origin()

                    if user == OPTIONS.user:
                        exists_str += 'Fully downloaded: ' + h.to_readable_bytes(total_size)
                    else:
                        exists_str += 'Fully downloaded (' + user + '): ' + h.to_readable_bytes(total_size)

                    if type(total_size) is int:
                        stat_total_archive_downloaded += total_size
                        stat_storm_archive_downloaded += total_size

                #########################################
                # The fully downloaded file is uploaded #
                #########################################

                elif os.path.exists(archive_file_path):
                    total_size = os.path.getsize(archive_file_path)
                    exists_str += 'Fully downloaded: ' + h.to_readable_bytes(total_size)

                    stat_total_archive_downloaded += total_size
                    stat_storm_archive_downloaded += total_size

                ####################################################################
                # A download for the archive file has been started by another user #
                ####################################################################

                elif os.path.exists(archive_file_path + s.PART_SUFFIX + s.LOCK_SUFFIX):

                    # Get the status of the file being downloaded elsewhere
                    lock_info = get_lock_info(base_file=archive_file_path + s.PART_SUFFIX)

                    last_modified = os.path.getmtime(archive_file_path + s.PART_SUFFIX + s.LOCK_SUFFIX)
                    total_size = lock_info[s.LOCK_TOTAL_SIZE_BYTES_FIELD]  # The number of total bytes to download
                    partial_size: int = lock_info[s.LOCK_PART_SIZE_BYTES_FIELD]  # The # of bytes downloaded so far
                    user: str = lock_info['user']  # The account that started the download (created the lock)

                    """Add information about who initiated the lock, how much is downloaded so far,
                    and when the lock information was last updated (does not update immediately)"""

                    exists_str += 'Partially downloaded (' + user + '): ' + h.to_readable_bytes(partial_size) + \
                                  '  ... Last Update: ' + datetime.fromtimestamp(last_modified).strftime(s.FORMAT_TIME)

                    if type(partial_size) is int:
                        stat_total_archive_downloaded += partial_size
                        stat_storm_archive_downloaded += partial_size

                #################################################
                # Part file exists without any lock association #
                #################################################

                elif os.path.exists(archive_file_path + s.PART_SUFFIX):
                    exists_str += 'Partially downloaded: ' + \
                                  h.to_readable_bytes(os.path.getsize(archive_file_path + s.PART_SUFFIX))

                    stat_total_archive_downloaded += os.path.getsize(archive_file_path + s.PART_SUFFIX)
                    stat_storm_archive_downloaded += os.path.getsize(archive_file_path + s.PART_SUFFIX)

                ###################################################################
                # No fully or partially downloaded file exists or has a lock file #
                ###################################################################

                else:
                    exists_str += 'Not downloaded.'

                print('\t-', archive, ' ...', h.to_readable_bytes(archive.get_file_size_origin()),
                      ' ...', exists_str)

                # Resort to querying the website if the total size cannot be determined locally
                if type(total_size) is not int:
                    total_size = archive.get_file_size_origin()

                stat_total_archive_size += total_size
                stat_storm_archive_size += total_size

            print('\tTotal:', h.to_readable_bytes(stat_storm_archive_downloaded), '/',
                  h.to_readable_bytes(stat_storm_archive_size),
                  ' (' + str(floor((stat_storm_archive_downloaded / stat_storm_archive_size) * 100)) + '%)')

        else:
            if storm.storm_id == 'redriver':
                # North Dakota Flooding (2011) does not provide an archive, only listed with "Contact for download info"
                print('\t' * 2 + '<No archive provided. Contact NOAA for questions>')
            else:
                print('\t' * 2 + '<No archive files detected>')

        print()
        storm_number += 1

    if stat_total_archive_size > 0:
        print('Total:', h.to_readable_bytes(stat_total_archive_downloaded), '/',
              h.to_readable_bytes(stat_total_archive_size),
              ' (' + str(floor((stat_total_archive_downloaded / stat_total_archive_size) * 100)) + '%)')

################################################
# Start the actual collection of archive files #
################################################

if OPTIONS.download:
    for storm in storms:
        for archive in storm.get_archive_list(OPTIONS.archive):
            download_incomplete: bool = True  # Turns to 'False' when the file is downloaded successfully

            # Save the archive to a directory based on the storm's ID (normalize the path to avoid errors)
            save_path: Union[bytes, str] = os.path.join(DOWNLOAD_PATH, storm.storm_id.title())

            # Repeatedly try to download the archive until it completes successfully
            while download_incomplete:
                try:
                    lock_info_part = get_lock_info(
                        base_file=os.path.join(save_path, str(archive.name) + archive.get_ext() + s.PART_SUFFIX))

                    if OPTIONS.overwrite is False and is_locked_by_another_user(
                            base_file=str(archive.name) + archive.get_ext(), this_user=OPTIONS.user):

                        print('Another user has fully downloaded ' + archive.name + archive.get_ext() +
                              '!  ... Skipping')
                        download_incomplete = False

                    elif OPTIONS.overwrite or lock_info_part['user'] is None or OPTIONS.user == lock_info_part['user']:

                        archive.download_url(output_dir=save_path, user=OPTIONS.user, overwrite=OPTIONS.overwrite)
                        download_incomplete = False

                    else:
                        print('Another user is in the process of downloading ' + archive.name + archive.get_ext() +
                              '!  ... Skipping')
                        download_incomplete = False

                except ConnectionError as e:
                    h.print_error('The download ran into a connection error: ' + str(e))
                except RequestException as e:
                    h.print_error('Something went wrong with reading the data transmitted. Error: ' + str(e))

                if download_incomplete:
                    h.print_error('Will retry download in 10 seconds...')
                    time.sleep(10)
