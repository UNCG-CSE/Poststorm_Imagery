import random
import warnings
from getpass import getuser
from os import path

import cv2
import numpy as np
import pandas as pd

from psic.resizer.generate import ResizeImages

warnings.filterwarnings("ignore")

SEED = 405


def get_washover_data() -> tuple:
    random.seed = SEED

    if getuser() == 'mattm':
        DRIVE_PATH = 'F:\\Shared drives\\P-Sick'
    else:
        DRIVE_PATH = 'mnt/Secondary/mcmoretz@uncg.edu/C-Sick'

    FINAL_TAGS_CSV = path.join(DRIVE_PATH, 'tag_csv/tagging_data.csv')
    FULL_IMAGES_DIR = path.join(DRIVE_PATH, 'data/Florence/20180917a_jpgs/jpgs')
    SMALL_IMAGES_DIR = path.join(DRIVE_PATH, 'vsmall/5/Florence/20180917a_jpgs/jpgs')

    print('Reading in the image list and labels...')
    data = pd.read_csv(FINAL_TAGS_CSV, usecols=['image_id', 'washover'])

    print(data)

    X = list()  # The features of the data
    y = data['washover']  # The labels of the data

    for i, row in data.iterrows():
        print('\rLoaded %s of %s images ' % (i, len(data)) + '.' * (i % 3), end='')
        full_image_path = path.join(FULL_IMAGES_DIR, row['image_id'])
        small_image_path = path.join(SMALL_IMAGES_DIR, row['image_id'])

        if not (path.exists(small_image_path) and path.isfile(small_image_path)):
            # Create a new compressed image that is 5% of original image size (516 x 388 pixels) using nearest neighbor
            ResizeImages.resize_image_at_path(original_path=full_image_path, small_path=small_image_path,
                                              new_res=(516, 388))

        # Load a 2d array of grayscale values
        image: np.ndarray = cv2.imread(small_image_path, 0)

        # String each row together to form a single 1d array of features
        image = image.ravel()

        # Create a row as a DataFrame with all the features as columns
        # features: pd.DataFrame = pd.DataFrame(image.reshape(-1, len(image)))

        X.append(list(image))

    print('\rLoaded all of the images!')

    print('\nGenerating a DataFrame from image features...')
    print(pd.DataFrame(X, columns=range(len(X[0]))))

    return X, y
