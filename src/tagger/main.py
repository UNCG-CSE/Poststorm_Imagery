import argparse
from typing import List

from src.tagger.ConnectionHandler import ConnectionHandler

# Add custom options to the script when running command line
from src.tagger.Storm import Storm

parser = argparse.ArgumentParser('Options for tagging images via command line')
parser.add_argument('--storm', '-s', default='.*', help='Regular expression search for storm')
parser.add_argument('--tar', '-t', default='.*', help='Regular expression search for tar files')
options = parser.parse_args()

c = ConnectionHandler()

storms: List[Storm] = c.get_storm_list(options.storm)

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
