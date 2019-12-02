# Imports.

import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os
# from os import path
from sklearn.model_selection import train_test_split
# from tensorflow import keras
# from keras.preprocessing.image import ImageDataGenerator

# Just a lil comment to rememebr wat each number for impact means
# NoneId:0,
# SwashId:1
# CollisionId:2
# OverwashId:3
# InundationId:4

# Global Constants.

SELF_PATH = os.getcwd()
PATH_TO_FILE_STREAM = 'G:/Shared drives/P-Sick'
PATH_TO_IMAGES = os.path.join(PATH_TO_FILE_STREAM, 'small/Florence/20180917a_jpgs')
PATH_TO_TAG_CSV = os.path.join(SELF_PATH, '../tagging_data.csv')

TEST_TO_TRAIN_RATIO = 0.3

# First lets load the csv that has all the completely tagged image tags.
df_image_tags = pd.read_csv(PATH_TO_TAG_CSV)
# create training and test set
tagged_image_list = df_image_tags['image_id'].tolist()
training_images, testing_images = train_test_split(tagged_image_list, test_size=TEST_TO_TRAIN_RATIO, random_state=42)

# do cnn shit
# profit?
