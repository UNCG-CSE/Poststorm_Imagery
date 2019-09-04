import argparse

from src.tagger.ConnectionHandler import ConnectionHandler

# Add custom options to the script when running command line
parser = argparse.ArgumentParser('Options for tagging images via command line')
parser.add_argument('--search', '-s', default='.*', help='Regular expression search')
options = parser.parse_args()

c = ConnectionHandler(search_re=options.search)

# Present the storm as a number the user can reference quickly
storm_number: int = 1

for storm in c.storm_list:
    print(str(storm_number) + '.  \t' + str(storm))
    storm_number += 1
