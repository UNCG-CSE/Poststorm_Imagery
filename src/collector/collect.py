import argparse
from typing import List

from src.collector import Tar
from src.collector.ConnectionHandler import ConnectionHandler

from src.collector.Storm import Storm

# Document and register parameters for this program in command-line

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

parser.add_argument('--path', '-p', default=Tar.TAR_PATH_CACHE,
                    help='The path on your system to download the tar files to (Default: %(default)s).')

parser.add_argument('--download', '-d', action='store_true',
                    help='If included, the program will automatically download all files found, sequentially '
                         '(Default: %(default)s).')

parser.add_argument('--overwrite', '-o', action='store_true',
                    help='If included, the program will overwrite any existing .tar files found in the directory by '
                         'the same name (Default: %(default)s).')

# Add custom OPTIONS to the script when running command line
OPTIONS = parser.parse_args()

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
        print(storms[0].get_tar_list()[0].download_url(output_file_dir_path=OPTIONS.path, overwrite=OPTIONS.overwrite))
