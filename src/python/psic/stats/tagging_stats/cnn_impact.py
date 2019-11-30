# Imports.

import pandas as pd
import jsonpickle
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
from os import path
import dateutil.parser
from datetime import datetime
import statistics

# Just a lil comment to rememebr wat each number for impact means
# NoneId:0,
# SwashId:
# CollisionId:
# OverwashId:
# InundationId:

# Global Constants.

SELF_PATH = os.getcwd()
PATH_TO_FILE_STREAM = 'G:\Shared drives\P-Sick'
PATH_TO_IMAGES = os.path.join(PATH_TO_FILE_STREAM,'data\Florence/20180917a_jpgs')
PATH_TO_TAG_CSV = os.path.join(SELF_PATH,'../tagging_data.csv')

# First lets load the csv that has all the completely tagged image tags.
df_image_tags = pd.read_csv(PATH_TO_TAG_CSV)

# Get a series of the images
series_images = df_image_tags['image_id']

# Check if all the images in the series exist
all_exist = True
count = 0
not_exist = 0
for image in series_images:
    count += 1
    all_exist = all_exist and path.exists(os.path.join(PATH_TO_IMAGES,image))
    if not path.exists(os.path.join(PATH_TO_IMAGES,image)):
        not_exist += 1

if all_exist:
    print(f'All {count} images exist')
else:
    print(f'Of {count} images, {not_exist} dont exist')


