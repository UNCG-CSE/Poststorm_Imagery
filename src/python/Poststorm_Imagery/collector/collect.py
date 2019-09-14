import argparse
import getpass
import os
import time
from datetime import datetime
from math import floor

from typing import List, Union

from src.python.Poststorm_Imagery.collector import h, s
from src.python.Poststorm_Imagery.collector.ConnectionHandler import ConnectionHandler
from src.python.Poststorm_Imagery.collector.Storm import Storm
from src.python.Poststorm_Imagery.collector.TarRef import TarRef

DATA_PATH: Union[bytes, str] = os.path.abspath(s.DATA_PATH)
TAR_CACHE_PATH: Union[bytes, str] = os.path.join(DATA_PATH, s.TAR_CACHE)

################################################
# Define command-line parameters and arguments #
################################################

parser = argparse.ArgumentParser(prog='collect')

parser.add_argument('--storm', '-s', default='.*',
                    help='Search all storms for a specific term or match a regular expression. '
                         'Search applies to storm title (including prefixes like "Hurricane") '
                         'as well as the year the storm occurred. Defaults to ALL storms (%(default)s).')

parser.add_argument('--tar', '-t', default='.*',
                    help='Search .tar files for a specific term or match a regular expression. '
                         'Search applies to the date string listed on the website (format varies based on storm) if '
                         'found as well as the file name (excluding the .tar) and the label (usually "TIF" or '
                         '"RAW JPEG". Defaults to ALL .tar files (%(default)s).')

parser.add_argument('--path', '-p', default=TAR_CACHE_PATH,
                    help='The path on your system to download the tar files to (Default: %(default)s).')

parser.add_argument('--user', '-u', default=getpass.getuser(),
                    help='The current user downloading the file (Default: %(default)s).')

parser.add_argument('--download', '-d', action='store_true',
                    help='If included, the program will automatically download all files found, sequentially '
                         '(Default: %(default)s).')

parser.add_argument('--no_status', '-n', action='store_true',
                    help='If included, the program will generate no status report (useful for downloading files '
                         'immediately, without waiting on a report to print) (Default: %(default)s).')

parser.add_argument('--overwrite', '-o', action='store_true',
                    help='If included, the program will overwrite any existing .tar files found in the directory by '
                         'the same name (Default: %(default)s).')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = parser.parse_args()

# Convert string to absolute path for uniformity
DOWNLOAD_PATH = os.path.abspath(OPTIONS.path)

# Expand out any path keywords or variables for certain operating system
DOWNLOAD_PATH = os.path.expanduser(os.path.expandvars(DOWNLOAD_PATH))

c = ConnectionHandler()

storms: List[Storm] = c.get_storm_list(OPTIONS.storm)

# Only display status report if user requests it, otherwise just start downloads
if OPTIONS.no_status is False:

    storm_number: int = 1  # Displayed number associates with storm list
    stat_total_tar_size: int = 0  # Running total of bytes on website
    stat_total_tar_downloaded: int = 0  # Running total of bytes downloaded (all local .tar files)

    ############################################
    # Print out a report of what is downloaded #
    ############################################

    print('Download Status Report (' + datetime.now().strftime(s.FORMAT_TIME) + ') <-s ' + OPTIONS.storm +
          ' -t ' + OPTIONS.tar + ' -p ' + OPTIONS.path + '>\n')

    for storm in storms:
        stat_storm_tar_size: int = 0  # Running total of bytes downloaded (by storm)
        stat_storm_tar_downloaded: int = 0  # Running total of bytes downloaded (by storm)
        tar_list: List[TarRef] = storm.get_tar_list(OPTIONS.tar)  # All TarRef for each storm

        # Output storm number, name, and year
        print(str(storm_number) + '.  \t' + str(storm))

        # Display .tar file statistics if any .tar files are found
        if len(tar_list) > 0:
            for tar_file in tar_list:

                # The path of the tar file including the .tar suffix
                tar_file_path = os.path.join(os.path.join(DOWNLOAD_PATH, storm.storm_id.title()),
                                             str(tar_file.tar_file_name) + '.tar')

                total_size: None or int = None  # Size of the .tar file in bytes

                # Create an appending string to print statuses next to .tar info
                exists_str: str = ''

                ###############################################
                # The fully downloaded file is being uploaded #
                ###############################################

                if os.path.exists(tar_file_path + s.LOCK_SUFFIX):

                    lock_info = h.get_lock_info(base_file=tar_file_path)
                    user: str = lock_info['user']
                    total_size = lock_info[s.LOCK_TOTAL_SIZE_BYTES_FIELD]

                    # Resort to querying the website if the total size cannot be determined locally
                    if type(total_size) is not int:
                        total_size = tar_file.get_file_size_origin()

                    if user == OPTIONS.user:
                        exists_str += 'Fully downloaded: ' + h.to_readable_bytes(total_size)
                    else:
                        exists_str += 'Fully downloaded (' + user + '): ' + h.to_readable_bytes(total_size)

                    if type(total_size) is int:
                        stat_total_tar_downloaded += total_size
                        stat_storm_tar_downloaded += total_size

                #########################################
                # The fully downloaded file is uploaded #
                #########################################

                elif os.path.exists(tar_file_path):
                    total_size = os.path.getsize(tar_file_path)
                    exists_str += 'Fully downloaded: ' + h.to_readable_bytes(total_size)

                    stat_total_tar_downloaded += total_size
                    stat_storm_tar_downloaded += total_size

                #################################################################
                # A download for the .tar file has been started by another user #
                #################################################################

                elif os.path.exists(tar_file_path + s.PART_SUFFIX + s.LOCK_SUFFIX):

                    # Get the status of the file being downloaded elsewhere
                    lock_info = h.get_lock_info(base_file=tar_file_path + s.PART_SUFFIX)

                    last_modified = os.path.getmtime(tar_file_path + s.PART_SUFFIX + s.LOCK_SUFFIX)
                    partial_size: int = lock_info[s.LOCK_PART_SIZE_BYTES_FIELD]  # The # of bytes downloaded so far
                    total_size: int = lock_info[s.LOCK_TOTAL_SIZE_BYTES_FIELD]  # The number of total bytes to download
                    user: str = lock_info['user']  # The account that started the download (created the lock)

                    """Add information about who initiated the lock, how much is downloaded so far, 
                    and when the lock information was last updated (does not update immediately)"""

                    exists_str += 'Partially downloaded (' + user + '): ' + h.to_readable_bytes(partial_size) + \
                                  '  ... Last Update: ' + datetime.fromtimestamp(last_modified).strftime(s.FORMAT_TIME)

                    if type(partial_size) is int:
                        stat_total_tar_downloaded += partial_size
                        stat_storm_tar_downloaded += partial_size

                #################################################
                # Part file exists without any lock association #
                #################################################

                elif os.path.exists(tar_file_path + s.PART_SUFFIX):
                    exists_str += 'Partially downloaded: ' + \
                                  h.to_readable_bytes(os.path.getsize(tar_file_path + s.PART_SUFFIX))

                    stat_total_tar_downloaded += os.path.getsize(tar_file_path + s.PART_SUFFIX)
                    stat_storm_tar_downloaded += os.path.getsize(tar_file_path + s.PART_SUFFIX)

                ###################################################################
                # No fully or partially downloaded file exists or has a lock file #
                ###################################################################

                else:
                    exists_str += 'Not downloaded.'

                print('\t\t-', tar_file, ' ...', h.to_readable_bytes(tar_file.get_file_size_origin()),
                      ' ...', exists_str)

                # Resort to querying the website if the total size cannot be determined locally
                if type(total_size) is not int:
                    total_size = tar_file.get_file_size_origin()

                stat_total_tar_size += total_size
                stat_storm_tar_size += total_size

            print('\t\tTotal:', h.to_readable_bytes(stat_storm_tar_downloaded), '/',
                  h.to_readable_bytes(stat_storm_tar_size),
                  ' (' + str(floor((stat_storm_tar_downloaded / stat_storm_tar_size) * 100)) + '%)')

        else:
            print('\t' * 2 + '<No .tar files detected in index.html>')

        print()
        storm_number += 1

    if stat_total_tar_size > 0:
        print('Total:', h.to_readable_bytes(stat_total_tar_downloaded), '/', h.to_readable_bytes(stat_total_tar_size),
              ' (' + str(floor((stat_total_tar_downloaded / stat_total_tar_size) * 100)) + '%)')

#############################################
# Start the actual collection of .tar files #
#############################################

if OPTIONS.download:
    for storm in storms:
        for tar in storm.get_tar_list(OPTIONS.tar):
            download_incomplete: bool = True  # Turns to 'False' when the file is downloaded successfully

            # Save the tar to a directory based on the storm's ID (normalize the path to avoid errors)
            save_path: Union[bytes, str] = os.path.join(DOWNLOAD_PATH, storm.storm_id.title())

            # Repeatedly try to download the .tar until it completes successfully
            while download_incomplete:
                try:
                    lock_info_part = h.get_lock_info(
                        base_file=os.path.join(save_path, str(tar.tar_file_name) + '.tar' + s.PART_SUFFIX))

                    if OPTIONS.overwrite is False and h.is_locked_by_another_user(
                            base_file=str(tar.tar_file_name) + '.tar', this_user=OPTIONS.user):

                        print('Another user has fully downloaded ', tar.tar_file_name, '.tar!  ... Skipping')
                        download_incomplete = False

                    elif OPTIONS.overwrite or lock_info_part['user'] is None or OPTIONS.user == lock_info_part['user']:

                        tar.download_url(output_dir=save_path, user=OPTIONS.user, overwrite=OPTIONS.overwrite)
                        download_incomplete = False

                    else:
                        print('Another user is in the process of downloading ', tar.tar_file_name, '.tar!  ... Skipping')
                        download_incomplete = False

                except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionResetError) as e:
                    print('The download ran into a connection error: ' + str(e))
                except ConnectionRefusedError as e:
                    print('I don\'t think the website likes you right now. Error: ' + str(e))

                if download_incomplete:
                    print('Will retry download in 10 seconds...')
                    time.sleep(10)
