import argparse
import os
import time
from typing import List, Union

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
                         'Search applies to the date string listed on the website (format varies based on storm) if found '
                         'as well as the file name (excluding the .tar) and the label (usually "TIF" or "RAW JPEG". '
                         'Defaults to ALL .tar files (%(default)s).')

parser.add_argument('--path', '-p', default=TAR_PATH_CACHE,
                    help='The path on your system to download the tar files to (Default: %(default)s).')

parser.add_argument('--download', '-d', action='store_true',
                    help='If included, the program will automatically download all files found, sequentially '
                         '(Default: %(default)s).')

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

for storm in storms:
    print(str(storm_number) + '.  \t' + str(storm))

    tar_list = storms[storm_number - 1].get_tar_list()

    if len(tar_list) > 0:
        for tar_file in tar_list:
            print('\t' * 2 + '- ' + str(tar_file))
    else:
        print('\t' * 2 + '<No .tar files detected in index.html>')

    print()
    storm_number += 1

if OPTIONS.download:
    for storm in storms:
        for tar in storm.get_tar_list():
            download_incomplete: bool = True

            # Save the tar to a directory based on the storm's ID (normalize the path to avoid errors)
            save_path: Union[bytes, str] = os.path.join(DOWNLOAD_PATH, storm.storm_id.title())

            while download_incomplete:
                try:
                    tar.download_url(output_dir=save_path, overwrite=OPTIONS.overwrite)
                    download_incomplete = False
                except Exception as e:
                    print('The download encountered an error: ' + str(e))
                    print('Will retry download in 10 seconds...')
                    time.sleep(10)
