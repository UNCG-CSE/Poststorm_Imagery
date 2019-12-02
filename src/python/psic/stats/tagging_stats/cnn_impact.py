# Imports.

import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os
# from os import path
from sklearn.model_selection import train_test_split
# from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
# import cv2

# Just a lil comment to rememebr wat each number for impact means
# NoneId:0,
# SwashId:1
# CollisionId:2
# OverwashId:3
# InundationId:4

# Global Constants.

SELF_PATH = os.getcwd()
PATH_TO_FILE_STREAM = 'G:\\Shared drives\\P-Sick'
PATH_TO_IMAGES = os.path.join(PATH_TO_FILE_STREAM, 'small\\Florence\\20180917a_jpgs\\jpgs')
PATH_TO_TAG_CSV = os.path.join(SELF_PATH, '../tagging_data.csv')
TEST_TO_TRAIN_RATIO = 0.3
NUM_RANDOM_IMAGES_GEN = 10

# First lets load the csv that has all the completely tagged image tags.
df_image_tags = pd.read_csv(PATH_TO_TAG_CSV)
# create training and test set
tagged_image_list = df_image_tags['image_id'].tolist()
training_images, testing_images = train_test_split(tagged_image_list, test_size=TEST_TO_TRAIN_RATIO, random_state=42)
print(len(training_images), len(testing_images))

# do cnn shit

# I am following this https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html
# datagen = ImageDataGenerator(
#         rotation_range=0,
#         width_shift_range=0.0,
#         height_shift_range=0.0,
#         rescale=None,
#         shear_range=0.0,
#         zoom_range=0.0,
#         horizontal_flip=True,
#         vertical_flip=True,
#         fill_mode='nearest')


# img_count = 0
# for image in tagged_image_list:
#     img = load_img(os.path.join(PATH_TO_IMAGES,image))  # this is a PIL image
#     x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
#     x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

#     # the .flow() command below generates batches of randomly transformed images
#     # and saves the results to the `preview/` directory
#     i = 0
#     for batch in datagen.flow(x, batch_size=1,save_to_dir='../random_image_gen_output'):
#         i += 1
#         if i > NUM_RANDOM_IMAGES_GEN:
#             break  # otherwise the generator would loop indefinitely
#     img_count +=1
#     print(img_count)
# print('done')

# profit?
