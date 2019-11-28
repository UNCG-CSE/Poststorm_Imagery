# Imports.

import pandas as pd
import jsonpickle
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import dateutil.parser
from datetime import datetime
import statistics
import argparse

# Global Constants.

SELF_PATH = os.getcwd()
PATH_TO_JSON = os.path.join(SELF_PATH,'../tag_states.json')
PATH_TO_OUTPUT_CSV = os.path.join(SELF_PATH,'../tagging_data.csv')


# Command line args.

parser = argparse.ArgumentParser(description='take JSON pickle and turn into CSV')

parser.add_argument('--path', '-p', default=PATH_TO_JSON,
                    help='The path to the JSON pickle file to turn into a CSV')

parser.add_argument('--out', '-o', default=PATH_TO_OUTPUT_CSV,
                    help='The path to place the CSV')

# Get args.
args = parser.parse_args()

# Depickle tag state json.
depickled = None
with open(args.path, 'r') as f:
    depickled = jsonpickle.decode(f.read())

# Get the total number of images that are done being tagged,and number of images
# that are partially tagged.
total_finished =len(depickled.finished_tagged_queue)
total_incomplete_tagged=0
    
for image in depickled.pending_images_queue:
    if len(image.get_taggers()) > 0:
        total_incomplete_tagged+=1

total_skipped = len(depickled.max_skipped_queue)
total_currently_getting_tagged = len(depickled.current_image)

# How many images have circulated.
total_images_handled = total_incomplete_tagged + total_finished + total_skipped + total_currently_getting_tagged
tagged_ratio = total_incomplete_tagged/total_images_handled

df_basic_tag_data = pd.DataFrame([{ 
        'partial':total_incomplete_tagged,
        'done':total_finished,
        'skipped':total_skipped,
        'current':total_currently_getting_tagged,
        'tagged_ratio': tagged_ratio
    }])

print('\n==== Basic tagging data ====')
print(df_basic_tag_data.head())
print('\n')
# depickle
# iterate
#gen csv