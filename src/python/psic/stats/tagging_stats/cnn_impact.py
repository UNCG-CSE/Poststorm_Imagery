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
import glob
import random

# Just a lil comment to rememebr wat each number for impact means
# NoneId:0,
# SwashId:1
# CollisionId:2
# OverwashId:3
# InundationId:4

# Global Constants.

SELF_PATH = os.getcwd()
PATH_TO_FILE_STREAM = 'G:\Shared drives\P-Sick'
PATH_TO_TRAINING_IMAGES = os.path.join(PATH_TO_FILE_STREAM,'data\Florence/20180917a_jpgs')
PATH_TO_TESTING_IMAGES = os.path.join(PATH_TO_FILE_STREAM,'data\Florence/20180918a_jpgs')
TEST_IMAGE_SIZE = 30

PATH_TO_TAG_CSV = os.path.join(SELF_PATH,'../tagging_data.csv')

# First lets load the csv that has all the completely tagged image tags.
df_image_tags = pd.read_csv(PATH_TO_TAG_CSV)

# Get a series of the images
series_images = df_image_tags['image_id']

# Check if all the images in the series exist
# all_exist = True
# count = 0
# not_exist = 0
# for image in series_images:
#     count += 1
#     all_exist = all_exist and path.exists(os.path.join(PATH_TO_TRAINING_IMAGES,image))
#     if not path.exists(os.path.join(PATH_TO_TRAINING_IMAGES,image)):
#         not_exist += 1

# if all_exist:
#     print(f'All {count} images exist')
# else:
#     print(f'Of {count} images, {not_exist} dont exist')

#glob.glob("G:\\Shared drives\\P-Sick\\data\\Florence/20180917a_jpgs/jpgs/*.jpg")

LIST_OF_POSSIBLE_TESTING_IMAGES = glob.glob(f"{PATH_TO_TESTING_IMAGES}/jpgs/*.jpg")
# print(len(LIST_OF_POSSIBLE_TESTING_IMAGES))
# print(type(LIST_OF_POSSIBLE_TESTING_IMAGES))

LIST_OF_TRAINING_IMAGES = []

selected_training_image_count = 0
while (selected_training_image_count < TEST_IMAGE_SIZE):
    secure_random = random.SystemRandom()
    selected_image = secure_random.choice(LIST_OF_POSSIBLE_TESTING_IMAGES)
    
    # # Make sure we dont select a duplicated file that has (1) in name
    if selected_image.find("(1)") == -1:
        split_image_name = selected_image.split("\\")[-1]
        # Make sure we havent added this image
        if split_image_name not in LIST_OF_TRAINING_IMAGES:
            # Use split just to get the file name
            LIST_OF_TRAINING_IMAGES.append(split_image_name)
            selected_training_image_count+=1
        
# Just incase, drop any duplicates
LIST_OF_TRAINING_IMAGES =  list( dict.fromkeys(LIST_OF_TRAINING_IMAGES) )

print('--- Training Set ---')
print(series_images.head())
print('\n')

print('--- Testing Set ---')
print(LIST_OF_TRAINING_IMAGES)
# finding how many duplicates
# duplicated_count = 0
# for image in LIST_OF_POSSIBLE_TESTING_IMAGES:
#     if image.find("(1)") != -1:
#         duplicated_count +=1
# print(duplicated_count)