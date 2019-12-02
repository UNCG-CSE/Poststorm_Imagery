# Imports.

import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os
# from os import path
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
import time
# from tensorflow.python.client import device_lib
import shutil

#print(device_lib.list_local_devices())
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
NUM_RANDOM_IMAGES_GEN = 2
TRAINING_IMAGE_FOLDER = "../_training_images"
TESTING_IMAGE_FOLDER = "../_testing_images"
IMG_WIDTH, IMG_HEIGHT = 150, 150
SIZE_OF_BATCH = 16

# First lets load the csv that has all the completely tagged image tags.
df_image_tags = pd.read_csv(PATH_TO_TAG_CSV)

# create training and test set
tagged_image_list = df_image_tags['image_id'].tolist()
training_images, testing_images = train_test_split(tagged_image_list, test_size=TEST_TO_TRAIN_RATIO, random_state=42)
print('>>>',len(training_images), len(testing_images))

# Before we copy the images, remove all files within these folders
for file in os.listdir(TRAINING_IMAGE_FOLDER):
    os.remove(os.path.join(TRAINING_IMAGE_FOLDER,file)) 

for file in os.listdir(TESTING_IMAGE_FOLDER):
    os.remove(os.path.join(TESTING_IMAGE_FOLDER,file)) 

#Copy our training and test images into their respective folders, while keeping metadata with copy2
for image in training_images:
    shutil.copy2(os.path.join(PATH_TO_IMAGES,image),  os.path.join(TRAINING_IMAGE_FOLDER,image))

for image in testing_images:
    shutil.copy2(os.path.join(PATH_TO_IMAGES,image),  os.path.join(TESTING_IMAGE_FOLDER,image))

print(">>> Moved training and test images to their respective folders")

# do cnn shit

# I am following this https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html


# A model that can store a lot of information has the potential to be more accurate by leveraging more features, but it is also more at risk to start storing irrelevant features. 
# Meanwhile, a model that can only store a few features will have to focus on the most significant features found in the data, and these are more likely to be truly relevant and to generalize better.

# model = Sequential()
# model.add(Conv2D(32, (3, 3), input_shape=(IMG_WIDTH, IMG_HEIGHT,3))) # 3 is features?
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# model.add(Conv2D(32, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# model.add(Conv2D(64, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# # the model so far outputs 3D feature maps (height, width, features)

# model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
# model.add(Dense(64))
# model.add(Activation('relu'))
# model.add(Dropout(0.5))
# model.add(Dense(1))
# model.add(Activation('sigmoid'))

# model.compile(loss='binary_crossentropy',
#               optimizer='rmsprop',
#               metrics=['accuracy'])


# # No configuration
# train_datagen = ImageDataGenerator()

# # No configuration
# test_datagen = ImageDataGenerator()

# # this is a generator that will read pictures found in
# # subfolers of 'data/train', and indefinitely generate
# # batches of augmented image data
# train_generator = train_datagen.flow_from_directory(
#         TRAINING_IMAGE_FOLDER,  # this is the target directory
#         target_size=(IMG_WIDTH, IMG_HEIGHT),  # all images will be resized to 150x150
#         batch_size=SIZE_OF_BATCH,
#         class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels

# # this is a similar generator, for validation data
# validation_generator = test_datagen.flow_from_directory(
#         TESTING_IMAGE_FOLDER,
#         target_size=(IMG_WIDTH, IMG_HEIGHT),
#         batch_size=SIZE_OF_BATCH,
#         class_mode='binary')

# t0 = time.time()
# model.fit_generator(
#         train_generator,
#         steps_per_epoch=16 // SIZE_OF_BATCH,
#         epochs=2,
#         validation_data=validation_generator,
#         validation_steps=16 // SIZE_OF_BATCH)
# model.save_weights('first_try.h5')  # always save your weights after training or during training
# t1 = time.time()

# print('>>> Time:',t1-t0)
# profit?
