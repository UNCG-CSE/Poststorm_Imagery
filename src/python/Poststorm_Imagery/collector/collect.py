import argparse
import getpass
import os
import time
from datetime import datetime

from typing import List, Union

import requests

from collector import TarRef, helpers
from collector.ConnectionHandler import ConnectionHandler
from collector.Storm import Storm

################################################################
# Build and document parameters for the command-line arguments #
################################################################

DATA_PATH: Union[bytes, str] = os.path.abspath('../../data')
TAR_PATH_CACHE: Union[bytes, str] = os.path.join(DATA_PATH, 'tar_cache')


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

parser.add_argument('--path', '-p', default=TAR_PATH_CACHE,
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

# Add custom OPTIONS to the script when running command line
OPTIONS: argparse.Namespace = parser.parse_args()

# Convert string to absolute path for uniformity
DOWNLOAD_PATH = os.path.abspath(OPTIONS.path)

# Expand out any path keywords or variables
DOWNLOAD_PATH = os.path.expanduser(os.path.expandvars(DOWNLOAD_PATH))


#######################################
# Start the actual collection of data #
#######################################


c = ConnectionHandler()

storms: List[Storm] = c.get_storm_list(OPTIONS.storm)

# Present the storm as a number the user can reference quickly
storm_number: int = 1

# Keep a running total of the number of bytes of the download
stat_total_tar_size: int = 0

# Keep a running total of the number of bytes of downloaded already
stat_total_tar_downloaded: int = 0

if OPTIONS.no_status is False:
    print('Download Status Report (' + datetime.now().strftime("%B %d, %Y at %I:%M %p") + ') <-s ' + OPTIONS.storm +
          ' -t ' + OPTIONS.tar + ' -p ' + OPTIONS.path + '> on v' + requests.__version__)
    print()

    for storm in storms:
        print(str(storm_number) + '.  \t' + str(storm))

        stat_storm_tar_size: int = 0

        tar_list = storms[storm_number - 1].get_tar_list(OPTIONS.tar)

        if len(tar_list) > 0:
            for tar_file in tar_list:

                # Create an appending string to print statuses next to .tar info
                exists_str: str = ''

                tar_file_path = os.path.join(os.path.join(DOWNLOAD_PATH, storm.storm_id.title()),
                                             str(tar_file.tar_file_name) + '.tar')

                if os.path.exists(tar_file_path):
                    exists_str += 'Fully downloaded: ' + \
                                 helpers.get_byte_size_readable(os.path.getsize(
                                     tar_file_path))

                    if os.path.getsize(tar_file_path) != tar_file.get_file_size_origin():
                        exists_str += '  ... ERROR: Sizes do not match!'
                    else:
                        stat_total_tar_downloaded += os.path.getsize(tar_file_path)

                elif os.path.exists(tar_file_path + '.lock'):

                    lock_info = helpers.get_lock_info(base_file=tar_file_path)
                    user: str = lock_info['user']
                    total_size: int = lock_info['total_size_bytes']

                    exists_str += 'Fully downloaded (' + user + '): ' + \
                                  helpers.get_byte_size_readable(total_size)

                    stat_total_tar_downloaded += total_size

                elif os.path.exists(tar_file_path + '.part'):
                    exists_str += 'Partially downloaded: ' + \
                                 helpers.get_byte_size_readable(os.path.getsize(
                                     tar_file_path + '.part'))

                    stat_total_tar_downloaded += os.path.getsize(tar_file_path + '.part')

                elif os.path.exists(tar_file_path + '.part.lock'):

                    lock_info = helpers.get_lock_info(base_file=tar_file_path + '.part')
                    partial_size: int = lock_info['size_bytes']
                    total_size: int = lock_info['total_size_bytes']
                    user: str = lock_info['user']

                    exists_str += 'Partially downloaded (' + user + '): ' + \
                                  helpers.get_byte_size_readable(partial_size)

                    if total_size is not None and total_size != tar_file.get_file_size_origin():
                        exists_str += '  ... ERROR: Total size in lock file does not match the website copy!'
                    else:
                        stat_total_tar_downloaded += partial_size

                else:
                    exists_str += 'Not downloaded.'

                print('\t' * 2 + '- ' + str(tar_file) +
                      '  ... ' + helpers.get_byte_size_readable(tar_file.get_file_size_origin()) +
                      '  ... ' + exists_str)

                stat_total_tar_size += tar_file.get_file_size_origin()
                stat_storm_tar_size += tar_file.get_file_size_origin()

            print('\t' * 2 + 'Total: ' + helpers.get_byte_size_readable(stat_storm_tar_size))

        else:
            print('\t' * 2 + '<No .tar files detected in index.html>')

        print()
        storm_number += 1

    print('Total: ' + helpers.get_byte_size_readable(stat_total_tar_downloaded) + ' / ' + helpers.get_byte_size_readable(stat_total_tar_size))

if OPTIONS.download:
    for storm in storms:
        for tar in storm.get_tar_list(OPTIONS.tar):
            download_incomplete: bool = True

            # Save the tar to a directory based on the storm's ID (normalize the path to avoid errors)
            save_path: Union[bytes, str] = os.path.join(DOWNLOAD_PATH, storm.storm_id.title())

            while download_incomplete:
                try:
                    lock_info_part = helpers.get_lock_info(
                        base_file=os.path.join(save_path, str(tar.tar_file_name) + '.tar.part'))
                    lock_info_full = helpers.get_lock_info(
                        base_file=os.path.join(save_path, str(tar.tar_file_name) + '.tar'))

                    if OPTIONS.overwrite is False and (lock_info_full['user'] is not None
                                                       or OPTIONS.user != lock_info_full['user']):

                        print('Another user has fully downloaded ' + tar.tar_file_name +
                              '.tar!  ... Skipping')
                        download_incomplete = False

                    elif OPTIONS.overwrite or lock_info_part['user'] is None or OPTIONS.user == lock_info_part['user']:

                        tar.download_url(output_dir=save_path, user=OPTIONS.user, overwrite=OPTIONS.overwrite)

                    else:
                        print('Another user is in the process of downloading ' + tar.tar_file_name +
                              '.tar!  ... Skipping')
                        download_incomplete = False

                except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionResetError) as e:
                    print('The download ran into a connection error: ' + str(e))
                except ConnectionRefusedError as e:
                    print('I don\'t think the website likes you right now. Error: ' + str(e))
                except Exception as e:
                    print('The download encountered an error: ' + str(e))

                if download_incomplete:
                    print('Will retry download in 10 seconds...')
                    time.sleep(10)
